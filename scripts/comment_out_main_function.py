"""This script will comment out the main function in all the cpp files
 in the geeks_for_geeks dataset except for return 0."""
from pathlib import Path
import sys


# TODO: make the path variable a cli argument
def main() -> int:
    """Main entry point for commenting main func script"""
    path = Path("datasets/raw/geeks_for_geeks_successful_test_scripts/cpp")
    # iterate over all .cpp files in path directory
    for file_path in path.iterdir():
        lines = None
        with file_path.open("r", encoding="utf-8") as source_file:
            lines = source_file.read()
            lines = lines.replace("int main()", "int main(){return 0;}\n/*int main()")
            lines = lines + "*/"
        if lines is not None:
            with file_path.open("w", encoding="utf-8") as source_file:
                source_file.write(lines)
        print(f"Finished commenting main function in {file_path.name}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
