"""Standardize assembly output from objdump command."""
import re
from pathlib import Path
from typing import Union


def standardize_asm_file(asm_file_path: Union[Path, str]) -> str:
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
            if not line:
                continue

            if re.search(r"^[0-9a-fA-F]{16} " + symbol, line):
                function_found = 1
                continue

            if function_found == 1:
                standardized_asm_buffer.append(line + "\n")
                function_found = 2

            elif function_found == 2:
                if re.search(r"endbr64", line):
                    continue
                if re.search(r"^[0-9a-fA-F]{16} <.*>:$", line):
                    break
                line = re.sub(r"\s+", " ", line).strip()
                line = " , ".join(line.split(","))
                line = "\t" + line + " ;\n"
                standardized_asm_buffer.append(line)
                # if "#" in line:
                #     # add a ; before the hash to make it a comment
                #     line = re.sub("#", "; #", line)
    ret = "".join(standardized_asm_buffer)
    return ret
