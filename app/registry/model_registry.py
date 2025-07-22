# app/registry/model_registry.py

from wind_models.lstm import LSTMModel
from wind_models.cnn_lstm import CNNLSTMModel
from wind_models.transformer import TransformerModel


def get_model_class(model_type: str):
    model_type = model_type.lower()
    if model_type == "lstm":
        return LSTMModel
    elif model_type == "cnn_lstm":
        return CNNLSTMModel
    elif model_type == "transformer":
        return TransformerModel
    else:
        raise ValueError(f"Unsupported model type: {model_type}")
