import json
import os
import rstr
import re
from xeger import Xeger

def remove_surrogates(value):
    if isinstance(value, str):
        return re.sub(r'[\ud800-\udfff]', '', value)
    return value

# Function to generate an invalid string that does not match a given pattern
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

    print("Failed to generate an invalid string within the max attempts.")
    return None

# JSON file name
file_name = 'uniq-regexes-8.json'

# Initialize an empty list to store patterns with their valid and invalid strings
patterns_with_strings = []

x = Xeger()

# Open the file and load each line as a JSON object
with open(file_name, 'r') as f:
    for line in f:
        json_obj = json.loads(line.strip())  # Parse each line as JSON
        pattern = json_obj.get('pattern')   # Extract the pattern
        pattern = remove_surrogates(pattern)
        valid_string = None
        invalid_string = None
        # Process only if the pattern is a string
        if isinstance(pattern, str):
            try:
                # Generate a valid string from the regex
                
                valid_string = x.xeger(pattern)

                # Generate an invalid string by slightly modifying the valid one
                invalid_string = generate_invalid_string(pattern)

                # Add the pattern with valid and invalid strings to the list
                
            except Exception as e:
                # Skip patterns that cannot be processed
                print(f"Skipping pattern due to error: {pattern}, Error: {e}")

            patterns_with_strings.append({
                    'Pattern': pattern,
                    'Valid String': valid_string,
                    'Invalid String': invalid_string
                })

# Save the list of patterns with strings to a JSON file
output_file = 'regexes_with_strings.json'
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(patterns_with_strings, f, ensure_ascii=False, indent=4)