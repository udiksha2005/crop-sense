from sqlalchemy.orm import Session
from backend.database import crud, schemas

def save_prediction_record(db: Session, prediction_data: schemas.PredictionCreate):
    return crud.create_prediction(db, prediction=prediction_data)

def get_prediction_history(db: Session, skip: int = 0, limit: int = 100):
    return crud.get_history(db, skip=skip, limit=limit)
