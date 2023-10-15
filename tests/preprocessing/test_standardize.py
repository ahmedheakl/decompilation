from decompile.preprossing.standardize import standardize_asm_file


def test_standardize():
    with open("tests/tests_data/preprocessing/standardize_test_output_1.s", "r") as f:
        output_text = f.read()
    assert (
        standardize_asm_file(
            "tests/tests_data/preprocessing/standardize_test_input_1.s"
        )
        == output_text
    )
