#Crop Sense – AI Crop Disease Detection System

Crop Sense is an AI-powered system that helps farmers quickly identify crop leaf diseases using an image and receive instant treatment recommendations.

# How It Works

1. User uploads a crop leaf image.
2. Backend preprocesses the image (resize, RGB conversion).
3. A custom-trained MobileNetV2 model performs disease classification.
4. The system returns:
   - Predicted disease
   - Confidence score
   - Recommended treatment
5. Prediction is stored in the database for history tracking.
   
# Model Details

- Architecture: MobileNetV2 (Transfer Learning)
- Dataset: PlantVillage
- Framework: PyTorch
- Inference: Local (No third-party dependency)

# Trained Model Weights

The trained model file is not included in this repository to keep it lightweight.

Download the trained model from: https://drive.google.com/file/d/1OX7aMCOkSvTaNsT3ghYdF49iLw4PZa_Z/view?usp=sharing

After downloading, place the file inside: backend/

Expected structure:

crop-sense/
├── backend/
│   ├── crop_sense_model.pth
│   ├── main.py
│   ├── model_loader.py

# Tech Stack

- FastAPI
- PyTorch
- SQLAlchemy
- Pillow
- Python

# Features

- Custom-trained ML model
- Local inference (no external API dependency)
- Confidence scoring
- Disease → solution mapping
- Prediction history logging
- REST API architecture

# Future Improvements

- Cloud deployment
- Dockerization
- Improved model calibration
- Frontend UI enhancement
