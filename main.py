from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
import time
from model import CropVisionModel

app = FastAPI(
    title="Industrialized Crop-Health API",
    description="Containerized microservice for agricultural disease detection.",
    version="1.0.0"
)

# Load model on startup
vision_model = CropVisionModel()

class PredictionResponse(BaseModel):
    status: str
    diagnosis: str
    confidence: float
    latency_ms: float

@app.get("/health")
async def health_check():
    return {"status": "healthy", "model_loaded": vision_model.is_loaded}

@app.post("/predict", response_model=PredictionResponse)
async def predict_disease(file: UploadFile = File(...)):
    if not file.filename.endswith(('.jpg', '.jpeg', '.png')):
        raise HTTPException(status_code=400, detail="Only JPG/PNG images allowed.")
    
    start_time = time.time()
    
    try:
        contents = await file.read()
        result = vision_model.predict(contents)
        
        latency = round((time.time() - start_time) * 1000, 2)
        
        return PredictionResponse(
            status="success",
            diagnosis=result["diagnosis"],
            confidence=result["confidence"],
            latency_ms=latency
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
