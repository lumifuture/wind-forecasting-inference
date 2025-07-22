# app/services/inference_engine.py

import torch
from app.schemas.request import ForecastRequest
from app.services.model_loader import load_model
from app.services.inference_pipeline import InferencePipeline
from app.predictors.factory import get_predictor
from app.utils.formats import postprocess_prediction


def extract_features(data_points):
    FEATURE_NAMES = [
        'wind_speed', 'wind_direction', 'cabin_angle', 'total_cabin_angle',
        'paddle1_angle', 'paddle2_angle', 'paddle3_angle', 'outdoor_temp',
        'wind_speed_100m', 'wind_direction_100m', 'temperature', 'air_pressure', 'air_density',
        'hour', 'dayofweek', 'month',
        'power_lag_1', 'power_lag_2', 'power_lag_3', 'power_lag_4'
    ]
    return [
        [getattr(dp, name, 0) if getattr(dp, name, None) is not None else 0 for name in FEATURE_NAMES]
        for dp in data_points
    ]


def run_forecast(request: ForecastRequest):
    """
    ┌──────────────────────────────────────┐
    │         run_forecast (main flow)     │
    ├──────────────────────────────────────┤
    │ 1. Load model + metadata + scalers   │
    │ 2. Preprocess input (scaler_x)       │
    │ 3. Get predictor class               │
    │ 4. Run prediction                    │
    │ 5. Postprocess (scaler_y, clip)      │
    │ 6. Return final output               │
    └──────────────────────────────────────┘
                │
                ▼
    ┌──────────────────────────────────────┐
    │          Predictor (pure logic)      │
    ├──────────────────────────────────────┤
    │ Only wraps: `output = model(input)`  │
    │ Possibly .squeeze() / reshape        │
    └──────────────────────────────────────┘
    """

    if request.level == "farm":
        if not request.farm_inputs:
            raise ValueError("'farm_inputs' is required for farm-level forecasts.")

        input_data = extract_features(request.farm_inputs)
        input_tensor = torch.tensor(input_data, dtype=torch.float32).unsqueeze(0)

        model, metadata, scaler_x, scaler_y = load_model(
            model_name=request.model_name,
            forecast_type=request.forecast_type,
            model_type=request.model_type,
            version=request.version,
            level="farm"
        )

        PredictorClass = get_predictor(metadata["model_type"])
        pipeline = InferencePipeline(model, metadata, PredictorClass, scaler_x, scaler_y)
        prediction = pipeline.run(input_tensor)
        # Post-process the prediction (format)
        last_historical_timestamp = request.farm_inputs[-1].time if request.farm_inputs else None
        forecast_points_list = postprocess_prediction(prediction, last_historical_timestamp, step_minutes=metadata.get("step_minutes", 15))
        return forecast_points_list

    elif request.level == "turbine":
        if not request.turbine_inputs:
            raise ValueError("'turbine_inputs' is required for turbine-level forecasts.")

        results = {}
        for tid, datapoints in request.turbine_inputs.items():
            input_data = extract_features(datapoints)
            input_tensor = torch.tensor(input_data, dtype=torch.float32).unsqueeze(0)
            model, metadata, scaler_x, scaler_y = load_model(
                model_name=request.model_name,
                forecast_type=request.forecast_type,
                model_type=request.model_type,
                version=request.version,
                level="turbine",
                turbine_id=tid
            )

            PredictorClass = get_predictor(metadata["model_type"])
            pipeline = InferencePipeline(model, metadata, PredictorClass, scaler_x, scaler_y)
            prediction = pipeline.run(input_tensor)
            # Post-process the prediction (format)
            last_historical_timestamp = datapoints[-1].time
            forecast_points_list = postprocess_prediction(prediction, last_historical_timestamp, step_minutes=metadata.get("step_minutes", 15))
            results[tid] = forecast_points_list

        return results

    else:
        raise ValueError("Invalid forecast level. Must be 'farm' or 'turbine'")