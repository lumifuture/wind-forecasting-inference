# app/services/inference_engine.py

import numpy as np
import torch

class InferencePipeline:
    def __init__(self, model, metadata, predictor_class, scaler_x=None, scaler_y=None):
        """
        Handles preprocessing, prediction, and postprocessing.
        
        Args:
            model: The trained PyTorch model.
            metadata: Dictionary with metadata for the model.
            predictor_class: A subclass of BasePredictor.
            scaler_x: Optional input scaler (e.g., sklearn StandardScaler).
            scaler_y: Optional output scaler for inverse transformation.
        """
        self.model = model
        self.metadata = metadata
        self.predictor = predictor_class(model, metadata)
        self.scaler_x = scaler_x
        self.scaler_y = scaler_y

    def preprocess(self, input_tensor: torch.Tensor) -> torch.Tensor:
        """
        Applies input scaling if scaler_x is provided.
        """
        if self.scaler_x is not None:
            input_np = input_tensor.squeeze(0).numpy()
            input_scaled = self.scaler_x.transform(input_np)
            input_tensor = torch.tensor(input_scaled, dtype=torch.float32).unsqueeze(0)
        return input_tensor

    def postprocess(self, predictions: list) -> list:
        """
        Applies inverse scaling and clipping based on metadata.
        """
        if self.scaler_y is not None:
            predictions = self.scaler_y.inverse_transform(
                np.array(predictions).reshape(-1, 1)
            ).flatten().tolist()

        if self.metadata.get("clip_min") is not None:
            predictions = [max(x, self.metadata["clip_min"]) for x in predictions]
        if self.metadata.get("clip_max") is not None:
            predictions = [min(x, self.metadata["clip_max"]) for x in predictions]

        return predictions

    def run(self, input_tensor: torch.Tensor) -> list:
        """
        Runs the full pipeline: preprocess → predict → postprocess.
        """
        input_tensor = self.preprocess(input_tensor)
        raw_output = self.predictor.predict(input_tensor)
        return self.postprocess(raw_output)
