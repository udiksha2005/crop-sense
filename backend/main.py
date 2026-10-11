from fastapi import FastAPI, UploadFile, File, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from backend.config.config import get_settings
from backend.database.connection import get_db, engine, Base
from backend.services.prediction_service import process_prediction
from backend.services.database_service import get_prediction_history
from backend.api.v1.router import router as api_v1_router
from backend.core.exceptions import InvalidImageError
from backend.utils.logger import app_logger, error_logger

settings = get_settings()

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app_logger.info("FastAPI application initialized.")

# Ensure database tables exist
try:
    Base.metadata.create_all(bind=engine)
    app_logger.info("Database tables verified.")
except Exception as e:
    error_logger.error(f"Database table verification failed: {str(e)}")

# Mount API v1
app.include_router(api_v1_router, prefix="/api/v1")

ALLOWED_TYPES = ["image/jpeg", "image/png", "image/jpg"]

# -------------------------------
# Backward compatible routes
# -------------------------------
@app.get("/")
def home():
    return {"status": "Crop Sense Backend Running"}

@app.get("/health")
def health_check(db: Session = Depends(get_db)):
    db_status = "connected"
    try:
        from sqlalchemy import text
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

@app.post("/predict")
async def predict(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if file.content_type not in ALLOWED_TYPES:
        raise InvalidImageError()
    return await process_prediction(file, db)

@app.get("/history")
def get_history(db: Session = Depends(get_db)):
    try:
        history = get_prediction_history(db)
        return history
    except Exception as e:
        error_logger.error(f"Error retrieving prediction history: {str(e)}", exc_info=True)
        from fastapi import HTTPException
        raise HTTPException(status_code=500, detail="Failed to retrieve prediction history.")
