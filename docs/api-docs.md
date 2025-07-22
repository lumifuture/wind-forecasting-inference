# Wind Forecasting Inference API

This service provides ultra-short to long-term wind power forecasts at both **farm** and **turbine** levels using multiple model architectures (LSTM, CNN+LSTM, Transformer).

## Base URL
[http://localhost:8000/api](http://localhost:8000/api)

## Health Check

### `GET /`

Returns a simple status message to confirm the service is running.

**Response:**
```json
{
  "status": "wind-forecasting-inference is running"
}
````

---

## Predict Wind Power

### `POST /predict`

Generates wind power forecasts using historical SCADA and/or NWP data.

### Request Body

#### Fields

| Field            | Type                                                                 | Description                                                                    |
| ---------------- | -------------------------------------------------------------------- | ------------------------------------------------------------------------------ |
| `model_name`     | `string`                                                             | Logical model group name (e.g., `"wind_forecast"`).                            |
| `forecast_type`  | `"ultra_short_term"`, `"short_term"`, `"medium_term"`, `"long_term"` | Type of forecast horizon.                                                      |
| `model_type`     | `"lstm"`, `"cnn_lstm"`, `"transformer"`                              | Model architecture to use.                                                     |
| `version`        | `string`                                                             | Specific version identifier of the model.                                      |
| `level`          | `"farm"` or `"turbine"`                                              | Forecasting granularity.                                                       |
| `farm_inputs`    | `List[WindDataPoint]`                                                | Historical input data for farm-level forecasts (required if `level = "farm"`). |
| `turbine_inputs` | `Dict[str, List[WindDataPoint]]`                                     | Turbine-specific data (required if `level = "turbine"`).                       |

#### `WindDataPoint` schema includes:

* `time`: Timestamp (ISO 8601)
* `wind_speed`, `wind_direction`, `cabin_angle`, `paddle1_angle`, ...
* Optional NWP features and lag features (`power_lag_1`, etc.)

### Sample Request (Farm-Level)

```json
{
  "model_name": "wind_forecast",
  "forecast_type": "ultra_short_term",
  "model_type": "lstm",
  "version": "v1.0",
  "level": "farm",
  "farm_inputs": [
    {
      "time": "2025-07-18T05:00:00",
      "wind_speed": 6.5,
      "wind_direction": 270.0,
      "cabin_angle": 110.0,
      "total_cabin_angle": 12500.0,
      "paddle1_angle": 1.0,
      "paddle2_angle": 1.1,
      "paddle3_angle": 0.9,
      "outdoor_temp": 15.0,
      "wind_speed_100m": 7.0,
      "wind_direction_100m": 268.0,
      "temperature": 14.5,
      "air_pressure": 1015.0,
      "air_density": 1.25,
      "power": 1000.0,
      "power_lag_1": 980.0,
      "power_lag_2": 960.0,
      "power_lag_3": 940.0,
      "power_lag_4": 920.0
    },
    {
      "time": "2025-07-18T05:15:00",
      "wind_speed": 6.8,
      "wind_direction": 272.0,
      "cabin_angle": 110.1,
      "total_cabin_angle": 12501.0,
      "paddle1_angle": 1.05,
      "paddle2_angle": 1.15,
      "paddle3_angle": 0.95,
      "outdoor_temp": 15.2,
      "wind_speed_100m": 7.2,
      "wind_direction_100m": 270.0,
      "temperature": 14.7,
      "air_pressure": 1015.1,
      "air_density": 1.25,
      "power": 1050.0,
      "power_lag_1": 1000.0,
      "power_lag_2": 980.0,
      "power_lag_3": 960.0,
      "power_lag_4": 940.0
    },
    {
      "time": "2025-07-18T05:30:00",
      "wind_speed": 7.0,
      "wind_direction": 275.0,
      "cabin_angle": 110.2,
      "total_cabin_angle": 12502.0,
      "paddle1_angle": 1.1,
      "paddle2_angle": 1.2,
      "paddle3_angle": 1.0,
      "outdoor_temp": 15.4,
      "wind_speed_100m": 7.4,
      "wind_direction_100m": 273.0,
      "temperature": 14.9,
      "air_pressure": 1015.2,
      "air_density": 1.25,
      "power": 1100.0,
      "power_lag_1": 1050.0,
      "power_lag_2": 1000.0,
      "power_lag_3": 980.0,
      "power_lag_4": 960.0
    },
    {
      "time": "2025-07-18T05:45:00",
      "wind_speed": 7.2,
      "wind_direction": 278.0,
      "cabin_angle": 110.3,
      "total_cabin_angle": 12503.0,
      "paddle1_angle": 1.15,
      "paddle2_angle": 1.25,
      "paddle3_angle": 1.05,
      "outdoor_temp": 15.6,
      "wind_speed_100m": 7.6,
      "wind_direction_100m": 276.0,
      "temperature": 15.1,
      "air_pressure": 1015.3,
      "air_density": 1.25,
      "power": 1150.0,
      "power_lag_1": 1100.0,
      "power_lag_2": 1050.0,
      "power_lag_3": 1000.0,
      "power_lag_4": 980.0
    },
    {
      "time": "2025-07-18T06:00:00",
      "wind_speed": 7.5,
      "wind_direction": 280.0,
      "cabin_angle": 110.4,
      "total_cabin_angle": 12504.0,
      "paddle1_angle": 1.2,
      "paddle2_angle": 1.3,
      "paddle3_angle": 1.1,
      "outdoor_temp": 15.8,
      "wind_speed_100m": 7.8,
      "wind_direction_100m": 278.0,
      "temperature": 15.3,
      "air_pressure": 1015.4,
      "air_density": 1.24,
      "power": 1200.0,
      "power_lag_1": 1150.0,
      "power_lag_2": 1100.0,
      "power_lag_3": 1050.0,
      "power_lag_4": 1000.0
    },
    {
      "time": "2025-07-18T06:15:00",
      "wind_speed": 7.7,
      "wind_direction": 282.0,
      "cabin_angle": 110.5,
      "total_cabin_angle": 12505.0,
      "paddle1_angle": 1.25,
      "paddle2_angle": 1.35,
      "paddle3_angle": 1.15,
      "outdoor_temp": 16.0,
      "wind_speed_100m": 8.0,
      "wind_direction_100m": 280.0,
      "temperature": 15.5,
      "air_pressure": 1015.5,
      "air_density": 1.24,
      "power": 1250.0,
      "power_lag_1": 1200.0,
      "power_lag_2": 1150.0,
      "power_lag_3": 1100.0,
      "power_lag_4": 1050.0
    },
    {
      "time": "2025-07-18T06:30:00",
      "wind_speed": 8.0,
      "wind_direction": 285.0,
      "cabin_angle": 110.6,
      "total_cabin_angle": 12506.0,
      "paddle1_angle": 1.3,
      "paddle2_angle": 1.4,
      "paddle3_angle": 1.2,
      "outdoor_temp": 16.2,
      "wind_speed_100m": 8.3,
      "wind_direction_100m": 283.0,
      "temperature": 15.7,
      "air_pressure": 1015.6,
      "air_density": 1.24,
      "power": 1300.0,
      "power_lag_1": 1250.0,
      "power_lag_2": 1200.0,
      "power_lag_3": 1150.0,
      "power_lag_4": 1100.0
    },
    {
      "time": "2025-07-18T06:45:00",
      "wind_speed": 8.2,
      "wind_direction": 288.0,
      "cabin_angle": 110.7,
      "total_cabin_angle": 12507.0,
      "paddle1_angle": 1.35,
      "paddle2_angle": 1.45,
      "paddle3_angle": 1.25,
      "outdoor_temp": 16.4,
      "wind_speed_100m": 8.5,
      "wind_direction_100m": 286.0,
      "temperature": 15.9,
      "air_pressure": 1015.7,
      "air_density": 1.24,
      "power": 1350.0,
      "power_lag_1": 1300.0,
      "power_lag_2": 1250.0,
      "power_lag_3": 1200.0,
      "power_lag_4": 1150.0
    },
    {
      "time": "2025-07-18T07:00:00",
      "wind_speed": 8.5,
      "wind_direction": 290.0,
      "cabin_angle": 110.8,
      "total_cabin_angle": 12508.0,
      "paddle1_angle": 1.4,
      "paddle2_angle": 1.5,
      "paddle3_angle": 1.3,
      "outdoor_temp": 16.6,
      "wind_speed_100m": 8.8,
      "wind_direction_100m": 288.0,
      "temperature": 16.1,
      "air_pressure": 1015.8,
      "air_density": 1.23,
      "power": 1400.0,
      "power_lag_1": 1350.0,
      "power_lag_2": 1300.0,
      "power_lag_3": 1250.0,
      "power_lag_4": 1200.0
    },
    {
      "time": "2025-07-18T07:15:00",
      "wind_speed": 8.7,
      "wind_direction": 292.0,
      "cabin_angle": 110.9,
      "total_cabin_angle": 12509.0,
      "paddle1_angle": 1.45,
      "paddle2_angle": 1.55,
      "paddle3_angle": 1.35,
      "outdoor_temp": 16.8,
      "wind_speed_100m": 9.0,
      "wind_direction_100m": 290.0,
      "temperature": 16.3,
      "air_pressure": 1015.9,
      "air_density": 1.23,
      "power": 1450.0,
      "power_lag_1": 1400.0,
      "power_lag_2": 1350.0,
      "power_lag_3": 1300.0,
      "power_lag_4": 1250.0
    },
    {
      "time": "2025-07-18T07:30:00",
      "wind_speed": 9.0,
      "wind_direction": 295.0,
      "cabin_angle": 111.0,
      "total_cabin_angle": 12510.0,
      "paddle1_angle": 1.5,
      "paddle2_angle": 1.6,
      "paddle3_angle": 1.4,
      "outdoor_temp": 17.0,
      "wind_speed_100m": 9.3,
      "wind_direction_100m": 293.0,
      "temperature": 16.5,
      "air_pressure": 1016.0,
      "air_density": 1.23,
      "power": 1500.0,
      "power_lag_1": 1450.0,
      "power_lag_2": 1400.0,
      "power_lag_3": 1350.0,
      "power_lag_4": 1300.0
    },
    {
      "time": "2025-07-18T07:45:00",
      "wind_speed": 9.2,
      "wind_direction": 298.0,
      "cabin_angle": 111.1,
      "total_cabin_angle": 12511.0,
      "paddle1_angle": 1.55,
      "paddle2_angle": 1.65,
      "paddle3_angle": 1.45,
      "outdoor_temp": 17.2,
      "wind_speed_100m": 9.5,
      "wind_direction_100m": 296.0,
      "temperature": 16.7,
      "air_pressure": 1016.1,
      "air_density": 1.23,
      "power": 1550.0,
      "power_lag_1": 1500.0,
      "power_lag_2": 1450.0,
      "power_lag_3": 1400.0,
      "power_lag_4": 1350.0
    },
    {
      "time": "2025-07-18T08:00:00",
      "wind_speed": 9.5,
      "wind_direction": 300.0,
      "cabin_angle": 111.2,
      "total_cabin_angle": 12512.0,
      "paddle1_angle": 1.6,
      "paddle2_angle": 1.7,
      "paddle3_angle": 1.5,
      "outdoor_temp": 17.4,
      "wind_speed_100m": 9.8,
      "wind_direction_100m": 298.0,
      "temperature": 16.9,
      "air_pressure": 1016.2,
      "air_density": 1.22,
      "power": 1600.0,
      "power_lag_1": 1550.0,
      "power_lag_2": 1500.0,
      "power_lag_3": 1450.0,
      "power_lag_4": 1400.0
    },
    {
      "time": "2025-07-18T08:15:00",
      "wind_speed": 9.7,
      "wind_direction": 302.0,
      "cabin_angle": 111.3,
      "total_cabin_angle": 12513.0,
      "paddle1_angle": 1.65,
      "paddle2_angle": 1.75,
      "paddle3_angle": 1.55,
      "outdoor_temp": 17.6,
      "wind_speed_100m": 10.0,
      "wind_direction_100m": 300.0,
      "temperature": 17.1,
      "air_pressure": 1016.3,
      "air_density": 1.22,
      "power": 1650.0,
      "power_lag_1": 1600.0,
      "power_lag_2": 1550.0,
      "power_lag_3": 1500.0,
      "power_lag_4": 1450.0
    },
    {
      "time": "2025-07-18T08:30:00",
      "wind_speed": 10.0,
      "wind_direction": 305.0,
      "cabin_angle": 111.4,
      "total_cabin_angle": 12514.0,
      "paddle1_angle": 1.7,
      "paddle2_angle": 1.8,
      "paddle3_angle": 1.6,
      "outdoor_temp": 17.8,
      "wind_speed_100m": 10.3,
      "wind_direction_100m": 303.0,
      "temperature": 17.3,
      "air_pressure": 1016.4,
      "air_density": 1.22,
      "power": 1700.0,
      "power_lag_1": 1650.0,
      "power_lag_2": 1600.0,
      "power_lag_3": 1550.0,
      "power_lag_4": 1500.0
    },
    {
      "time": "2025-07-18T08:45:00",
      "wind_speed": 10.2,
      "wind_direction": 308.0,
      "cabin_angle": 111.5,
      "total_cabin_angle": 12515.0,
      "paddle1_angle": 1.75,
      "paddle2_angle": 1.85,
      "paddle3_angle": 1.65,
      "outdoor_temp": 18.0,
      "wind_speed_100m": 10.5,
      "wind_direction_100m": 306.0,
      "temperature": 17.5,
      "air_pressure": 1016.5,
      "air_density": 1.22,
      "power": 1750.0,
      "power_lag_1": 1700.0,
      "power_lag_2": 1650.0,
      "power_lag_3": 1600.0,
      "power_lag_4": 1550.0
    },
    {
      "time": "2025-07-18T09:00:00",
      "wind_speed": 10.5,
      "wind_direction": 310.0,
      "cabin_angle": 111.6,
      "total_cabin_angle": 12516.0,
      "paddle1_angle": 1.8,
      "paddle2_angle": 1.9,
      "paddle3_angle": 1.7,
      "outdoor_temp": 18.2,
      "wind_speed_100m": 10.8,
      "wind_direction_100m": 308.0,
      "temperature": 17.7,
      "air_pressure": 1016.6,
      "air_density": 1.21,
      "power": 1800.0,
      "power_lag_1": 1750.0,
      "power_lag_2": 1700.0,
      "power_lag_3": 1650.0,
      "power_lag_4": 1600.0
    }
  ]
}
```

---

### Sample Response (Farm-Level)

```json
{
  "predictions": [
    {
      "timestamp": "2025-07-18T09:15:00",
      "forecasted_power_kw": 819.118028913275
    },
    {
      "timestamp": "2025-07-18T09:30:00",
      "forecasted_power_kw": 1033.62637771335
    },
    {
      "timestamp": "2025-07-18T09:45:00",
      "forecasted_power_kw": 1256.3594688792061
    },
    {
      "timestamp": "2025-07-18T10:00:00",
      "forecasted_power_kw": 1446.8185161887793
    },
    {
      "timestamp": "2025-07-18T10:15:00",
      "forecasted_power_kw": 1525.3419857305098
    },
    {
      "timestamp": "2025-07-18T10:30:00",
      "forecasted_power_kw": 1541.5937664790167
    },
    {
      "timestamp": "2025-07-18T10:45:00",
      "forecasted_power_kw": 1535.524382534582
    },
    {
      "timestamp": "2025-07-18T11:00:00",
      "forecasted_power_kw": 1534.9523446006936
    },
    {
      "timestamp": "2025-07-18T11:15:00",
      "forecasted_power_kw": 1512.9870740952188
    },
    {
      "timestamp": "2025-07-18T11:30:00",
      "forecasted_power_kw": 1524.479302002605
    },
    {
      "timestamp": "2025-07-18T11:45:00",
      "forecasted_power_kw": 1476.006027346164
    },
    {
      "timestamp": "2025-07-18T12:00:00",
      "forecasted_power_kw": 1406.6417841488835
    },
    {
      "timestamp": "2025-07-18T12:15:00",
      "forecasted_power_kw": 1276.9928886372002
    },
    {
      "timestamp": "2025-07-18T12:30:00",
      "forecasted_power_kw": 1133.332373446366
    },
    {
      "timestamp": "2025-07-18T12:45:00",
      "forecasted_power_kw": 996.3458367856599
    },
    {
      "timestamp": "2025-07-18T13:00:00",
      "forecasted_power_kw": 880.3138284362253
    }
  ]
}
```

### Sample Request (Turbine-Level) 

```
{
  "model_name": "wind_forecast",
  "forecast_type": "ultra_short_term",
  "model_type": "lstm",
  "version": "v1.0",
  "level": "turbine",
  "turbine_inputs": {
    "T1": [
      {
        "time": "2025-07-18T05:00:00",
        "wind_speed": 6.5,
        "wind_direction": 270,
        "cabin_angle": 110,
        "total_cabin_angle": 12500,
        "paddle1_angle": 1,
        "paddle2_angle": 1.1,
        "paddle3_angle": 0.9,
        "outdoor_temp": 15,
        "wind_speed_100m": 7,
        "wind_direction_100m": 268,
        "temperature": 14.5,
        "air_pressure": 1015,
        "air_density": 1.25,
        "power": 1000,
        "power_lag_1": 980,
        "power_lag_2": 960,
        "power_lag_3": 940,
        "power_lag_4": 920
      },
      {
        "time": "2025-07-18T05:15:00",
        "wind_speed": 6.8,
        "wind_direction": 272,
        "cabin_angle": 110.1,
        "total_cabin_angle": 12501,
        "paddle1_angle": 1.05,
        "paddle2_angle": 1.15,
        "paddle3_angle": 0.95,
        "outdoor_temp": 15.2,
        "wind_speed_100m": 7.2,
        "wind_direction_100m": 270,
        "temperature": 14.7,
        "air_pressure": 1015.1,
        "air_density": 1.25,
        "power": 1050,
        "power_lag_1": 1000,
        "power_lag_2": 980,
        "power_lag_3": 960,
        "power_lag_4": 940
      },
      {
        "time": "2025-07-18T05:30:00",
        "wind_speed": 7,
        "wind_direction": 275,
        "cabin_angle": 110.2,
        "total_cabin_angle": 12502,
        "paddle1_angle": 1.1,
        "paddle2_angle": 1.2,
        "paddle3_angle": 1,
        "outdoor_temp": 15.4,
        "wind_speed_100m": 7.4,
        "wind_direction_100m": 273,
        "temperature": 14.9,
        "air_pressure": 1015.2,
        "air_density": 1.25,
        "power": 1100,
        "power_lag_1": 1050,
        "power_lag_2": 1000,
        "power_lag_3": 980,
        "power_lag_4": 960
      },
      {
        "time": "2025-07-18T05:45:00",
        "wind_speed": 7.2,
        "wind_direction": 278,
        "cabin_angle": 110.3,
        "total_cabin_angle": 12503,
        "paddle1_angle": 1.15,
        "paddle2_angle": 1.25,
        "paddle3_angle": 1.05,
        "outdoor_temp": 15.6,
        "wind_speed_100m": 7.6,
        "wind_direction_100m": 276,
        "temperature": 15.1,
        "air_pressure": 1015.3,
        "air_density": 1.25,
        "power": 1150,
        "power_lag_1": 1100,
        "power_lag_2": 1050,
        "power_lag_3": 1000,
        "power_lag_4": 980
      },
      {
        "time": "2025-07-18T06:00:00",
        "wind_speed": 7.5,
        "wind_direction": 280,
        "cabin_angle": 110.4,
        "total_cabin_angle": 12504,
        "paddle1_angle": 1.2,
        "paddle2_angle": 1.3,
        "paddle3_angle": 1.1,
        "outdoor_temp": 15.8,
        "wind_speed_100m": 7.8,
        "wind_direction_100m": 278,
        "temperature": 15.3,
        "air_pressure": 1015.4,
        "air_density": 1.24,
        "power": 1200,
        "power_lag_1": 1150,
        "power_lag_2": 1100,
        "power_lag_3": 1050,
        "power_lag_4": 1000
      },
      {
        "time": "2025-07-18T06:15:00",
        "wind_speed": 7.7,
        "wind_direction": 282,
        "cabin_angle": 110.5,
        "total_cabin_angle": 12505,
        "paddle1_angle": 1.25,
        "paddle2_angle": 1.35,
        "paddle3_angle": 1.15,
        "outdoor_temp": 16,
        "wind_speed_100m": 8,
        "wind_direction_100m": 280,
        "temperature": 15.5,
        "air_pressure": 1015.5,
        "air_density": 1.24,
        "power": 1250,
        "power_lag_1": 1200,
        "power_lag_2": 1150,
        "power_lag_3": 1100,
        "power_lag_4": 1050
      },
      {
        "time": "2025-07-18T06:30:00",
        "wind_speed": 8,
        "wind_direction": 285,
        "cabin_angle": 110.6,
        "total_cabin_angle": 12506,
        "paddle1_angle": 1.3,
        "paddle2_angle": 1.4,
        "paddle3_angle": 1.2,
        "outdoor_temp": 16.2,
        "wind_speed_100m": 8.3,
        "wind_direction_100m": 283,
        "temperature": 15.7,
        "air_pressure": 1015.6,
        "air_density": 1.24,
        "power": 1300,
        "power_lag_1": 1250,
        "power_lag_2": 1200,
        "power_lag_3": 1150,
        "power_lag_4": 1100
      },
      {
        "time": "2025-07-18T06:45:00",
        "wind_speed": 8.2,
        "wind_direction": 288,
        "cabin_angle": 110.7,
        "total_cabin_angle": 12507,
        "paddle1_angle": 1.35,
        "paddle2_angle": 1.45,
        "paddle3_angle": 1.25,
        "outdoor_temp": 16.4,
        "wind_speed_100m": 8.5,
        "wind_direction_100m": 286,
        "temperature": 15.9,
        "air_pressure": 1015.7,
        "air_density": 1.24,
        "power": 1350,
        "power_lag_1": 1300,
        "power_lag_2": 1250,
        "power_lag_3": 1200,
        "power_lag_4": 1150
      },
      {
        "time": "2025-07-18T07:00:00",
        "wind_speed": 8.5,
        "wind_direction": 290,
        "cabin_angle": 110.8,
        "total_cabin_angle": 12508,
        "paddle1_angle": 1.4,
        "paddle2_angle": 1.5,
        "paddle3_angle": 1.3,
        "outdoor_temp": 16.6,
        "wind_speed_100m": 8.8,
        "wind_direction_100m": 288,
        "temperature": 16.1,
        "air_pressure": 1015.8,
        "air_density": 1.23,
        "power": 1400,
        "power_lag_1": 1350,
        "power_lag_2": 1300,
        "power_lag_3": 1250,
        "power_lag_4": 1200
      },
      {
        "time": "2025-07-18T07:15:00",
        "wind_speed": 8.7,
        "wind_direction": 292,
        "cabin_angle": 110.9,
        "total_cabin_angle": 12509,
        "paddle1_angle": 1.45,
        "paddle2_angle": 1.55,
        "paddle3_angle": 1.35,
        "outdoor_temp": 16.8,
        "wind_speed_100m": 9,
        "wind_direction_100m": 290,
        "temperature": 16.3,
        "air_pressure": 1015.9,
        "air_density": 1.23,
        "power": 1450,
        "power_lag_1": 1400,
        "power_lag_2": 1350,
        "power_lag_3": 1300,
        "power_lag_4": 1250
      },
      {
        "time": "2025-07-18T07:30:00",
        "wind_speed": 9,
        "wind_direction": 295,
        "cabin_angle": 111,
        "total_cabin_angle": 12510,
        "paddle1_angle": 1.5,
        "paddle2_angle": 1.6,
        "paddle3_angle": 1.4,
        "outdoor_temp": 17,
        "wind_speed_100m": 9.3,
        "wind_direction_100m": 293,
        "temperature": 16.5,
        "air_pressure": 1016,
        "air_density": 1.23,
        "power": 1500,
        "power_lag_1": 1450,
        "power_lag_2": 1400,
        "power_lag_3": 1350,
        "power_lag_4": 1300
      },
      {
        "time": "2025-07-18T07:45:00",
        "wind_speed": 9.2,
        "wind_direction": 298,
        "cabin_angle": 111.1,
        "total_cabin_angle": 12511,
        "paddle1_angle": 1.55,
        "paddle2_angle": 1.65,
        "paddle3_angle": 1.45,
        "outdoor_temp": 17.2,
        "wind_speed_100m": 9.5,
        "wind_direction_100m": 296,
        "temperature": 16.7,
        "air_pressure": 1016.1,
        "air_density": 1.23,
        "power": 1550,
        "power_lag_1": 1500,
        "power_lag_2": 1450,
        "power_lag_3": 1400,
        "power_lag_4": 1350
      },
      {
        "time": "2025-07-18T08:00:00",
        "wind_speed": 9.5,
        "wind_direction": 300,
        "cabin_angle": 111.2,
        "total_cabin_angle": 12512,
        "paddle1_angle": 1.6,
        "paddle2_angle": 1.7,
        "paddle3_angle": 1.5,
        "outdoor_temp": 17.4,
        "wind_speed_100m": 9.8,
        "wind_direction_100m": 298,
        "temperature": 16.9,
        "air_pressure": 1016.2,
        "air_density": 1.22,
        "power": 1600,
        "power_lag_1": 1550,
        "power_lag_2": 1500,
        "power_lag_3": 1450,
        "power_lag_4": 1400
      },
      {
        "time": "2025-07-18T08:15:00",
        "wind_speed": 9.7,
        "wind_direction": 302,
        "cabin_angle": 111.3,
        "total_cabin_angle": 12513,
        "paddle1_angle": 1.65,
        "paddle2_angle": 1.75,
        "paddle3_angle": 1.55,
        "outdoor_temp": 17.6,
        "wind_speed_100m": 10,
        "wind_direction_100m": 300,
        "temperature": 17.1,
        "air_pressure": 1016.3,
        "air_density": 1.22,
        "power": 1650,
        "power_lag_1": 1600,
        "power_lag_2": 1550,
        "power_lag_3": 1500,
        "power_lag_4": 1450
      },
      {
        "time": "2025-07-18T08:30:00",
        "wind_speed": 10,
        "wind_direction": 305,
        "cabin_angle": 111.4,
        "total_cabin_angle": 12514,
        "paddle1_angle": 1.7,
        "paddle2_angle": 1.8,
        "paddle3_angle": 1.6,
        "outdoor_temp": 17.8,
        "wind_speed_100m": 10.3,
        "wind_direction_100m": 303,
        "temperature": 17.3,
        "air_pressure": 1016.4,
        "air_density": 1.22,
        "power": 1700,
        "power_lag_1": 1650,
        "power_lag_2": 1600,
        "power_lag_3": 1550,
        "power_lag_4": 1500
      },
      {
        "time": "2025-07-18T08:45:00",
        "wind_speed": 10.2,
        "wind_direction": 308,
        "cabin_angle": 111.5,
        "total_cabin_angle": 12515,
        "paddle1_angle": 1.75,
        "paddle2_angle": 1.85,
        "paddle3_angle": 1.65,
        "outdoor_temp": 18,
        "wind_speed_100m": 10.5,
        "wind_direction_100m": 306,
        "temperature": 17.5,
        "air_pressure": 1016.5,
        "air_density": 1.22,
        "power": 1750,
        "power_lag_1": 1700,
        "power_lag_2": 1650,
        "power_lag_3": 1600,
        "power_lag_4": 1550
      },
      {
        "time": "2025-07-18T09:00:00",
        "wind_speed": 10.5,
        "wind_direction": 310,
        "cabin_angle": 111.6,
        "total_cabin_angle": 12516,
        "paddle1_angle": 1.8,
        "paddle2_angle": 1.9,
        "paddle3_angle": 1.7,
        "outdoor_temp": 18.2,
        "wind_speed_100m": 10.8,
        "wind_direction_100m": 308,
        "temperature": 17.7,
        "air_pressure": 1016.6,
        "air_density": 1.21,
        "power": 1800,
        "power_lag_1": 1750,
        "power_lag_2": 1700,
        "power_lag_3": 1650,
        "power_lag_4": 1600
      }
    ],
    "T2": [
      {
        "time": "2025-07-18T05:00:00",
        "wind_speed": 6.5,
        "wind_direction": 270,
        "cabin_angle": 110,
        "total_cabin_angle": 12500,
        "paddle1_angle": 1,
        "paddle2_angle": 1.1,
        "paddle3_angle": 0.9,
        "outdoor_temp": 15,
        "wind_speed_100m": 7,
        "wind_direction_100m": 268,
        "temperature": 14.5,
        "air_pressure": 1015,
        "air_density": 1.25,
        "power": 1000,
        "power_lag_1": 980,
        "power_lag_2": 960,
        "power_lag_3": 940,
        "power_lag_4": 920
      },
      {
        "time": "2025-07-18T05:15:00",
        "wind_speed": 6.8,
        "wind_direction": 272,
        "cabin_angle": 110.1,
        "total_cabin_angle": 12501,
        "paddle1_angle": 1.05,
        "paddle2_angle": 1.15,
        "paddle3_angle": 0.95,
        "outdoor_temp": 15.2,
        "wind_speed_100m": 7.2,
        "wind_direction_100m": 270,
        "temperature": 14.7,
        "air_pressure": 1015.1,
        "air_density": 1.25,
        "power": 1050,
        "power_lag_1": 1000,
        "power_lag_2": 980,
        "power_lag_3": 960,
        "power_lag_4": 940
      },
      {
        "time": "2025-07-18T05:30:00",
        "wind_speed": 7,
        "wind_direction": 275,
        "cabin_angle": 110.2,
        "total_cabin_angle": 12502,
        "paddle1_angle": 1.1,
        "paddle2_angle": 1.2,
        "paddle3_angle": 1,
        "outdoor_temp": 15.4,
        "wind_speed_100m": 7.4,
        "wind_direction_100m": 273,
        "temperature": 14.9,
        "air_pressure": 1015.2,
        "air_density": 1.25,
        "power": 1100,
        "power_lag_1": 1050,
        "power_lag_2": 1000,
        "power_lag_3": 980,
        "power_lag_4": 960
      },
      {
        "time": "2025-07-18T05:45:00",
        "wind_speed": 7.2,
        "wind_direction": 278,
        "cabin_angle": 110.3,
        "total_cabin_angle": 12503,
        "paddle1_angle": 1.15,
        "paddle2_angle": 1.25,
        "paddle3_angle": 1.05,
        "outdoor_temp": 15.6,
        "wind_speed_100m": 7.6,
        "wind_direction_100m": 276,
        "temperature": 15.1,
        "air_pressure": 1015.3,
        "air_density": 1.25,
        "power": 1150,
        "power_lag_1": 1100,
        "power_lag_2": 1050,
        "power_lag_3": 1000,
        "power_lag_4": 980
      },
      {
        "time": "2025-07-18T06:00:00",
        "wind_speed": 7.5,
        "wind_direction": 280,
        "cabin_angle": 110.4,
        "total_cabin_angle": 12504,
        "paddle1_angle": 1.2,
        "paddle2_angle": 1.3,
        "paddle3_angle": 1.1,
        "outdoor_temp": 15.8,
        "wind_speed_100m": 7.8,
        "wind_direction_100m": 278,
        "temperature": 15.3,
        "air_pressure": 1015.4,
        "air_density": 1.24,
        "power": 1200,
        "power_lag_1": 1150,
        "power_lag_2": 1100,
        "power_lag_3": 1050,
        "power_lag_4": 1000
      },
      {
        "time": "2025-07-18T06:15:00",
        "wind_speed": 7.7,
        "wind_direction": 282,
        "cabin_angle": 110.5,
        "total_cabin_angle": 12505,
        "paddle1_angle": 1.25,
        "paddle2_angle": 1.35,
        "paddle3_angle": 1.15,
        "outdoor_temp": 16,
        "wind_speed_100m": 8,
        "wind_direction_100m": 280,
        "temperature": 15.5,
        "air_pressure": 1015.5,
        "air_density": 1.24,
        "power": 1250,
        "power_lag_1": 1200,
        "power_lag_2": 1150,
        "power_lag_3": 1100,
        "power_lag_4": 1050
      },
      {
        "time": "2025-07-18T06:30:00",
        "wind_speed": 8,
        "wind_direction": 285,
        "cabin_angle": 110.6,
        "total_cabin_angle": 12506,
        "paddle1_angle": 1.3,
        "paddle2_angle": 1.4,
        "paddle3_angle": 1.2,
        "outdoor_temp": 16.2,
        "wind_speed_100m": 8.3,
        "wind_direction_100m": 283,
        "temperature": 15.7,
        "air_pressure": 1015.6,
        "air_density": 1.24,
        "power": 1300,
        "power_lag_1": 1250,
        "power_lag_2": 1200,
        "power_lag_3": 1150,
        "power_lag_4": 1100
      },
      {
        "time": "2025-07-18T06:45:00",
        "wind_speed": 8.2,
        "wind_direction": 288,
        "cabin_angle": 110.7,
        "total_cabin_angle": 12507,
        "paddle1_angle": 1.35,
        "paddle2_angle": 1.45,
        "paddle3_angle": 1.25,
        "outdoor_temp": 16.4,
        "wind_speed_100m": 8.5,
        "wind_direction_100m": 286,
        "temperature": 15.9,
        "air_pressure": 1015.7,
        "air_density": 1.24,
        "power": 1350,
        "power_lag_1": 1300,
        "power_lag_2": 1250,
        "power_lag_3": 1200,
        "power_lag_4": 1150
      },
      {
        "time": "2025-07-18T07:00:00",
        "wind_speed": 8.5,
        "wind_direction": 290,
        "cabin_angle": 110.8,
        "total_cabin_angle": 12508,
        "paddle1_angle": 1.4,
        "paddle2_angle": 1.5,
        "paddle3_angle": 1.3,
        "outdoor_temp": 16.6,
        "wind_speed_100m": 8.8,
        "wind_direction_100m": 288,
        "temperature": 16.1,
        "air_pressure": 1015.8,
        "air_density": 1.23,
        "power": 1400,
        "power_lag_1": 1350,
        "power_lag_2": 1300,
        "power_lag_3": 1250,
        "power_lag_4": 1200
      },
      {
        "time": "2025-07-18T07:15:00",
        "wind_speed": 8.7,
        "wind_direction": 292,
        "cabin_angle": 110.9,
        "total_cabin_angle": 12509,
        "paddle1_angle": 1.45,
        "paddle2_angle": 1.55,
        "paddle3_angle": 1.35,
        "outdoor_temp": 16.8,
        "wind_speed_100m": 9,
        "wind_direction_100m": 290,
        "temperature": 16.3,
        "air_pressure": 1015.9,
        "air_density": 1.23,
        "power": 1450,
        "power_lag_1": 1400,
        "power_lag_2": 1350,
        "power_lag_3": 1300,
        "power_lag_4": 1250
      },
      {
        "time": "2025-07-18T07:30:00",
        "wind_speed": 9,
        "wind_direction": 295,
        "cabin_angle": 111,
        "total_cabin_angle": 12510,
        "paddle1_angle": 1.5,
        "paddle2_angle": 1.6,
        "paddle3_angle": 1.4,
        "outdoor_temp": 17,
        "wind_speed_100m": 9.3,
        "wind_direction_100m": 293,
        "temperature": 16.5,
        "air_pressure": 1016,
        "air_density": 1.23,
        "power": 1500,
        "power_lag_1": 1450,
        "power_lag_2": 1400,
        "power_lag_3": 1350,
        "power_lag_4": 1300
      },
      {
        "time": "2025-07-18T07:45:00",
        "wind_speed": 9.2,
        "wind_direction": 298,
        "cabin_angle": 111.1,
        "total_cabin_angle": 12511,
        "paddle1_angle": 1.55,
        "paddle2_angle": 1.65,
        "paddle3_angle": 1.45,
        "outdoor_temp": 17.2,
        "wind_speed_100m": 9.5,
        "wind_direction_100m": 296,
        "temperature": 16.7,
        "air_pressure": 1016.1,
        "air_density": 1.23,
        "power": 1550,
        "power_lag_1": 1500,
        "power_lag_2": 1450,
        "power_lag_3": 1400,
        "power_lag_4": 1350
      },
      {
        "time": "2025-07-18T08:00:00",
        "wind_speed": 9.5,
        "wind_direction": 300,
        "cabin_angle": 111.2,
        "total_cabin_angle": 12512,
        "paddle1_angle": 1.6,
        "paddle2_angle": 1.7,
        "paddle3_angle": 1.5,
        "outdoor_temp": 17.4,
        "wind_speed_100m": 9.8,
        "wind_direction_100m": 298,
        "temperature": 16.9,
        "air_pressure": 1016.2,
        "air_density": 1.22,
        "power": 1600,
        "power_lag_1": 1550,
        "power_lag_2": 1500,
        "power_lag_3": 1450,
        "power_lag_4": 1400
      },
      {
        "time": "2025-07-18T08:15:00",
        "wind_speed": 9.7,
        "wind_direction": 302,
        "cabin_angle": 111.3,
        "total_cabin_angle": 12513,
        "paddle1_angle": 1.65,
        "paddle2_angle": 1.75,
        "paddle3_angle": 1.55,
        "outdoor_temp": 17.6,
        "wind_speed_100m": 10,
        "wind_direction_100m": 300,
        "temperature": 17.1,
        "air_pressure": 1016.3,
        "air_density": 1.22,
        "power": 1650,
        "power_lag_1": 1600,
        "power_lag_2": 1550,
        "power_lag_3": 1500,
        "power_lag_4": 1450
      },
      {
        "time": "2025-07-18T08:30:00",
        "wind_speed": 10,
        "wind_direction": 305,
        "cabin_angle": 111.4,
        "total_cabin_angle": 12514,
        "paddle1_angle": 1.7,
        "paddle2_angle": 1.8,
        "paddle3_angle": 1.6,
        "outdoor_temp": 17.8,
        "wind_speed_100m": 10.3,
        "wind_direction_100m": 303,
        "temperature": 17.3,
        "air_pressure": 1016.4,
        "air_density": 1.22,
        "power": 1700,
        "power_lag_1": 1650,
        "power_lag_2": 1600,
        "power_lag_3": 1550,
        "power_lag_4": 1500
      },
      {
        "time": "2025-07-18T08:45:00",
        "wind_speed": 10.2,
        "wind_direction": 308,
        "cabin_angle": 111.5,
        "total_cabin_angle": 12515,
        "paddle1_angle": 1.75,
        "paddle2_angle": 1.85,
        "paddle3_angle": 1.65,
        "outdoor_temp": 18,
        "wind_speed_100m": 10.5,
        "wind_direction_100m": 306,
        "temperature": 17.5,
        "air_pressure": 1016.5,
        "air_density": 1.22,
        "power": 1750,
        "power_lag_1": 1700,
        "power_lag_2": 1650,
        "power_lag_3": 1600,
        "power_lag_4": 1550
      },
      {
        "time": "2025-07-18T09:00:00",
        "wind_speed": 10.5,
        "wind_direction": 310,
        "cabin_angle": 111.6,
        "total_cabin_angle": 12516,
        "paddle1_angle": 1.8,
        "paddle2_angle": 1.9,
        "paddle3_angle": 1.7,
        "outdoor_temp": 18.2,
        "wind_speed_100m": 10.8,
        "wind_direction_100m": 308,
        "temperature": 17.7,
        "air_pressure": 1016.6,
        "air_density": 1.21,
        "power": 1800,
        "power_lag_1": 1750,
        "power_lag_2": 1700,
        "power_lag_3": 1650,
        "power_lag_4": 1600
      }
    ]
  }
}
```

### Sample Request (Turbine-Level) 

```json
{
  "predictions": {
    "T1": [
      {
        "timestamp": "2025-07-18T09:15:00",
        "forecasted_power_kw": 819.118028913275
      },
      {
        "timestamp": "2025-07-18T09:30:00",
        "forecasted_power_kw": 1033.62637771335
      },
      {
        "timestamp": "2025-07-18T09:45:00",
        "forecasted_power_kw": 1256.3594688792061
      },
      {
        "timestamp": "2025-07-18T10:00:00",
        "forecasted_power_kw": 1446.8185161887793
      },
      {
        "timestamp": "2025-07-18T10:15:00",
        "forecasted_power_kw": 1525.3419857305098
      },
      {
        "timestamp": "2025-07-18T10:30:00",
        "forecasted_power_kw": 1541.5937664790167
      },
      {
        "timestamp": "2025-07-18T10:45:00",
        "forecasted_power_kw": 1535.524382534582
      },
      {
        "timestamp": "2025-07-18T11:00:00",
        "forecasted_power_kw": 1534.9523446006936
      },
      {
        "timestamp": "2025-07-18T11:15:00",
        "forecasted_power_kw": 1512.9870740952188
      },
      {
        "timestamp": "2025-07-18T11:30:00",
        "forecasted_power_kw": 1524.479302002605
      },
      {
        "timestamp": "2025-07-18T11:45:00",
        "forecasted_power_kw": 1476.006027346164
      },
      {
        "timestamp": "2025-07-18T12:00:00",
        "forecasted_power_kw": 1406.6417841488835
      },
      {
        "timestamp": "2025-07-18T12:15:00",
        "forecasted_power_kw": 1276.9928886372002
      },
      {
        "timestamp": "2025-07-18T12:30:00",
        "forecasted_power_kw": 1133.332373446366
      },
      {
        "timestamp": "2025-07-18T12:45:00",
        "forecasted_power_kw": 996.3458367856599
      },
      {
        "timestamp": "2025-07-18T13:00:00",
        "forecasted_power_kw": 880.3138284362253
      }
    ],
    "T2": [
      {
        "timestamp": "2025-07-18T09:15:00",
        "forecasted_power_kw": 819.118028913275
      },
      {
        "timestamp": "2025-07-18T09:30:00",
        "forecasted_power_kw": 1033.62637771335
      },
      {
        "timestamp": "2025-07-18T09:45:00",
        "forecasted_power_kw": 1256.3594688792061
      },
      {
        "timestamp": "2025-07-18T10:00:00",
        "forecasted_power_kw": 1446.8185161887793
      },
      {
        "timestamp": "2025-07-18T10:15:00",
        "forecasted_power_kw": 1525.3419857305098
      },
      {
        "timestamp": "2025-07-18T10:30:00",
        "forecasted_power_kw": 1541.5937664790167
      },
      {
        "timestamp": "2025-07-18T10:45:00",
        "forecasted_power_kw": 1535.524382534582
      },
      {
        "timestamp": "2025-07-18T11:00:00",
        "forecasted_power_kw": 1534.9523446006936
      },
      {
        "timestamp": "2025-07-18T11:15:00",
        "forecasted_power_kw": 1512.9870740952188
      },
      {
        "timestamp": "2025-07-18T11:30:00",
        "forecasted_power_kw": 1524.479302002605
      },
      {
        "timestamp": "2025-07-18T11:45:00",
        "forecasted_power_kw": 1476.006027346164
      },
      {
        "timestamp": "2025-07-18T12:00:00",
        "forecasted_power_kw": 1406.6417841488835
      },
      {
        "timestamp": "2025-07-18T12:15:00",
        "forecasted_power_kw": 1276.9928886372002
      },
      {
        "timestamp": "2025-07-18T12:30:00",
        "forecasted_power_kw": 1133.332373446366
      },
      {
        "timestamp": "2025-07-18T12:45:00",
        "forecasted_power_kw": 996.3458367856599
      },
      {
        "timestamp": "2025-07-18T13:00:00",
        "forecasted_power_kw": 880.3138284362253
      }
    ]
  }
}
```

---

## Testing with Swagger

You can try the API directly at:

```
http://localhost:8000/docs
```

---

## Supported Forecast Types

| Type               | Horizon                                                      |
| ------------------ | ------------------------------------------------------------ |
| `ultra_short_term` | 15 minutes to 4 hours in the future, 15 minutes time resolution |
| `short_term`       | From 0:00 the next day to the next 72 hours, 15-minute time resolution |

