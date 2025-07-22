# app/api/routes.py

from fastapi import APIRouter, HTTPException
from app.schemas.request import ForecastRequest
from app.schemas.response import ForecastResponse
from app.services.inference_engine import run_forecast

router = APIRouter()

@router.post("/predict", response_model=ForecastResponse)
def predict(request: ForecastRequest):
    # try:
    #     result = run_forecast(request)
    #     return ForecastResponse(predictions=result)
    # except ValueError as ve:
    #     raise HTTPException(status_code=400, detail=str(ve))
    # except Exception as e:
    #     raise HTTPException(status_code=500, detail=str(e))
    result = run_forecast(request)
    return ForecastResponse(predictions=result)
