from PIL import Image
import io

TARGET_SIZE = 224


def preprocess_image(image_bytes: bytes) -> bytes:
    """
    Preprocess image for the AI model.

    Steps:
    1. Convert to RGB
    2. Resize while maintaining aspect ratio
    3. Pad image to 224x224
    4. Return processed image as PNG bytes
    """

    try:
        # Load image from uploaded bytes
        image = Image.open(io.BytesIO(image_bytes))

        # Convert to RGB (important for model)
        image = image.convert("RGB")

        # Maintain aspect ratio
        image.thumbnail((TARGET_SIZE, TARGET_SIZE))

        # Create white background
        new_image = Image.new("RGB", (TARGET_SIZE, TARGET_SIZE), (255, 255, 255))

        # Center the image
        x = (TARGET_SIZE - image.width) // 2
        y = (TARGET_SIZE - image.height) // 2

        new_image.paste(image, (x, y))

        # Convert back to bytes
        buffer = io.BytesIO()
        new_image.save(buffer, format="PNG")
        buffer.seek(0)

        return buffer.getvalue()

    except Exception as e:
        raise ValueError(f"Image preprocessing failed: {e}")                                                                                                                               