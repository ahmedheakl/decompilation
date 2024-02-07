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
    with asm_file_path.open("r", encoding="utf-8") as file:
        asm = file.read()
    return asm
