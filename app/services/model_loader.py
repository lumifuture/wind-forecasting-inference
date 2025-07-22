# app/services/model_loader.py

import json
from pathlib import Path
import joblib
import torch
from app.registry.model_registry import get_model_class

CATALOG_PATH = Path("app/config/model_catalog.json")


def load_model_from_path(model_path: str, metadata_path: str):
    model_path = Path(model_path)
    metadata_path = Path(metadata_path)
    model_dir = model_path.parent

    if not model_path.exists():
        raise FileNotFoundError(f"Model file not found at: {model_path}")
    if not metadata_path.exists():
        raise FileNotFoundError(f"Metadata file not found at: {metadata_path}")

    metadata = json.loads(metadata_path.read_text())
    model_type = metadata["model_type"]
    model_args = metadata["model_architecture"]

    ModelClass = get_model_class(model_type)
    model = ModelClass(**model_args)
    model.load_state_dict(torch.load(model_path, map_location="cpu"))
    model.eval()

    scaler_x_path = model_dir / "scaler_x.pkl"
    scaler_y_path = model_dir / "scaler_y.pkl"
    scaler_x = joblib.load(scaler_x_path) if scaler_x_path.exists() else None
    scaler_y = joblib.load(scaler_y_path) if scaler_y_path.exists() else None

    return model, metadata, scaler_x, scaler_y


def load_model(model_name, forecast_type, model_type, version, level, turbine_id=None):
    catalog = json.loads(CATALOG_PATH.read_text())

    try:
        entry = catalog[model_name][forecast_type][model_type][version]
    except KeyError:
        raise ValueError(f"Model not found in catalog: {model_name}/{forecast_type}/{model_type}/{version}")

    if level == "farm":
        model_path = entry["farm"]
        metadata_path = str(Path(model_path).parent / "metadata.json")

    elif level == "turbine":
        try:
            model_path = entry["turbines"][turbine_id]
            metadata_path = str(Path(model_path).parent / "metadata.json")
        except KeyError:
            if "shared_turbine_model" in entry:
                model_path = entry["shared_turbine_model"]
                metadata_path = str(Path(model_path).parent / "metadata.json")
            else:
                raise ValueError(f"No model found for turbine {turbine_id} and no shared fallback.")

    else:
        raise ValueError("Unknown level: should be 'farm' or 'turbine'")

    return load_model_from_path(model_path, metadata_path)
