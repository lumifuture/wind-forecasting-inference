from app.predictors.base import BasePredictor
import torch

class TransformerPredictor(BasePredictor):
    def predict(self, input_tensor: torch.Tensor) -> list:
        with torch.no_grad():
            output = self.model(input_tensor)
        return output.squeeze(0).tolist()
