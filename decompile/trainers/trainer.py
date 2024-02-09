"""Abstract class for all trainers."""
from typing import Any, Tuple
from abc import ABC, abstractmethod


class Trainer(ABC):
    """Abstract class for all trainers."""

    def __init__(
        self,
        dataset_path: str,
        input_field_name: str = "input",
        output_field_name: str = "output",
    ) -> None:
        self.dataset_path = dataset_path
        self.input_field_name = input_field_name
        self.output_field_name = output_field_name

    @abstractmethod
    def train(self) -> Tuple[Any, Any]:
        """Train the model.

        Returns:
            Any: Trained model and the tokenizer.
        """

    @staticmethod
    @abstractmethod
    def add_template(assembly_text: str) -> str:
        """Add template to assembly.

        Args:
            assembly (str): Assembly to add template to.

        Returns:
            str: Assembly with template.
        """

    @staticmethod
    @abstractmethod
    def load_model(model_path: str, tokenizer_path: str) -> Tuple[Any, Any]:
        """Load model from path.

        Args:
            model_path (str): Path to the model.
            tokenizer_path (str): Path to the tokenizer.

        Returns:
            Tuple[Any, Any]: Model and tokenizer.
        """
