import torch
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image
import io
import json
import os

# Always resolve paths relative to this file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Device (CPU for laptop)
device = torch.device("cpu")

# Load class names safely
with open(os.path.join(BASE_DIR, "classes.json"), "r") as f:
    classes = json.load(f)

# Load model architecture
model = models.mobilenet_v2(weights=None)
model.classifier[1] = nn.Linear(model.last_channel, len(classes))

# Load trained weights safely
model.load_state_dict(
    torch.load(os.path.join(BASE_DIR, "crop_sense_model.pth"), map_location=device)
)

model.to(device)
model.eval()

# Transform
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
])


def predict_local(image_bytes: bytes):
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    image = transform(image).unsqueeze(0).to(device)

    with torch.no_grad():
        outputs = model(image)
        probabilities = torch.softmax(outputs, dim=1)
        confidence, predicted = torch.max(probabilities, 1)

    label = classes[predicted.item()]

    return {
        "label": label,
        "confidence": round(confidence.item() * 100, 2)
    }
