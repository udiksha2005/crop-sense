from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from dotenv import load_dotenv
import os

from sqlalchemy.orm import Session

from .image_processing import preprocess_image
from .model_loader import predict_local
from .solution import get_solution
from .db import SessionLocal, Prediction


# Load environment variables
load_dotenv()

app = FastAPI(title="Crop Sense API")


# -------------------------------
# CORS
# -------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


ALLOWED_TYPES = ["image/jpeg", "image/png", "image/jpg"]


# -------------------------------
# Home
# -------------------------------
@app.get("/")
def home():
    return {"status": "Crop Sense Backend Running"}


# -------------------------------
# Predict
# -------------------------------
@app.post("/predict")
async def predict(file: UploadFile = File(...)):

    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(
            status_code=400,
            detail="Only JPG/PNG images allowed"
        )

    try:
        # Read file
        contents = await file.read()

        # Preprocess image
        processed_bytes = preprocess_image(contents)

        # Local model prediction
        result = predict_local(processed_bytes)

        label = result["label"]
        confidence = result["confidence"]

        if confidence < 50:
         return {
        "filename": file.filename,
        "prediction": label,
        "confidence": confidence,
        "solution": "Low confidence prediction. Please upload a clearer image."
    }

        # Get solution
        solution_text = get_solution(label)

        # Save to database
        db: Session = SessionLocal()

        try:
            record = Prediction(
                filename=file.filename,
                label=label,
                confidence=confidence
            )
            db.add(record)
            db.commit()
        finally:
            db.close()

        return {
            "filename": file.filename,
            "prediction": label,
            "confidence": confidence,
            "solution": solution_text
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# -------------------------------
# History
# -------------------------------
@app.get("/history")
def get_history():

    db: Session = SessionLocal()

    try:
        records = db.query(Prediction).order_by(
            Prediction.created_at.desc()
        ).all()
        return records
    finally:
        db.close()
