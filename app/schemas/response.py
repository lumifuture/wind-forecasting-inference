# app/models/response.py

from pydantic import BaseModel, Field
from typing import List, Dict, Union
from datetime import datetime

class ForecastPoint(BaseModel):
    """
    Represents a single forecasted wind power value for a specific future timestamp.
    """
    timestamp: datetime = Field(..., description="Timestamp of the forecasted point.")
    forecasted_power_kw: float = Field(..., description="Forecasted wind power in kilowatts (kW).")
    # You might add prediction intervals or other metadata here

class ForecastResponse(BaseModel):
    """
    Represents the complete response for a wind power forecast request.
    """
    predictions: Union[List[ForecastPoint], Dict[str, List[ForecastPoint]]]
    # - If farm: List[ForecastPoint]
    # - If turbine: Dict[turbine_id -> List[ForecastPoint]]
