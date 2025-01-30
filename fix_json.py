import json

import json

# Input and output file names
input_file = "books.json"  # Path to the uploaded JSON file
output_file = "fixed_books.json"  # Path to save the corrected JSON

# Read the improperly formatted JSON data
with open(input_file, 'r', encoding='utf-8') as file:
    # Read all lines and strip whitespace
    lines = [line.strip() for line in file if line.strip()]

# Combine the lines into a single JSON array
json_array = '[' + ','.join(lines) + ']'

# Parse the combined JSON array to ensure it's valid
try:
    fixed_data = json.loads(json_array)
except json.JSONDecodeError as e:
    print(f"Error decoding JSON: {e}")
    exit(1)

# Write the fixed JSON data to a new file
with open(output_file, 'w', encoding='utf-8') as file:
    json.dump(fixed_data, file, ensure_ascii=False, indent=4)

print(f"Fixed JSON data has been written to {output_file}")

# Usage


