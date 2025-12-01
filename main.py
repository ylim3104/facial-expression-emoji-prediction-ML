import os

import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from emotion_model import EmotionModel
from preprocessing import decode_and_preprocess
from smoothing import Smoother
from fastapi.middleware.cors import CORSMiddleware
import threading  # For thread-safety

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Lazy init
model = None
smoother = None
model_lock = threading.Lock()

def load_components():
    global model, smoother
    with model_lock:
        if model is None:
            print("Loading model...")  # Logs to Cloud Run
            model = EmotionModel()
            smoother = Smoother()
            print("Model loaded.")
        return model, smoother

class ImageData(BaseModel):
    image: str

@app.get("/")
async def root():
    return {
        "message": "Facial expression emoji prediction API",
        "endpoints": {
            "/health": "GET - Health check",
            "/predict-cnn": "POST - predict cnn",
            "/warmup": "GET - warm up check"
        }
    }

@app.get("/health")
async def health_check():
    return {"status": "ok", "model_loaded": model is not None}

@app.post("/predict-cnn")
async def predict(data: ImageData):
    try:
        m, s = load_components()  # Lazy load here
        x = decode_and_preprocess(data.image)
        label, confidence = m.predict(x)
        stable_label = s.update(label)
        return {
            "emotion": stable_label,
            "confidence": confidence
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

# Optional: Warmup endpoint (ping this via cron for min-instances=1)
@app.get("/warmup")
async def warmup():
    load_components()
    return {"status": "warmed up"}

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port, reload=False)