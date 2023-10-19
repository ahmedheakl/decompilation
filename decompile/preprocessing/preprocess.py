"""Process the C code"""
from typing import List
import os
import subprocess
import shutil
from functools import partial
from multiprocessing import Pool


def compile_to_binary(c_file_path: str, output_folder: str) -> None:
    """Converting C code files into binary files

    Args:
        c_file_path (str): Path for .c source file.
        output_folder (str): Path for output of the compilation.
    """

    binary_file = os.path.splitext(c_file_path)[0]
    binary_file = binary_file[::-1]
    edit = ""
    for c in binary_file:
        if c == "/":
            break
        edit += c
    edit = edit[::-1]
    out_file = output_folder + "/" + edit + ".out"

    assemble_command = f"gcc -c {c_file_path} -o {out_file}"

    try:
        subprocess.run(assemble_command, check=True, shell=True)
    except subprocess.CalledProcessError as e:
        print(
            f"Compilation failed with error:\n{e} and "
            + "the error is associated with the following output file {out_file}"
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
    except subprocess.CalledProcessError as e:
        print(
            f"Compilation failed with error:\n{e} and "
            + "the error is associated with the following output file {assembly_file}"
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
        input_folder (str): It's the path for the input folder for the C code files
        output_folder (str): It's the path for the output folder for the preprocessing
        number_of_samples (int): It's the number of data samples that will used for training
        number_of_processor_cores (int): It's the number of cores to be used by the multiprocessing
        module in python to optimize the exection time of the function
        syntax_for_assembly_language (str): This will be used in the objdump command to specify the
        assembly langauge syntax for the assembly output files
        architecture (str): This will specify the architecture that's
        we're working with in the output files
    """

    c_files: List[str] = []
    for filename in os.listdir(input_folder):
        if len(c_files) == number_of_samples:
            break

        if filename.endswith(".c"):
            c_files.append(os.path.join(input_folder, filename))

    partial_compile = partial(compile_to_binary, output_folder=output_folder)
    with Pool(processes=number_of_processor_cores) as pool:
        pool.map(partial_compile, c_files)

    binary_files = [
        os.path.join(
            output_folder, os.path.basename(os.path.splitext(file)[0]) + ".out"
        )
        for file in c_files
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

    os.makedirs(output_dir_path, exist_ok=True)
    for entry in os.scandir(source_folder_path):
        if entry.name in (".", ".."):
            continue
        full_path = os.path.join(source_folder_path, entry.name)

        if entry.is_dir():
            collect_c_files(full_path, output_dir_path)
        elif entry.name.endswith(".c"):
            output_file_path = os.path.join(output_dir_path, entry.name)
            shutil.move(full_path, output_file_path)
