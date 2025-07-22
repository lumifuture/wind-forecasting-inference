from datetime import datetime
from typing import List, Dict, Literal, Optional, Union
import pandas as pd
import torch


def postprocess_prediction(prediction: torch.Tensor, start_time: datetime, step_minutes: int = 15) -> List[Dict[str, Union[str, float]]]:
    """
    Format prediction into a list of ForecastPoint objects.

    Args:
        prediction (torch.Tensor): The real power forecast, shape (1, len(prediction)).
        start_time (datetime): The timestamp of the last historical data point.
        step_minutes (int): Interval between predictions in minutes (from metadata)

    Returns:
        List[Dict[str, Union[str, float]]]: A list of dictionaries, each representing a forecasted point.
    """

    # Generate timestamps for the forecast horizon
    forecast_points = []
    # The first forecast is for the step *after* the last historical data point.
    # Assuming each prediction step is 15 minutes.
    base_timestamp = pd.Timestamp(start_time)
    for i in range(len(prediction)):
        # Add (i+1) * step_minutes to the start_time (last historical time)
        forecast_timestamp = base_timestamp + pd.Timedelta(minutes=(i + 1) * step_minutes)
        forecast_points.append({
            "timestamp": forecast_timestamp.isoformat(), # ISO format for consistent JSON
            "forecasted_power_kw": max(0.0, float(prediction[i])) # Ensure non-negative power
        })
    return forecast_points