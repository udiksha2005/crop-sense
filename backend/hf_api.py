# backend/hf_api.py
import os
import requests
from io import BytesIO
from typing import Tuple
from PIL import Image

HF_API_URL = "https://api-inference.huggingface.co/models/google/vit-base-patch16-224"


# Read HF token from environment or fallback to placeholder
HF_API_TOKEN = os.getenv("HF_API_TOKEN")


HEADERS = {"Authorization": f"Bearer {HF_API_TOKEN}"}


def predict_disease(image: Image.Image) -> dict:
    """
    Converts PIL image → bytes and sends to HuggingFace model.
    Returns: {"label": str, "confidence": float}
    """

    # Convert image to bytes (JPEG)
    buffer = BytesIO()
    image.save(buffer, format="JPEG")
    img_bytes = buffer.getvalue()

    # Send bytes to HF model
    response = requests.post(
        HF_API_URL,
        headers=HEADERS,
        data=img_bytes,
        timeout=30,
    )
    response.raise_for_status()

    data = response.json()

    # HF sometimes returns {"error": "..."}
    if isinstance(data, dict) and "error" in data:
        raise RuntimeError(f"HuggingFace error: {data['error']}")

    # Expected: list of predictions
    top_pred = data[0]
    return {
        "label": top_p_
    }
