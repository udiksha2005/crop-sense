from PIL import Image # type: ignore
import io

def preprocess_image(image):
    """
    Ensures image is PIL Image.
    Converts to RGB, resizes, and returns JPEG bytes.
    """
    # If input is bytes → convert to PIL
    if isinstance(image, bytes):
        image = Image.open(io.BytesIO(image))

    # Just in case input is UploadFile.file stream
    if not isinstance(image, Image.Image):
        image = Image.open(image)

    # Convert to RGB
    image = image.convert("RGB")

    # Resize
    image = image.resize((224, 224))

    # Convert PIL → bytes
    buffer = io.BytesIO()
    image.save(buffer, format="JPEG")
    buffer.seek(0)

    return buffer.getvalue()
