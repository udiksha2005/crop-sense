from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from backend.database.connection import get_db
from backend.services.prediction_service import process_prediction
from backend.services.database_service import get_prediction_history
from backend.core.exceptions import InvalidImageError
from backend.config.config import get_settings
from backend.utils.logger import error_logger

settings = get_settings()
router = APIRouter()

ALLOWED_TYPES = ["image/jpeg", "image/png", "image/jpg"]

@router.get("/health")
def health_check(db: Session = Depends(get_db)):
    db_status = "connected"
    try:
        db.execute(text("SELECT 1"))
    except Exception as e:
        error_logger.error(f"Health check database ping failed: {str(e)}")
        db_status = "disconnected"

    from backend.model_loader import model
    model_status = "loaded" if model is not None else "not loaded"
    overall_status = "healthy" if db_status == "connected" and model_status == "loaded" else "degraded"

    return {
        "status": overall_status,
        "database": db_status,
        "model": model_status,
        "version": settings.APP_VERSION
    }

@router.post("/predict")
async def predict(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if file.content_type not in ALLOWED_TYPES:
        raise InvalidImageError()
    return await process_prediction(file, db)

@router.get("/history")
def get_history(db: Session = Depends(get_db)):
    try:
        history = get_prediction_history(db)
        return history
    except Exception as e:
        error_logger.error(f"Error retrieving prediction history: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to retrieve prediction history.")
