from sqlalchemy.orm import Session
from . import models, schemas
from uuid import UUID

# Prediction CRUD
def create_prediction(db: Session, prediction: schemas.PredictionCreate) -> models.Prediction:
    db_prediction = models.Prediction(**prediction.model_dump())
    try:
        db.add(db_prediction)
        db.commit()
        db.refresh(db_prediction)
        return db_prediction
    except Exception:
        db.rollback()
        raise

def get_history(db: Session, skip: int = 0, limit: int = 100):
    try:
        return db.query(models.Prediction).order_by(models.Prediction.created_at.desc()).offset(skip).limit(limit).all()
    except Exception:
        db.rollback()
        raise

# Placeholders
def create_user(db: Session):
    pass

def get_user(db: Session, user_id: UUID):
    pass

def get_prediction(db: Session, prediction_id: UUID):
    pass

def delete_prediction(db: Session, prediction_id: UUID):
    pass
