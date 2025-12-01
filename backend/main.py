from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from image_processing import preprocess_image
from hf_api import predict_disease
from PIL import Image
import io

app = FastAPI()

# Allow frontend to call backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all (change later if needed)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "Backend running!"}

# -------------------------------
# NEW: Prediction API endpoint
# -------------------------------
@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    # Read uploaded image bytes
    contents = await file.read()
    image = Image.open(io.BytesIO(contents))

    # Step 1: preprocess image
    processed_image = preprocess_image(image)

    # Step 2: send to HuggingFace model
    result = predict_disease(processed_image)

    # Step 3: return structured result
    return {
        "filename": file.filename,
        "prediction": result.get("label"),
        "confidence": result.get("confidence")
    }
