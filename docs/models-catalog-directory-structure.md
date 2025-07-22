# Models catalog directory Structure

## Directory Structure for  `wind-forecasting-inference` service

```
wind-forecasting-inference/
├── app/
│   ├── main.py
│   ├── api/
│   │   └── routes.py
│   ├── services/
│   │   ├── inference_engine.py
│   │   ├── model_loader.py
│   │   ├── forecast_router.py
│   │   └── postprocessing.py
│   ├── models/
│   │   ├── request.py
│   │   └── response.py
│   ├── config/
│   │   └── model_catalog.json
│   ├── registry/
│   │   └── model_registry.py
│   ├── predictors/
│   │   ├── base.py
│   │   ├── lstm_predictor.py
│   │   ├── cnn_lstm_predictor.py
│   │   └── transformer_predictor.py
│   └── utils/
│       └── time.py
├── models/
│   └── wind/
│       └── short_term/
│           └── lstm/
│               └── v1.0/
│                   ├── farm/
│                   │   ├── model.pt
│                   │   └── metadata.json
│                   └── turbines/
│                       ├── T1/
│                       │   ├── model.pt
│                       │   └── metadata.json
│                       ├── T2/
│                       │   ├── model.pt
│                       │   └── metadata.json
│                       └── shared_turbine_model/
│                           ├── model.pt
│                           └── metadata.json
├── tests/
│   ├── test_predict_endpoint.py
│   ├── test_model_loader.py
│   ├── test_forecast_router.py
│   └── test_inference_engine.py
├── Dockerfile
├── requirements.txt
└── README.md

```

## `model_catalog.json` with Per-Turbine Models

```json
{
  "wind_forecast": {
    "short_term": {
      "lstm": {
        "v1.0": {
          "farm": "models/wind/short_term/lstm/v1.0/farm/model.pt",
          "turbines": {
            "T1": "models/wind/short_term/lstm/v1.0/turbines/T1/model.pt",
            "T2": "models/wind/short_term/lstm/v1.0/turbines/T2/model.pt",
            "T3": "models/wind/short_term/lstm/v1.0/turbines/T3/model.pt"
          }
        }
      }
    }
  }
}
```

## Directory Layout (for turbine-level models)

```
models/
└── wind/
    └── short_term/
        └── lstm/
            └── v1.0/
                ├── farm/
                │   └── model.pt
                └── turbines/
                    ├── T1/
                    │   └── model.pt
                    ├── T2/
                    │   └── model.pt
                    └── T3/
                        └── model.pt
```

##  Optional: Shared Model for All Turbines

If you don’t train per-turbine models (i.e. one model works for all turbines), you can simplify:

```json
{
  "wind_forecast": {
    "short_term": {
      "lstm": {
        "v1.0": {
          "shared_turbine_model": "models/.../shared_turbine.pt"
        }
      }
    }
  }
}
```