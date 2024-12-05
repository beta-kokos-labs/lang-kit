import json

# Define a function to load JSON from a file and convert it to a dictionary
def json_to_dict(file_path):
    try:
        with open(file_path, 'r') as json_file:
            data = json.load(json_file)  # Load the JSON data
        return data  # Return as a dictionary
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' does not exist.")
    except json.JSONDecodeError:
        print(f"Error: The file '{file_path}' contains invalid JSON.")

# Example usage
file_path = 'code.json'  # Replace with your JSON file's path
dictionary = json_to_dict(file_path)

if dictionary:
    print("JSON successfully converted to dictionary:")
    print(dictionary)

x=dictionary['code'].keys()#['og']
print(x)

import re

# Function to split code by semicolons
def split_code_by_semicolon(code):
    # Split the input code by semicolons and strip whitespace
    statements = [stmt.strip() for stmt in code.split(';') if stmt.strip()]
    return statements

# Function to replace certain text in code
def replace_text_in_code(code, replacements):
    for old_text, new_text in replacements.items():
        code = code.replace(old_text, new_text)
    return code

# Example custom code
custom_code = """
def hi(){
    print('hi');
    error('errir');
    print('done');
}
hi()
"""

# Define text replacements
'''replacements = {
    "print": "console.log",
    "error": "console.error",
    "def": "function"
}'''

replacements={
}

for item in x:
    replacements[item]=dictionary['code'][item]['og']

# Replace text in the code
replaced_code = replace_text_in_code(custom_code, replacements)

# Split the code into statements
split_statements = split_code_by_semicolon(replaced_code)

# Print each statement
print("Modified and Split Statements:")
for statement in split_statements:
    print(statement)

import subprocess

def create_js_file(file_name, js_code):
    """
    Creates a JavaScript file with the provided code.
    
    :param file_name: Name of the JavaScript file to create
    :param js_code: JavaScript code to write into the file
    """
    with open(file_name, 'w') as js_file:
        js_file.write(js_code)
    print(f"JavaScript file '{file_name}' created successfully.")

def run_js_file(file_name):
    """
    Runs a JavaScript file using Node.js.
    
    :param file_name: Name of the JavaScript file to run
    """
    try:
        result = subprocess.run(['node', file_name], capture_output=True, text=True, check=True)
        print("Output from JavaScript file:")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error running JavaScript file: {e}")
        print("Error Output:")
        print(e.stderr)

# Example usage
js_file_name = "example.js"
js_code = replaced_code
# Create and run the JavaScript file
create_js_file(js_file_name, js_code)
run_js_file(js_file_name)
