"""This module was specefically made to delete the comments in the source cpp files
 of the geeks for geeks dataset. THIS SCRIPT MUST FOLLOW delete_comments.py for correct use."""
import sys
from pathlib import Path


def main():
    """Main entry point for deleting comments script"""
    path = Path("datasets/raw/geeks_for_geeks_successful_test_scripts/cpp")
    for file_path in path.iterdir():
        lines = []
        found_main = False
        with file_path.open("r", encoding="utf-8") as source_file:
            for line in source_file:
                if line.strip().startswith("//") or found_main or not line.strip():
                    continue
                if line.startswith("int main()"):
                    found_main = True
                lines.append(line)

        if lines:
            with file_path.open("w", encoding="utf-8") as source_file:
                source_file.write("".join(lines).strip() + "\n")
            print(f"Finished commenting main function in {file_path.name}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
