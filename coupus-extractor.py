import pandas as pd
import json
import os
import rstr
import random
from xeger import Xeger
import re

def generate_invalid_string(pattern, max_attempts=1000):
    compiled_pattern = re.compile(pattern)
    attempts = 0

    while attempts < max_attempts:
        # Generate a random string with rstr
        generated_string = rstr.rstr("[ -~]{10}")  # Generate a random string with printable ASCII characters

        # Check if the generated string does not match the regex pattern
        if not compiled_pattern.fullmatch(generated_string):
            return generated_string

        attempts += 1

    raise ValueError("Failed to generate an invalid string within the max attempts.")


# JSON file name
file_name = 'uniq-regexes-8.json'

# Initialize an empty list to store patterns
regex_patterns = []

# Open the file and load each line as a JSON object
with open(file_name, 'r') as f:
    for line in f:
        json_obj = json.loads(line.strip())  # Parse each line as JSON
        pattern = json_obj.get('pattern')   # Extract the pattern
        
        # Add to list only if the pattern is a string
        if isinstance(pattern, str):
            regex_patterns.append(pattern)

# Create a DataFrame with the initial patterns
df = pd.DataFrame({
    'Pattern': regex_patterns,
    'Valid String': [None] * len(regex_patterns),
    'Invalid String': [None] * len(regex_patterns)
})
# x = Xeger()

# # Generate valid and invalid strings for each regex pattern
# for index, pattern in enumerate(regex_patterns):
#     try:
#         # Generate a valid string from the regex
#         valid_string = x.xeger(pattern)
#         df.at[index, 'Valid String'] = valid_string
        
#         # Generate an invalid string by slightly modifying the valid one
#         invalid_string = generate_invalid_string(pattern)
#         df.at[index, 'Invalid String'] = invalid_string
#     except Exception as e:
#         # Skip patterns that cannot be processed
#         print(f"Skipping pattern due to error: {pattern}, Error: {e}")

# Save the DataFrame to a JSON file
df.to_json(os.path.join("regexes_with_strings.json"))