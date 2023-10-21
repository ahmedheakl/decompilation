#!/usr/bin/env python3
"""Main script for preprocessing the anghadataset. Must be run from the root dir of the project"""
import sys
from pathlib import Path

from decompile.preprocessing.preprocess import (
    preprocess,
    collect_c_files,
    create_jsonl_and_standardize,
)

# TODO: provide the dataset as a cli argument
DATASET_NAME = "geeks_for_geeks_successful_test_scripts"
dataset_folder = Path(f"./datasets/raw/{DATASET_NAME}")
input_folder = Path("./datasets/formatted/input")
output_folder = Path("./datasets/formatted/output")
jsonl_file = Path(f"./datasets/formatted/{DATASET_NAME}.jsonl")
ARCHITECTURE = "x86-64"
SYNTAX_TYPE = "att"


def main() -> int:
    """Main entry point for preprocessing the dataset"""
    if not dataset_folder.exists():
        raise FileNotFoundError(f"dataset folder not found at {dataset_folder}")
    if not input_folder.exists():
        input_folder.mkdir(parents=True)

    if not output_folder.exists():
        output_folder.mkdir(parents=True)

    collect_c_files(
        str(dataset_folder),
        str(input_folder),
    )
    print("Finished collecting source files.")

    preprocess(
        str(input_folder),
        str(output_folder),
        number_of_samples=1000,
        number_of_processor_cores=4,
        syntax_for_assembly_language=SYNTAX_TYPE,
        architecture=ARCHITECTURE,
    )
    print("Finished dissembling.")
    create_jsonl_and_standardize(output_folder, input_folder, jsonl_file)
    print("Finished creating jsonl file.")
    print(f"Finished preprocessing {DATASET_NAME}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
