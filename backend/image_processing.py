# backend/image_processing.py

from PIL import Image
import io

TARGET_SIZE = 224


def preprocess_image(image_bytes: bytes) -> bytes:
    """
    Preprocess image for model:
    - Convert to RGB
    - Resize while keeping aspect ratio
    - Pad to 224x224
    - Return PNG bytes
    """

    try:
        image = Image.open(io.BytesIO(image_bytes))
        image = image.convert("RGB")

        # Resize maintaining aspect ratio
        image.thumbnail((TARGET_SIZE, TARGET_SIZE))

        # Create white background
        new_image = Image.new("RGB", (TARGET_SIZE, TARGET_SIZE), (255, 255, 255))

        # Center image
        x = (TARGET_SIZE - image.width) // 2
        y = (TARGET_SIZE - image.height) // 2
        new_image.paste(image, (x, y))

        # Convert back to bytes
        buffer = io.BytesIO()
        new_image.save(buffer, format="PNG")
        buffer.seek(0)

        return buffer.getvalue()

    except Exception as e:
        raise ValueError(f"Image preprocessing failed: {str(e)}")                                                                                                                                     
