from pydantic import BaseModel, UUID4
from typing import Optional, List, Dict, Any
from datetime import datetime

class PredictionCreate(BaseModel):
    filename: str
    image_path: Optional[str] = None
    crop_name: str
    disease_name: str
    confidence: float
    severity: Optional[str] = None
    model_version: Optional[str] = "1.0.0"
    processing_time: Optional[float] = None
    status: Optional[str] = "completed"

class PredictionResponse(BaseModel):
    id: UUID4
    filename: str
    crop_name: str
    disease_name: str
    confidence: float
    created_at: datetime
    
    class Config:
        from_attributes = True

# Old response format for backward compatibility
class OldPredictionResponse(BaseModel):
    filename: str
    plant: str
    health_status: str
    disease: str
    confidence: float
    solution: str
    top_predictions: List[Dict[str, Any]]
    healthy_probability: float
    diseased_probability: float
