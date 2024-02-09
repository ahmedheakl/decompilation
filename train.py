"""Trainer script

To invoke this endpoint, just run `python train.py --dataset_path <path_to_dataset>`.
"""
from typing import Dict
import sys
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter

from decompile.trainers.llama_trainer import LLaMaTrainer
from decompile.trainers.trainer import Trainer


def main() -> int:
    """Main entry point"""
    models: Dict[str, Trainer] = {
        "llama": LLaMaTrainer,
    }
    parser = ArgumentParser(
        prog="Train",
        description="Training LLama model",
        epilog="Hope it goes well!",
        formatter_class=ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--model",
        type=str,
        choices=models.keys(),
        default="llama",
        help="Model to train.",
    )
    parser.add_argument(
        "--dataset_path",
        type=str,
        required=True,
        help="Path to the dataset folder.",
    )
    parser.add_argument(
        "--input_field_name",
        type=str,
        default="input",
        help="Name of the input field in the dataset.",
    )
    parser.add_argument(
        "--output_field_name",
        type=str,
        default="output",
        help="Name of the output field in the dataset.",
    )
    args = parser.parse_args()

    trainer_class = models[args.model]
    trainer = trainer_class(
        dataset_path=args.dataset_path,
        input_field_name=args.input_field_name,
        output_field_name=args.output_field_name,
    )

    trainer.train()
    print("Training finished.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
