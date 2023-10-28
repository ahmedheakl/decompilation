import json
from pathlib import Path
import re

path = Path("datasets/formatted/geeks_for_geeks_successful_test_scripts.jsonl")
# load the jsonl file as a dict
buffer = []
output = []
with path.open("r") as file:
    for line in file:
        data = json.loads(line)
        output.append(data["output"])
        data = data["input"]
        regex = ".*?(<_Z6f_gold.*?\n)<"
        found = re.search(regex, data, re.DOTALL)
        buffer.append(found.group(1))

# write the buffer to a file
with path.open("w") as file:
    for i, line in enumerate(buffer):
        # write to a file in one line the json dict from the buffer and the output
        # file.write(line+'\n')
        data = {"input": line, "output": output[i]}
        json_string = json.dumps(data)
        file.write(json_string + "\n")
