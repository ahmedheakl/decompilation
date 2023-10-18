"""Process the C code"""
import os
import subprocess
import shutil
from multiprocessing import Pool

folder_path = "/home/mohanned/Work/DataC"
output_folder = "/home/mohanned/Work/Binary"

def compile_to_binary(file_path: str) -> None:
    """
        Converting C code files into binary files
        
        Args:
        file_path (str): It's the path for the C code file being compiled
    """
    binary_file = os.path.splitext(file_path)[0]
    binary_file = binary_file[::-1]
    EDIT = ""
    for c in binary_file:
        if(c == '/'):
            break
        EDIT += c
    EDIT = EDIT[::-1]
    out_file = output_folder + "/" + EDIT + ".out"

    assemble_command = f"gcc -c {file_path} -o {out_file}"

    try:
        subprocess.run(assemble_command, check=True, shell=True)
        print(f"Assembly successful. Binary machine code saved as {out_file}")
    except subprocess.CalledProcessError as e:
        print(f"Assembly failed with error:\n{e}")

def disassemble_to_assembly(binary_file: str) -> None:
    """
        Disassembling binary files
        
        Args:
        file_path (str): It's the path for the binary file being disassembled
    """
    assembly_file = os.path.splitext(binary_file)[0] + ".s"
    with open(assembly_file, "w") as assembly_file:
        subprocess.run(["objdump", "-d", "-M", "att", "-M", "x86-64", "--no-addresses", binary_file], stdout=assembly_file)


def preprcoess(number_of_samples):
    """
        The process of converting C code files into specific artichture of assembly

        Args:
            number_of_samples (int): It's the number of data samples that will used for training 
    """

    c_files = []
    for filename in os.listdir(folder_path):
        if len(c_files) == number_of_samples:
            break

        if filename.endswith(".c"):
            c_files.append(os.path.join(folder_path, filename))

    with Pool(processes=4) as pool:
        pool.map(compile_to_binary, c_files)

    binary_files = [os.path.join(output_folder, os.path.basename(os.path.splitext(file)[0]) + ".out") for file in c_files]
    with Pool(processes=4) as pool:
        pool.map(disassemble_to_assembly, binary_files)


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
