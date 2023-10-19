#!/usr/bin/env python3
"""Main script for preprocessing the anghadataset. Must be run from the root dir of the project"""
import sys
from pathlib import Path

from decompile.preprocessing.preprocess import preprocess
from decompile.preprocessing.preprocess import collect_c_files

DATASET_NAME = "AnghaBench"
anghaBench_dataset_folder = Path(f"./datasets/raw/{DATASET_NAME}")
input_folder = Path("./datasets/formatted/input")
output_folder = Path("./datasets/formatted/output")
ARCHITECTURE = "x86-64"
SYNTAX_TYPE = "att"


def main() -> int:
    """Main entry point for preprocessing the anghadataset"""
    if not anghaBench_dataset_folder.exists():
        raise FileNotFoundError(
            f"AngaBench dataset folder not found at {anghaBench_dataset_folder}"
        )
    if not input_folder.exists():
        input_folder.mkdir(parents=True)

    if not output_folder.exists():
        output_folder.mkdir(parents=True)

    collect_c_files(
        str(anghaBench_dataset_folder),
        str(input_folder),
    )
    print("Finished collecting c files.")
    preprocess(
        str(input_folder),
        str(output_folder),
        number_of_samples=1000,
        number_of_processor_cores=4,
        syntax_for_assembly_language=SYNTAX_TYPE,
        architecture=ARCHITECTURE,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
