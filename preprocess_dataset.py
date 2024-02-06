#!/usr/bin/env python3
"""Main script for preprocessing the anghadataset. Must be run from the root dir of the project"""
import sys
from pathlib import Path

from decompile.preprocessing.preprocess import GeeksForGeeksDataset

# constants
SOURCE_CODE_FOLDER = Path("./datasets/formatted/input")
ASM_CODE_FOLDER = Path("./datasets/formatted/output")

# TODO: provide the dataset as a cli argument
DATASET_NAME = "geeks_for_geeks_successful_test_scripts"
ARCHITECTURE = "x86-64"
SYNTAX_TYPE = "att"
NUM_OF_SAMPLES = 1000
NUM_CORES = 4
jsonl_file_path = Path(f"./datasets/formatted/{DATASET_NAME}.jsonl")
dataset_folder = Path(f"./datasets/raw/{DATASET_NAME}")


def main() -> int:
    """Main entry point for preprocessing the dataset"""
    if not dataset_folder.exists():
        raise FileNotFoundError(f"dataset folder not found at {dataset_folder}")
    SOURCE_CODE_FOLDER.mkdir(parents=True, exist_ok=True)
    ASM_CODE_FOLDER.mkdir(parents=True, exist_ok=True)

    dataset = GeeksForGeeksDataset(
        raw_dataset_path=dataset_folder,
        out_source_folder_path=SOURCE_CODE_FOLDER,
        out_asm_folder_path=ASM_CODE_FOLDER,
        num_samples=NUM_OF_SAMPLES,
        asm_syntax_type=SYNTAX_TYPE,
        architecture=ARCHITECTURE,
    )
    dataset.collect_and_preprocess_source_files()
    print("Finished collecting source files.")

    dataset.compile_source_folder_and_generate_assembly(nproc=NUM_CORES)
    print("Finished dissembling.")

    dataset.save_as_jsonl_and_standardize(jsonl_file_path)
    print("Finished creating jsonl file.")

    print(f"Finished preprocessing {DATASET_NAME}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
