"""Testing models inference"""
import sys
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter

from transformers import pipeline

from decompile.trainers.llama_trainer import LLaMaTrainer


def main() -> int:
    """Main entry point for inference"""

    parser = ArgumentParser(
        prog="Evaluate",
        description="Testing models inference",
        epilog="Hope it goes well!",
        formatter_class=ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        "--model-path",
        type=str,
        required=True,
        help="Path to the model.",
    )
    parser.add_argument(
        "--tokenizer-path",
        type=str,
        required=True,
        help="Path to the tokenizer.",
    )
    parser.add_argument(
        "--input",
        type=str,
        required=True,
        help="Input assembly.",
    )
    parser.add_argument(
        "--max-length",
        type=int,
        default=1024,
        help="Maximum length of the output.",
    )

    args = parser.parse_args()
    prompt = LLaMaTrainer.add_template(args.input)
    model, tokenizer = LLaMaTrainer.load_model(args.model_path, args.tokenizer_path)
    pipe = pipeline(
        task="text-generation",
        model=model,
        tokenizer=tokenizer,
        max_length=args.max_length,
    )
    result = pipe(prompt)
    print("Model Output:\n", result[0]["generated_text"], sep="")
    return 0


if __name__ == "__main__":
    sys.exit(main())
