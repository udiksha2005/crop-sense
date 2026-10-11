import os
from fastapi import UploadFile
from backend.config.config import get_settings

settings = get_settings()

ORIGINAL_DIR = os.path.join(settings.UPLOAD_DIRECTORY, "original")
PROCESSED_DIR = os.path.join(settings.UPLOAD_DIRECTORY, "processed")

# Ensure directories exist automatically
os.makedirs(ORIGINAL_DIR, exist_ok=True)
os.makedirs(PROCESSED_DIR, exist_ok=True)

async def save_original_image(file: UploadFile, contents: bytes) -> str:
    """Save the uploaded original image to disk"""
    file_path = os.path.join(ORIGINAL_DIR, file.filename)
    with open(file_path, 'wb') as out_file:
        out_file.write(contents)
    return file_path

def save_processed_image(filename: str, image_bytes: bytes) -> str:
    """Save the processed/cropped image to disk"""
    file_path = os.path.join(PROCESSED_DIR, f"processed_{filename}")
    with open(file_path, 'wb') as out_file:
        out_file.write(image_bytes)
    return file_path
