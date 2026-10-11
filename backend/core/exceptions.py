from fastapi import HTTPException, status

class PredictionError(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail)

class InvalidImageError(HTTPException):
    def __init__(self, detail: str = "Only JPG/PNG images allowed"):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)

class ModelLoadError(HTTPException):
    def __init__(self, detail: str = "Failed to load ML models"):
        super().__init__(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail)
