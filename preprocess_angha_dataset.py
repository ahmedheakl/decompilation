"""Main script for preprocessing the anghadataset"""
from pathlib import Path

from decompile.preprocessing import preprocess

anghaBench_dataset_folder = Path("/home/mohanned/Work/AnghaBench")
input_folder = Path("/home/mohanned/Work/DataC")
output_folder = Path("/home/mohanned/Work/Binary")
architecture = "x86-64"
syntax_type = "att"


def main() -> None:
    """Main entry point for preprocessing the anghadataset"""
    if not input_folder.exists():
        input_folder.mkdir(parents=True, exist_ok=True)

    if not output_folder.exists():
        output_folder.mkdir(parents=True, exist_ok=True)

    preprocess.collect_c_files(
        anghaBench_dataset_folder.as_posix(),
        input_folder.as_posix(),
    )
    preprocess.preprocess(
        input_folder.as_posix(),
        output_folder.as_posix(),
        number_of_samples=1000,
        number_of_processor_cores=4,
        syntax_for_assembly_language=syntax_type,
        archticture=architecture,
    )


if __name__ == "__main__":
    main()
