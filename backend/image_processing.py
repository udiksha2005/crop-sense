# backend/image_processing.py
from PIL import Image

def preprocess_image(image: Image.Image) -> Image.Image:
    """
    Convert image to RGB and resize to 224x224 for the HF model.
    """
    # Ensure RGB
    image = image.convert("RGB")

    # Resize for model input
    image = image.resize((224, 224))

    return image
