"""Testing Standardization of Assembly Files"""
from pathlib import Path
from decompile.preprocessing.standardize import standardize_asm_file

TESTIING_DATA_FOLDER = Path("tests/tests_data/preprocessing")


def test_standardize():
    with open(
        TESTIING_DATA_FOLDER / "standardize_test_output_1.s",
        "r",
        encoding="utf-8",
    ) as file:
        output_text = file.read()
    assert (
        standardize_asm_file(
            "tests/tests_data/preprocessing/standardize_test_input_1.s"
        )
        == output_text
    )
