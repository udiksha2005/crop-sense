from fastapi import UploadFile
from sqlalchemy.orm import Session
from backend.services import storage_service, database_service
from backend.database import schemas
from backend.utils.logger import prediction_logger, error_logger
from backend.core.exceptions import PredictionError
import time

# Import existing AI logic (untouched)
from backend.leaf_detector import detect_leaf
from backend.image_processing import preprocess_image
from backend.model_loader import predict_local
from backend.solution import get_solution

async def process_prediction(file: UploadFile, db: Session) -> dict:
    start_time = time.time()
    try:
        contents = await file.read()
        
        # 1. Storage: Save original
        original_path = await storage_service.save_original_image(file, contents)
        
        # 2. AI Pipeline: Detect Leaf
        leaf_image_bytes = detect_leaf(contents)
        
        # 3. AI Pipeline: Preprocess
        processed_bytes = preprocess_image(leaf_image_bytes)
        
        # 4. Storage: Save processed
        processed_path = storage_service.save_processed_image(file.filename, processed_bytes)
        
        # 5. AI Pipeline: Inference
        result = predict_local(processed_bytes)
        
        confidence = result["confidence"]
        top_predictions = result["top_predictions"]
        healthy_probability = result["healthy_probability"]
        diseased_probability = result["diseased_probability"]
        label = result["label"]

        if confidence < 60:
            prediction_logger.info(f"Low confidence prediction for {file.filename}: {confidence}%")
            return {
                "filename": file.filename,
                "plant": "Unknown",
                "health_status": "Unknown",
                "disease": "Not detected",
                "confidence": confidence,
                "solution": "⚠️ Plant not recognized. Please upload a clearer crop image.",
                "top_predictions": top_predictions,
                "healthy_probability": healthy_probability,
                "diseased_probability": diseased_probability
            }

        # Clean label formatting (preserves old logic)
        clean_label = label.replace("___", "_")
        parts = clean_label.split("_")
        plant = parts[0]

        if "healthy" in label.lower():
            health_status = "Healthy"
            disease = "None"
        else:
            health_status = "Diseased"
            disease = " ".join(parts[1:])

        solution_text = get_solution(label)
        
        processing_time = time.time() - start_time

        # Save to database
        saved_to_history = False
        try:
            prediction_create = schemas.PredictionCreate(
                filename=file.filename,
                image_path=original_path,
                crop_name=plant,
                disease_name=disease,
                confidence=confidence,
                severity=None,
                processing_time=processing_time
            )
            database_service.save_prediction_record(db, prediction_create)
            saved_to_history = True
            prediction_logger.info(f"Successfully processed and saved prediction for {file.filename}")
        except Exception as db_err:
            error_logger.error(f"Failed to save prediction record to database for {file.filename}: {str(db_err)}", exc_info=True)
            saved_to_history = False

        return {
            "filename": file.filename,
            "plant": plant,
            "health_status": health_status,
            "disease": disease,
            "confidence": confidence,
            "solution": solution_text,
            "top_predictions": top_predictions,
            "healthy_probability": healthy_probability,
            "diseased_probability": diseased_probability,
            "saved_to_history": saved_to_history
        }
        
    except Exception as e:
        error_logger.error(f"Error processing prediction: {str(e)}", exc_info=True)
        raise PredictionError(detail="Failed to process image.")
