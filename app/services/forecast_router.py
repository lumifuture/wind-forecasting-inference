# app/services/forecast_router.py

def route_forecast_level(level: str):
    if level == "farm":
        return "farm"
    elif level == "turbine":
        return "turbine"
    else:
        raise ValueError("Invalid forecast level. Expected 'farm' or 'turbine'.")
