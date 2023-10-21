"""Process the C code"""
from typing import List
import os
import subprocess
import shutil
from functools import partial
from multiprocessing import Pool
import json
from pathlib import Path
from decompile.preprocessing.standardize import standardize_asm_file

sample_files_num = 1000


def compile_to_binary(c_file_path: Path | str, output_folder: Path | str) -> None:
    """Converting C code files into binary files

    Args:
        c_file_path (str): Path for .c source file.
        output_folder (str): Path for output of the compilation.
    """
    c_file_path = Path(c_file_path)
    file_name_without_ext = c_file_path.stem
    out_file = str(output_folder) + "/" + str(file_name_without_ext) + ".o"
    compiler_command = "gcc -c" if c_file_path.suffix == ".c" else "g++ -c"
    assemble_command = f"{compiler_command} {c_file_path} -o {out_file}"

    try:
        subprocess.run(assemble_command, check=True, shell=True)
    except subprocess.CalledProcessError as e:
        print(
            f"Compilation failed with error:\n{e} and "
            + f"the error is associated with the following output file {out_file}"
        )


def disassemble_to_assembly(
    binary_file: str,
    syntax_for_assembly_language: str,
    architecture: str,
) -> None:
    """Disassembling binary files into assembly code files

    Args:
        binary_file (str): It's the path for the binary file being disassembled
        syntax_for_assembly_language (str): This will be used in the objdump command to specify the
        assembly langauge syntax for the assembly output files
        architecture (str): This will specify the architecture that's we're
        working with in the output files
    """

    assembly_file_path: str = os.path.splitext(binary_file)[0] + ".s"
    try:
        with open(assembly_file_path, "w", encoding="utf-8") as assembly_file:
            subprocess.run(
                [
                    "objdump",
                    "-d",
                    "-M",
                    syntax_for_assembly_language,
                    "-M",
                    architecture,
                    "--no-addresses",
                    binary_file,
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
    input_folder: str,
    output_folder: str,
    number_of_samples: int,
    number_of_processor_cores: int,
    syntax_for_assembly_language: str,
    architecture: str,
) -> None:
    """Converts .c source files into specific artichture of
    assembly using multiporocessing module.

    Args:
        input_folder (str): Path for the input folder for .c files.
        output_folder (str): It's the path for the output folder for the preprocessing
        number_of_samples (int): It's the number of data samples that will used for training
        number_of_processor_cores (int): It's the number of cores to be used by the multiprocessing
        module in python to optimize the exection time of the function
        syntax_for_assembly_language (str): This will be used in the objdump command to specify the
        assembly langauge syntax for the assembly output files
        architecture (str): This will specify the architecture that's
        we're working with in the output files
    """

    source_files: List[str] = []
    for filename in os.listdir(input_folder)[:number_of_samples]:
        if filename.endswith(".c") or filename.endswith(".cpp"):
            source_files.append(os.path.join(input_folder, filename))

    partial_compile = partial(compile_to_binary, output_folder=output_folder)
    with Pool(processes=number_of_processor_cores) as pool:
        pool.map(partial_compile, source_files)

    binary_files = [
        os.path.join(output_folder, os.path.basename(os.path.splitext(file)[0]) + ".o")
        for file in source_files
    ]

    partial_disassemble = partial(
        disassemble_to_assembly,
        syntax_for_assembly_language=syntax_for_assembly_language,
        architecture=architecture,
    )
    with Pool(processes=number_of_processor_cores) as pool:
        pool.map(partial_disassemble, binary_files)


def collect_c_files(source_folder_path: str, output_dir_path: str) -> None:
    """Collect all C files into one folder. This helps to make
        the compilation process easier by avoiding recursively calling the
        functions inside each subdirectory of a directory to access all the
        C code files of the dataset of AngaBench.

    Args:
        source_folder_path (str): Folder containing all source files
        output_dir_path (str): Output folder for binary code
    """
    # FIXME: The global variable is not a good idea.
    # FIXME: The actual number of files found is 900 not 1000 like the global variable.
    global sample_files_num
    os.makedirs(output_dir_path, exist_ok=True)
    for entry in os.scandir(source_folder_path):
        if sample_files_num == 0:
            break
        if entry.name in (".", ".."):
            continue
        full_path = os.path.join(source_folder_path, entry.name)

        if entry.is_dir():
            collect_c_files(full_path, output_dir_path)
        elif entry.name.endswith(".c") or entry.name.endswith(".cpp"):
            output_file_path = os.path.join(output_dir_path, entry.name)
            shutil.copyfile(full_path, output_file_path)
            sample_files_num -= 1


def create_jsonl_and_standardize(
    assembly_folder_path: Path,
    source_folder_path: Path,
    jsonl_file_path: Path,
) -> None:
    """Creates jsonl file after standardizing the assembly files. The jsonl
    file is then used to create the dataset using load_dataset function.

    Args:
        assembly_folder_path (Path): path to the folder containing assembly files
        source_folder_path (Path): path to the folder containing source files
        jsonl_file_path (Path): path to the jsonl file
    """
    # loop over all files in the source_folder_path
    data_buffer = []
    for source_file in source_folder_path.iterdir():
        output_str = source_file.read_text(encoding="utf-8")
        assembly_file_path = Path(source_file.stem + ".s")
        assembly_file_path = assembly_folder_path / assembly_file_path
        input_str = standardize_asm_file(assembly_file_path)
        data_buffer.append({"input": input_str, "output": output_str})
    with jsonl_file_path.open(mode="w", encoding="utf-8") as jsonl_file:
        for entry in data_buffer:
            jsonl_file.write(json.dumps(entry) + "\n")
