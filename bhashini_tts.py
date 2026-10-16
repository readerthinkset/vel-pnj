import os
import sys
import base64
import requests
from pathlib import Path

CONFIG_URL = "https://meity-auth.ulcacontrib.org/ulca/apis/v0/model/getModelsPipeline"
PIPELINE_ID = "64392f96daac500b55c543d0"

def generate_bhashini_audio(text: str, target_lang: str, output_path: str, gender: str = "female") -> bool:
    """
    Generate audio using Bhashini Indic-TTS API.
    Supports all 22 official Indian languages including:
      - 'or' / 'ory' for Odia
      - 'pa' / 'pan' for Punjabi
    """
    user_id = os.getenv("BHASHINI_USER_ID")
    api_key = os.getenv("BHASHINI_API_KEY") or os.getenv("ULCA_API_KEY")
    
    if not user_id or not api_key:
        print("[bhashini] Missing BHASHINI_USER_ID or BHASHINI_API_KEY. Please set them in .env or environment.")
        return False

    # Normalize language codes to ISO 639-1
    lang_code = target_lang.lower().strip()
    if lang_code in ["odia", "oriya", "ory"]:
        lang_code = "or"
    elif lang_code in ["punjabi", "pan"]:
        lang_code = "pa"

    headers = {
        "Content-Type": "application/json",
        "userID": user_id,
        "ulcaApiKey": api_key,
    }

    payload = {
        "pipelineTasks": [
            {
                "taskType": "tts",
                "config": {
                    "language": {"sourceLanguage": lang_code}
                }
            }
        ],
        "pipelineRequestConfig": {"pipelineId": PIPELINE_ID}
    }

    try:
        # Step 1: Query Pipeline Config
        res = requests.post(CONFIG_URL, headers=headers, json=payload, timeout=25)
        if res.status_code != 200:
            print(f"[bhashini] Pipeline config failed ({res.status_code}): {res.text}")
            return False
            
        res_data = res.json()
        service_id = res_data["pipelineResponseConfig"][0]["serviceId"]
        callback_url = res_data["pipelineInferenceAPIEndPoint"]["callbackUrl"]
        inference_key_name = res_data["pipelineInferenceAPIEndPoint"]["inferenceApiKey"]["name"]
        inference_key_value = res_data["pipelineInferenceAPIEndPoint"]["inferenceApiKey"]["value"]

        # Step 2: Inference Call
        inference_headers = {
            "Content-Type": "application/json",
            inference_key_name: inference_key_value
        }
        
        inference_payload = {
            "pipelineTasks": [
                {
                    "taskType": "tts",
                    "config": {
                        "language": {"sourceLanguage": lang_code},
                        "serviceId": service_id,
                        "gender": gender,
                        "audioFormat": "mp3"
                    }
                }
            ],
            "inputData": {
                "input": [{"source": text}]
            }
        }

        infer_res = requests.post(callback_url, headers=inference_headers, json=inference_payload, timeout=30)
        if infer_res.status_code != 200:
            print(f"[bhashini] Inference failed ({infer_res.status_code}): {infer_res.text}")
            return False

        infer_data = infer_res.json()
        audio_base64 = infer_data["pipelineResponse"][0]["audio"][0]["audioContent"]
        audio_bytes = base64.b64decode(audio_base64)
        
        out = Path(output_path)
        out.parent.mkdir(parents=True, exist_ok=True)
        with open(out, "wb") as f:
            f.write(audio_bytes)
            
        print(f"[bhashini] ✓ Saved {lang_code.upper()} audio to {out.name} ({len(audio_bytes)} bytes)")
        return True

    except Exception as e:
        print(f"[bhashini] Exception during TTS generation: {e}")
        return False
