import requests
import os
from dotenv import load_dotenv

load_dotenv()

HF_TOKEN = os.getenv("HF_API_TOKEN")
MODEL_ID = os.getenv("MODEL_ID")

API_URL = f"https://api-inference.huggingface.co/models/{MODEL_ID}"

HEADERS = {
    "Authorization": f"Bearer {HF_TOKEN}"
}


def predict_disease(image_bytes: bytes):

    try:
        response = requests.post(
            API_URL,
            headers=HEADERS,
            data=image_bytes,
            timeout=60
        )

        response.raise_for_status()
        predictions = response.json()

        if not isinstance(predictions, list) or len(predictions) == 0:
            return {"error": "Invalid prediction response"}

        top_prediction = predictions[0]

        label = top_prediction.get("label")
        confidence = round(top_prediction.get("score", 0) * 100, 2)

        return {
            "label": label,
            "confidence": confidence
        }

    except Exception as e:
        return {"error": str(e)}
