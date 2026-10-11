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

# Load class names
with open(os.path.join(BASE_DIR, "classes.json"), "r") as f:
    classes = json.load(f)

# Load model architecture
model = models.mobilenet_v2(weights=None)
model.classifier[1] = nn.Linear(model.last_channel, len(classes))

# Load trained weights
model.load_state_dict(
    torch.load(os.path.join(BASE_DIR, "crop_sense_model.pth"), map_location=device)
)

model.to(device)
model.eval()

# Image transform
transform = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485,0.456,0.406],
        std=[0.229,0.224,0.225]
    )
])
def predict_local(image_bytes: bytes):
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    image = transform(image).unsqueeze(0).to(device)

    with torch.no_grad():
        outputs1 = model(image)  # original image
        outputs2 = model(torch.flip(image, dims=[3]))   # horizontal flip
        outputs3 = model(torch.flip(image, dims=[2]))   # vertical flip

        outputs = (outputs1 + outputs2 + outputs3) / 3

    probabilities = torch.softmax(outputs, dim=1)
    confidence, predicted = torch.max(probabilities, 1)

    # Get top 3 predictions
    top3_prob, top3_idx = torch.topk(probabilities, 3)

    top_predictions = []

    healthy_prob = 0
    diseased_prob = 0

    for i in range(len(classes)):
        label = classes[i]
        prob = probabilities[0][i].item() * 100

        if "healthy" in label.lower():
            healthy_prob += prob
        else:
            diseased_prob += prob

    for i in range(3):
        label = classes[top3_idx[0][i].item()]
        confidence = round(top3_prob[0][i].item() * 100, 2)

        top_predictions.append({
            "label": label,
            "confidence": confidence
        })

    best_prediction = top_predictions[0]

    return {
        "label": best_prediction["label"],
        "confidence": best_prediction["confidence"],
        "top_predictions": top_predictions,
        "healthy_probability": round(healthy_prob, 2),
        "diseased_probability": round(diseased_prob, 2)
    }