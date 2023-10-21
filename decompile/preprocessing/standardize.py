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
    section_start_text = "Disassembly of section"
    length_memory_address_format_example = len(
        "48 c7 45 f8 00 00 00    "
    )  # from objdump output, need to know length to remove it from start of instruction.
    standardized_asm_buffer = []

    with asm_file_path.open("r", encoding="utf-8") as file:
        for line in file.readlines()[4:]:
            line = line.strip()

            if not line or line.startswith(section_start_text):
                continue

            # TODO: Use a regex to find "<section_name>:" or detect prev text
            if line.startswith("<"):
                standardized_asm_buffer.append(line + "\n")

            else:
                line = line[
                    length_memory_address_format_example - 2 :
                ]  # remove memory address from start of instruction.
                if not line:
                    continue
                line = re.sub(r"\s+", " ", line).strip()
                line = " , ".join(line.split(","))
                if "#" in line:
                    # add a ; before the hash to make it a comment
                    line = re.sub("#", "; #", line)
                else:
                    line = line + " ;"
                standardized_asm_buffer.append(line + "\n")
    ret = "".join(standardized_asm_buffer)
    return ret
