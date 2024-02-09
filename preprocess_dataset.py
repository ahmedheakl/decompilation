#!/usr/bin/env python3
"""Main script for preprocessing the anghadataset. Must be run from the root dir of the project"""
import sys
from pathlib import Path

from decompile.preprocessing.preprocess import DatasetJsonl

# constants
INPUT_FOLDER = Path("./datasets/formatted/input")
OUTPUT_FOLDER = Path("./datasets/formatted/output")

# TODO: provide the dataset as a cli argument
DATASET_NAME = "geeks_for_geeks_successful_test_scripts"
ARCHITECTURE = "x86-64"
SYNTAX_TYPE = "att"
NUM_OF_SAMPLES = 1000
NUM_CORES = 4
jsonl_file = Path(f"./datasets/formatted/{DATASET_NAME}.jsonl")
dataset_folder = Path(f"./datasets/raw/{DATASET_NAME}")


def main() -> int:
    """Main entry point for preprocessing the dataset"""
    if not dataset_folder.exists():
        raise FileNotFoundError(f"dataset folder not found at {dataset_folder}")
    if not INPUT_FOLDER.exists():
        INPUT_FOLDER.mkdir(parents=True)

    if not OUTPUT_FOLDER.exists():
        OUTPUT_FOLDER.mkdir(parents=True)

    dataset = DatasetJsonl(
        raw_dataset_path=dataset_folder,
        num_samples=NUM_OF_SAMPLES,
        asm_syntax_type=SYNTAX_TYPE,
        architecture=ARCHITECTURE,
    )
    dataset.collect_source_files(INPUT_FOLDER)
    print("Finished collecting source files.")

    dataset.preprocess(INPUT_FOLDER, OUTPUT_FOLDER, nproc=4)
    print("Finished dissembling.")
    DatasetJsonl.create_jsonl_and_standardize(OUTPUT_FOLDER, INPUT_FOLDER, jsonl_file)
    print("Finished creating jsonl file.")
    print(f"Finished preprocessing {DATASET_NAME}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
