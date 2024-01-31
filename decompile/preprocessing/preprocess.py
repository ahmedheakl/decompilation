"""Dataset preprocessing moduel. Takes care of collecting, and compiling source files,
 and disassembling binaries."""
import os
import subprocess
import shutil
import json
from pathlib import Path
from typing import List
from typing import Union
from functools import partial
from multiprocessing import Pool

from decompile.preprocessing.standardize import standardize_asm_file


class DatasetJsonl:
    """Class for representing datasets and creating jsonl files

    Attributes:
        dataset_path (Union[Path, str]): Path for the dataset folder.
        num_samples (int): Number of samples to be used for training.
        asm_syntax_type (str): Syntax type for Generated asm files.
        architecture (str): Architecture type for asm output files.
    """

    compilation_command_dict = {".c": "gcc -c", ".cpp": "g++ -c"}

    def __init__(
        self,
        raw_dataset_path: Union[Path, str],
        num_samples: int,
        asm_syntax_type: str = "att",
        architecture: str = "x86-64",
    ) -> None:
        self.raw_dataset_path = Path(raw_dataset_path)
        self.num_samples = num_samples
        self.asm_syntax_type = asm_syntax_type
        self.architecture = architecture

    @staticmethod
    def _compile_to_binary(
        source_file_path: Union[Path, str], output_folder: Union[Path, str]
    ) -> None:
        """Converts source files into binary files

        Args:
            source_file_path (str): Path for .c source file.
            output_folder (str): Path for compilation output.
        """
        source_file_path = Path(source_file_path)
        output_folder = Path(output_folder)
        file_name_without_ext = source_file_path.stem
        out_file = (output_folder / file_name_without_ext).with_suffix(".o")
        compiler_command = DatasetJsonl.compilation_command_dict[
            source_file_path.suffix
        ]
        assemble_command = f"{compiler_command} {source_file_path} -o {out_file}"

        try:
            subprocess.run(assemble_command, check=True, shell=True)
        except subprocess.CalledProcessError as e:
            print(
                f"Compilation failed with error:\n{e} and "
                + f"the error is associated with the following output file {out_file}"
            )

    @staticmethod
    def _disassemble_to_assembly(
        binary_file: Union[Path, str],
        syntax_for_assembly_language: str,
        architecture: str,
    ) -> None:
        """Disassembles binary files into assembly(.s) files in the same folder.

        Args:
            binary_file (Union[Path, str]): Disassembled binary file path.
            syntax_for_assembly_language (str): syntax type for the assembly output files.
            architecture (str): architecure type for assembly output files.
        """
        binary_file = Path(binary_file)
        assembly_file_path = binary_file.with_suffix(".s")
        try:
            with assembly_file_path.open("w", encoding="utf-8") as assembly_file:
                subprocess.run(
                    [
                        "objdump",
                        "-d",
                        "-M",
                        syntax_for_assembly_language,
                        "-M",
                        architecture,
                        "-M",
                        "att-mnemonic",
                        "-M",
                        "suffix",
                        "--demangle",
                        "--line-numbers",
                        "--no-show-raw-insn",
                        # "--no-addresses",
                        str(binary_file),
                    ],
                    stdout=assembly_file,
                    check=True,
                )
                os.remove(binary_file)
        except subprocess.CalledProcessError as e:
            print(
                f"Dissembling failed with error:\n{e} and "
                + f"the error is associated with the following output file {assembly_file_path}"
            )

    def preprocess(
        self,
        input_folder: Union[Path, str],
        output_folder: Union[Path, str],
        nproc: int,
    ) -> None:
        """Converts source files into assembly using multiprocessing. First
        compiles source using corresponding language compiler. Then disassembles
        binaries using objdump.

        Args:
            input_folder (str): Path for the folder containing source files.
            output_folder (str): Path for the folder to deposit the binaries then assembly files.
            nproc (int): Number of processes to use for multiprocessing.
        """
        input_folder = Path(input_folder)
        output_folder = Path(output_folder)
        source_files: List[str] = []
        for filename in os.listdir(input_folder)[: self.num_samples]:
            if os.path.splitext(filename)[1] in DatasetJsonl.compilation_command_dict:
                source_files.append(os.path.join(input_folder, filename))

        partial_compile = partial(
            DatasetJsonl._compile_to_binary, output_folder=output_folder
        )
        with Pool(processes=nproc) as pool:
            pool.map(partial_compile, source_files)

        print("Finished compiling.")
        binary_files = [
            os.path.join(
                output_folder, os.path.basename(os.path.splitext(file)[0]) + ".o"
            )
            for file in source_files
        ]

        partial_disassemble = partial(
            DatasetJsonl._disassemble_to_assembly,
            syntax_for_assembly_language=self.asm_syntax_type,
            architecture=self.architecture,
        )
        with Pool(processes=nproc) as pool:
            pool.map(partial_disassemble, binary_files)

    def collect_source_files(
        self,
        output_folder_path: Union[Path, str],
    ) -> None:
        """Collect all source files into one folder.

        Args:
            output_folder_path (Union[Path, str]): Folder for depositing collected source files.
        """
        sample_files_num = self.num_samples

        def _collect_source_files(source_folder_path: Union[Path, str]) -> None:
            """DFS search for collecting source files from source_folder_path
            and copying them to output_folder_path.

            Args:
                source_folder_path (Union[Path, str]): Folder containing all source files.
                output_folder_path (Union[Path, str]): Folder for depositing collected source files.
            """
            # FIXME: The global variable is not a good idea.
            # FIXME: The actual number of files found is 900 not 1000 like the global variable.
            nonlocal sample_files_num
            nonlocal output_folder_path
            for entry in os.scandir(source_folder_path):
                if sample_files_num == 0:
                    break
                if entry.name in (".", ".."):
                    continue
                full_input_path = os.path.join(source_folder_path, entry.name)

                if entry.is_dir():
                    _collect_source_files(full_input_path)
                elif entry.name.endswith(".c") or entry.name.endswith(".cpp"):
                    output_file_path = os.path.join(output_folder_path, entry.name)
                    shutil.copyfile(full_input_path, output_file_path)
                    DatasetJsonl.remove_comments_empty_includes_and_main(
                        output_file_path
                    )
                    sample_files_num -= 1

        _collect_source_files(self.raw_dataset_path)

    @staticmethod
    def create_jsonl_and_standardize(
        assembly_folder_path: Union[Path, str],
        source_folder_path: Union[Path, str],
        jsonl_file_path: Union[Path, str],
    ) -> None:
        """Creates jsonl file after standardizing the assembly files. The jsonl
        file is then used to create the dataset using load_dataset function.

        Args:
            assembly_folder_path (Path): Path to the folder containing assembly files.
            source_folder_path (Path): Path to the folder containing source files.
            jsonl_file_path (Path): Path to the jsonl file.
        """
        assembly_folder_path = Path(assembly_folder_path)
        source_folder_path = Path(source_folder_path)
        jsonl_file_path = Path(jsonl_file_path)
        data_buffer = []
        for source_file in source_folder_path.iterdir():
            output_str = source_file.read_text(encoding="utf-8").strip()
            assembly_file_path = Path(source_file.stem + ".s")
            assembly_file_path = assembly_folder_path / assembly_file_path
            input_str = standardize_asm_file(assembly_file_path)
            data_buffer.append(
                {
                    "input": input_str,
                    "output": output_str,
                    "file_name": f"{source_file.name}",
                }
            )
        with jsonl_file_path.open(mode="w", encoding="utf-8") as jsonl_file:
            for entry in data_buffer:
                print(entry)
                jsonl_file.write(json.dumps(entry) + "\n")

    @staticmethod
    def remove_comments_empty_includes_and_main(file_path: Union[Path, str]) -> None:
        """Removes all // comments, empty lines, and main function with everything after it.

        Args:
            file_path (Union[Path, str]): path to c/cpp file
        """
        if isinstance(file_path, str):
            file_path = Path(file_path)
        buffer = []
        with file_path.open("r", encoding="utf-8") as read_file:
            for line in read_file:
                stripped_line = line.strip()
                if (
                    stripped_line.startswith("//")
                    or not stripped_line
                    or (
                        stripped_line.startswith("#include")
                        and stripped_line.find("bits/stdc++.h") == -1
                    )
                ):
                    continue
                if stripped_line.startswith("int main()"):
                    break
                buffer.append(line.rstrip())
        with file_path.open("w", encoding="utf-8") as write_file:
            write_file.write("\n".join(buffer) + "\n")
