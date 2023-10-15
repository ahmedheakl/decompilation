"""Standardize assembly output from objdump command."""
import re


def standardize_asm_file(asm_file_path: str) -> str:
    """Standardize asm file.

    Args:
        asm_file_path(str): path to asm file.

    Returns:
        str: standardized asm file as text."""
    section_start_text = "Disassembly of section"
    memory_address_format_example = "48 c7 45 f8 00 00 00    "
    instruction_split_regex = " "
    standardized_asm_buffer = ""
    with open(asm_file_path, "r") as f:
        for line in f.readlines()[4:]:
            line = line.strip()
            if not line or line.startswith(section_start_text):
                continue
            if line.startswith("<"):
                standardized_asm_buffer += line + "\n"
            else:
                line = line[len(memory_address_format_example) - 2 :]
                if not line:
                    continue
                components = re.split(instruction_split_regex, line)
                components = [c for c in components if c]
                line = " ".join(components)
                line = " , ".join(line.split(","))
                standardized_asm_buffer += line + " ;" + "\n"
    return standardized_asm_buffer
