# app/utils/time.py

from datetime import datetime, timedelta

def generate_forecast_timestamps(start_time: datetime, interval_minutes: int, horizon: int):
    """
    Generate list of forecast timestamps.
    
    Args:
        start_time (datetime): time to start forecasting from
        interval_minutes (int): spacing between predictions
        horizon (int): number of steps to forecast

    Returns:
        List[datetime]: list of forecast timestamps
    """
    return [start_time + timedelta(minutes=i * interval_minutes) for i in range(1, horizon + 1)]