from app.predictors.lstm_predictor import LSTMPredictor
from app.predictors.cnn_lstm_predictor import CNNLSTMPredictor
from app.predictors.transformer_predictor import TransformerPredictor

def get_predictor(model_type: str):
    model_type = model_type.lower()
    if model_type == "lstm":
        return LSTMPredictor
    elif model_type == "cnn_lstm":
        return CNNLSTMPredictor
    elif model_type == "transformer":
        return TransformerPredictor
    else:
        raise ValueError(f"Unsupported model type: {model_type}")
