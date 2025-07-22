# app/main.py

from fastapi import FastAPI
from app.api.routes import router as predict_router

app = FastAPI(
    title="Wind Forecasting Inference Service",
    description="Inference API for turbine and farm-level forecasting using multiple models.",
    version="1.0.0"
)

app.include_router(predict_router, prefix="/api")

@app.get("/")
def read_root():
    return {"status": "wind-forecasting-inference is running"}
