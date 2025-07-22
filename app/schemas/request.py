# app/models/request.py

from pydantic import BaseModel, Field
from typing import List, Dict, Literal, Optional
from datetime import datetime


class WindDataPoint(BaseModel):
    """
    Represents a single historical wind data point from SCADA or NWP.
    Includes common features relevant for wind forecasting.
    """
    # Use str for timestamp in Pydantic for easier JSON serialization/deserialization
    # You'll parse it to datetime objects in your processing code.
    time: datetime = Field(..., description="Timestamp of the data point.")
    wind_speed: float = Field(..., description="Wind speed (m/s).")
    wind_direction: float = Field(..., description="Wind direction (degrees).")
    # SCADA specific
    cabin_angle: Optional[float] = Field(None, description="Cabin angle of the turbine.")
    total_cabin_angle: Optional[float] = Field(None, description="Total accumulated cabin angle.")
    paddle1_angle: Optional[float] = Field(None, description="Pitch angle of paddle 1.")
    paddle2_angle: Optional[float] = Field(None, description="Pitch angle of paddle 2.")
    paddle3_angle: Optional[float] = Field(None, description="Pitch angle of paddle 3.")
    outdoor_temp: Optional[float] = Field(None, description="Outdoor temperature (Celsius).")
    # NWP specific (could be optional if not always available or for different data sources)
    wind_speed_100m: Optional[float] = Field(None, description="NWP wind speed at 100m (m/s).")
    wind_direction_100m: Optional[float] = Field(None, description="NWP wind direction at 100m (degrees).")
    temperature: Optional[float] = Field(None, description="NWP temperature (Celsius).")
    air_pressure: Optional[float] = Field(None, description="NWP air pressure (hPa).")
    air_density: Optional[float] = Field(None, description="NWP air density (kg/m^3).")
    power: Optional[float] = Field(None, description="Actual power output for historical data points.")
    power_lag_1: Optional[float] = Field(None, description="Lag 1 (15-min) of actual power.")
    power_lag_2: Optional[float] = Field(None, description="Lag 2 (30-min) of actual power.")
    power_lag_3: Optional[float] = Field(None, description="Lag 3 (45-min) of actual power.")
    power_lag_4: Optional[float] = Field(None, description="Lag 4 (1-hour) of actual power.")


class ForecastRequest(BaseModel):
    """
    Represents an API request for a wind power forecast.
    Requires a sequence of historical data points to make a prediction.
    """
    model_name: str
    forecast_type: Literal["ultra_short_term", "short_term", "medium_term", "long_term"]
    model_type: Literal["lstm", "cnn_lstm", "transformer"]
    version: str
    level: Literal["farm", "turbine"]
    farm_inputs: Optional[List[WindDataPoint]] = Field(None, description="For farm-level forecasting.")
    turbine_inputs: Optional[Dict[str, List[WindDataPoint]]] = Field(None, description="For turbine-level forecasting. Keys are turbine IDs.")
    turbine_ids: Optional[List[str]] = None