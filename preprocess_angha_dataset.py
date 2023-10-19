"""Main script for preprocessing the anghadataset"""
from pathlib import Path

from decompile.preprocessing import preprocess

DATASET_NAME = "AnghaBench"
anghaBench_dataset_folder = Path(f"./datasets/raw/{DATASET_NAME}")
input_folder = Path(f"./datasets/formatted/{DATASET_NAME}/input")
output_folder = Path(f"./datasets/formatted/{DATASET_NAME}/output")
ARCHITECTURE = "x86-64"
SYNTAX_TYPE = "att"


def main() -> None:
    """Main entry point for preprocessing the anghadataset"""
    if not anghaBench_dataset_folder.exists():
        raise FileNotFoundError(
            f"AngaBench dataset folder not found at {anghaBench_dataset_folder}"
        )
    if not input_folder.exists():
        input_folder.mkdir(parents=True)

    if not output_folder.exists():
        output_folder.mkdir(parents=True)

    preprocess.collect_c_files(
        str(anghaBench_dataset_folder),
        str(input_folder),
    )
    preprocess.preprocess(
        str(input_folder),
        str(output_folder),
        number_of_samples=1000,
        number_of_processor_cores=4,
        syntax_for_assembly_language=SYNTAX_TYPE,
        archticture=ARCHITECTURE,
    )


if __name__ == "__main__":
    main()
