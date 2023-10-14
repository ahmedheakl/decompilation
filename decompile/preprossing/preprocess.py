"""Process the C code"""
import os
import subprocess
import shutil

C_CODE_FOLDER = "D:\Work\Research paper\DatasetC"
ASSEMBLY_FOLDER = "D:\Work\Research paper\DatasetAO3"
SOURCE_FOLDER = "D:\Work\Research paper\AnghaBench-master"


def compile_to_assembly(c_code_file: str, output_file: str) -> bool:
    """Compile C code to assembly.

    Args:
        c_code_file_path (str): Path to C code file
        output_file_path (str): Path to C code file

    Returns:
        bool: Indicates whether the compilation was successful
    """
    try:
        subprocess.run(["gcc", "-S", "-O3", c_code_file, "-o", output_file], check=True)
        return True
    except subprocess.CalledProcessError:
        return False


def compile_folder() -> None:
    """Compile C code"""
    if not os.path.exists(ASSEMBLY_FOLDER):
        os.makedirs(ASSEMBLY_FOLDER)
    for root, _, files in os.walk(C_CODE_FOLDER):
        for file in files:
            if not file.endswith(".c"):
                continue

            c_code_file = os.path.join(root, file)
            assembly_file = os.path.join(
                ASSEMBLY_FOLDER, os.path.splitext(file)[0] + ".s"
            )

            if not compile_to_assembly(c_code_file, assembly_file):
                print(f"Something went wrong with {c_code_file}")


def collect_c_files(source_folder: str, output_dir: str) -> None:
    """Collect all C files into one folder

    Args:
        source_folder (str): Folder containing all source files
        output_dir (str): Output folder for binary code
    """

    try:
        os.makedirs(output_dir, exist_ok=True)
        for entry in os.scandir(source_folder):
            if entry.name in (".", ".."):
                continue
            full_path = os.path.join(source_folder, entry.name)

            if entry.is_dir():
                collect_c_files(full_path, output_dir)
            elif entry.name.endswith(".c"):
                output_file_path = os.path.join(output_dir, entry.name)
                shutil.move(full_path, output_file_path)

    except Exception as e:
        print(f"An error occurred: {e}")
