"""Standardize assembly output from objdump command."""

import re
from pathlib import Path
from typing import Union

def standardize_objdump_asm_file(asm_file_path: Union[Path, str]) -> str:
    """Standardize asm file.

    Args:
        asm_file_path(str): path to asm file.

    Returns:
        str: standardized asm file as text.
    """
    asm_file_path = Path(asm_file_path)
    function_found = 0
    symbol = "<f_gold.*>"
    standardized_asm_buffer = []

    with asm_file_path.open("r", encoding="utf-8") as file:
        for line in file.readlines()[5:]:
            line = line.rstrip()
            # skip empty lines
            if not line:
                continue
            # found function start address
            if re.search(r"^[0-9a-fA-F]{16} " + symbol, line):
                function_found = 1
                continue
            # after function start address comes function signature
            if function_found == 1:
                standardized_asm_buffer.append(line + "\n")
                function_found = 2
            # after function signature comes the assembly code
            elif function_found == 2:
                if re.search(r"endbr64", line):
                    continue
                # if we find a new function, we stop
                if re.search(r"^[0-9a-fA-F]{16} <.*>:$", line):
                    break
                line = re.sub(r"\s+", " ", line).strip()
                line = " , ".join(line.split(","))
                line = "\t" + line + " ;\n"
                standardized_asm_buffer.append(line)

    ret = "".join(standardized_asm_buffer)
    return ret


def standardize_gcc_asm_output(asm_file_path: Union[Path, str]) -> str:
    """Standardize asm file.

    Args:
        asm_file_path(str): path to asm file.

    Returns:
        str: standardized asm file as text.
    """
    asm_file_path = Path(asm_file_path)
    func_pattern = r"[^\n]+:\n[^\n]+:\n\s\.cfi_startproc.+?\.cfi_endproc"
    with asm_file_path.open("r", encoding="utf-8") as file:
        asm = file.read()
        asm_func = re.search(func_pattern, asm, re.DOTALL)
        if asm_func is None:
            print(f"Failed to find function in {asm_file_path}")
            raise ValueError(f"Failed to find function in {asm_file_path}")
        asm_func = asm_func.group(0)
        lines = asm_func.split("\n")
        buffer = []
        for line in lines:
            stripped_line = line.strip()
            if not stripped_line or stripped_line.startswith(".cfi") or stripped_line.startswith("endbr64"):
                continue
            buffer.append(line)

    return "\n".join(buffer)
