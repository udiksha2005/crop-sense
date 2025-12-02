import os
import requests  # type: ignore

HF_API_TOKEN = os.getenv("HF_API_TOKEN")

MODEL_ID = "IronNeuron/leaf-disease-classification-vit-base"
API_URL = f"https://router.huggingface.co/pipeline/feature-extraction/{MODEL_ID}"

headers = {
    "Authorization": f"Bearer {HF_API_TOKEN}",
}

def predict_disease(image_bytes: bytes):
    try:
        response = requests.post(
            API_URL,
            headers=headers,
            files={"inputs": image_bytes},
        )

        if response.status_code != 200:
            return {"error": response.text}

        result = response.json()

        # assumes top label and score
        return {
            "label": result[0]["label"],
            "confidence": result[0]["score"],
        }

    except Exception as e:
        return {"error": str(e)}