# Wind Forecasting Inference Service

This microservice provides turbine-level and farm-level wind power forecasts using deep learning models such as **LSTM**, **CNN+LSTM**, and **Transformer**. It supports multiple forecast horizons, model versioning, and flexible input data formats (e.g., SCADA, NWP).

## Features

- Supports **ultra-short**, **short**, **medium**, and **long-term** forecasting
- Predicts at **turbine** or **farm** granularity
- Model-agnostic: LSTM, CNN+LSTM, Transformer
- Scalable, versioned model loading
- Input/output scaling via `scaler_x.pkl` and `scaler_y.pkl`
- Clean REST API with Swagger UI

## Project Structure

```bash
wind-forecasting-inference/
├── app/
│   ├── api/                  # FastAPI route handlers
│   ├── models/               # Pydantic request/response schemas
│   ├── predictors/           # LSTM, CNN+LSTM, Transformer wrappers
│   ├── services/             # Model loader, inference pipeline, postprocessing
│   ├── utils/                # Time, feature, and helper utils
├── models/                   # Saved PyTorch models and metadata
├── config/                   # model_catalog.json, logging configs, etc.
├── Dockerfile                # Container definition
├── requirements.txt
├── README.md
````

## Setup

### 1. Clone the repo

```bash
git clone https://github.com/your-org/wind-forecasting-inference.git
cd wind-forecasting-inference
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the service

```bash
uvicorn app.main:app --reload
```

## Model Structure

Each model should live in its own directory with:

```
models/
└── wind_forecast/
    └── short_term/
        └── lstm/
            └── v1/
                ├── model.pt
                ├── scaler_x.pkl
                ├── scaler_y.pkl
                └── metadata.json
```

The `metadata.json` must include:

```json
{
    "model_type": "lstm",
    "model_architecture": {
        "input_dim": 20,
        "hidden_dim": 128,
        "num_layers": 2,
        "pred_len": 16
    }
}
```

## API Documentation

Once the app is running, access:

* Swagger UI: [http://localhost:9000/docs](http://localhost:8000/docs)
* ReDoc: [http://localhost:9000/redoc](http://localhost:8000/redoc)

## Sample API Request

### Endpoint

```http
POST /api/predict
```

### JSON Request (Farm-Level)

```json
{
  "model_name": "wind_forecast",
  "forecast_type": "short_term",
  "model_type": "lstm",
  "version": "v1",
  "level": "farm",
  "farm_inputs": [
    {
      "time": "2025-07-22T12:00:00Z",
      "wind_speed": 8.1,
      "wind_direction": 210,
      "power": 230.4,
      "power_lag_1": 225.6
    }
    // ... at least 16 points
  ]
}
```

## Response (Simplified)

```json
{
  "predictions": [
    {
      "timestamp": "2025-07-22T12:15:00Z",
      "forecasted_power_kw": 243.8
    },
    ...
  ]
}
```

## Testing Locally

Use curl or Postman:

```bash
curl -X POST http://localhost:8000/api/predict \
     -H "Content-Type: application/json" \
     -d @sample_request.json
```

## Docker

### Build & Run

```bash
docker build -t wind-inference .
docker run -p 9000:9000 wind-inference
```

## Tech Stack

* FastAPI
* PyTorch
* Pydantic
* NumPy / Pandas
* Scikit-learn (for scalers)

## Related Repositories

* [`wind-forecasting-training`](https://github.com/lumifuture/wind-forecasting-training): Training pipelines
* [`wind-forecasting-models`](https://github.com/lumifuture/wind-forecasting-models): Saved models & metadata
* [`wind-forecasting-dev`](https://github.com/lumifuture/wind-forecasting-dev): DevOps, orchestration, dashboardsContributors

## License

[Apache License 2.0](https://github.com/lumifuture/wind-forecasting-inference/blob/main/LICENSE)

