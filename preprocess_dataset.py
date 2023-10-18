from decompilation.decompile.preprocessing import preprocess
from pathlib import Path

AnghaBench_dataset_folder = Path("/home/mohanned/Work/AnghaBench")
input_folder = Path("/home/mohanned/Work/DataC")
output_folder = Path("/home/mohanned/Work/Binary")

if not input_folder.exists():
    input_folder.mkdir(parents=True, exist_ok=True)

if not output_folder.exists():
    output_folder.mkdir(parents=True, exist_ok=True)

preprocess.collect_c_files(AnghaBench_dataset_folder.as_posix(), input_folder.as_posix())
preprocess.preprcoess(input_folder.as_posix(), output_folder.as_posix(), 1000, 4, "att", "x86-64")
