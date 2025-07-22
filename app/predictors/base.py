from abc import ABC, abstractmethod
import torch

class BasePredictor(ABC):
    def __init__(self, model, metadata):
        self.model = model
        self.metadata = metadata

    @abstractmethod
    def predict(self, input_tensor: torch.Tensor) -> list:
        pass
