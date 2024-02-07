"""Dataset classes for creating json files from raw datasets."""

from pathlib import Path
from typing import Union

from decompile.preprocessing.preprocess import (
    collect_source_files,
    compile_source_folder_and_generate_assembly_using_objdump,
    compile_source_folder_and_generate_assembly_using_gcc,
    create_jsonl_and_standardize,
)
from decompile.preprocessing.standardize import (
    standardize_objdump_asm_file,
    standardize_gcc_asm_output,
)


class GeeksForGeeksDataset:
    """Class for representing datasets and creating jsonl files

    Attributes:
        raw_dataset_path (Union[Path, str]): Path for the dataset folder.
        out_source_folder_path (Union[Path, str]): Path for the source code folder.
        out_asm_folder_path (Union[Path, str]): Path for the assembly code folder.
        num_samples (int): Number of samples to be used for training.
        asm_syntax_type (str): Syntax type for Generated asm files.
        architecture (str): Architecture type for asm output files.
    """

    def __init__(
        self,
        raw_dataset_path: Union[Path, str],
        out_source_folder_path: Union[Path, str],
        out_asm_folder_path: Union[Path, str],
        num_samples: int,
        asm_syntax_type: str = "att",
        architecture: str = "x86-64",
    ) -> None:
        self.raw_dataset_path = Path(raw_dataset_path)
        self.out_source_folder_path = Path(out_source_folder_path)
        self.out_asm_folder_path = Path(out_asm_folder_path)
        self.num_samples = num_samples
        self.asm_syntax_type = asm_syntax_type
        self.architecture = architecture

        self.out_source_folder_path.mkdir(parents=True, exist_ok=True)
        self.out_asm_folder_path.mkdir(parents=True, exist_ok=True)

    def collect_and_preprocess_source_files(self) -> None:
        """Collects source files from the dataset and preprocesses them."""
        collect_source_files(
            self.raw_dataset_path, self.out_source_folder_path, self.num_samples
        )

    def compile_source_folder_and_generate_assembly(self, nproc: int) -> None:
        """Compiles source files and generates assembly files using multiprocessing.

        Args:
            nproc (int): Number of processes to use for multiprocessing.
        """
        compile_source_folder_and_generate_assembly_using_objdump(
            self.out_source_folder_path,
            self.out_asm_folder_path,
            self.asm_syntax_type,
            self.architecture,
            nproc,
        )

    def save_as_jsonl_and_standardize(self, jsonl_file_path: Union[Path, str]):
        """Creates jsonl file after standardizing the assembly files. The jsonl
        file is then used to create the dataset using load_dataset function.

        Args:
            jsonl_file_path (Union[Path, str]): Path to the jsonl file.
        """
        create_jsonl_and_standardize(
            self.out_asm_folder_path,
            self.out_source_folder_path,
            jsonl_file_path,
            standardization_function=standardize_objdump_asm_file,
        )


class AnghaBench:
    """Class for representing the angha dataset and creating jsonl files."""

    def __init__(
        self,
        raw_dataset_path: Union[Path, str],
        out_source_folder_path: Union[Path, str],
        out_asm_folder_path: Union[Path, str],
        num_samples: int,
    ) -> None:
        self.raw_dataset_path = Path(raw_dataset_path)
        self.out_source_folder_path = Path(out_source_folder_path)
        self.out_asm_folder_path = Path(out_asm_folder_path)
        self.num_samples = num_samples

        self.out_source_folder_path.mkdir(parents=True, exist_ok=True)
        self.out_asm_folder_path.mkdir(parents=True, exist_ok=True)

    def collect_and_preprocess_source_files(self) -> None:
        """Collects source files from the dataset and preprocesses them."""
        collect_source_files(
            self.raw_dataset_path,
            self.out_source_folder_path,
            self.num_samples,
            isanghabench=True,
        )

    def compile_source_folder_and_generate_assembly(self, nproc: int) -> None:
        """Compiles source files and generates assembly files using multiprocessing.

        Args:
            nproc (int): Number of processes to use for multiprocessing.
        """
        compile_source_folder_and_generate_assembly_using_gcc(
            self.out_source_folder_path,
            self.out_asm_folder_path,
            nproc,
        )

    def save_as_jsonl_and_standardize(self, jsonl_file_path: Union[Path, str]):
        """Creates jsonl file after standardizing the assembly files. The jsonl
        file is then used to create the dataset using load_dataset function.

        Args:
            jsonl_file_path (Union[Path, str]): Path to the jsonl file.
        """
        create_jsonl_and_standardize(
            self.out_asm_folder_path,
            self.out_source_folder_path,
            jsonl_file_path,
            standardization_function=standardize_gcc_asm_output,
        )
