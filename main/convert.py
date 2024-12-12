import json
import subprocess
import re
import os
# Define a function to load JSON from a file and convert it to a dictionary

def json_to_dict(file_name):
    # Get the directory of the current script
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, file_name)

    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
        print(f"Successfully loaded data from {file_name}:")
        print(data)
        return data
    except FileNotFoundError:
        print(f"Error: The file '{file_name}' was not found in {current_dir}.")
    except json.JSONDecodeError:
        print(f"Error: The file '{file_name}' contains invalid JSON.")

# Example Usage
#load_json_file("code.json")

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


# Define text replacements
def build():
    with open('scripts.js', 'w') as js_file:
        js_file.write(js_code)
replacements={
}
def convert(code): 
    # Example usage
      # Replace with your JSON file's path
    dictionary = json_to_dict(file_path)
    print(dictionary)

    if dictionary:
        print("JSON successfully converted to dictionary:")
        print(dictionary)
        x=dictionary['code'].keys()#['og']
        print(x)
        for item in x:
            replacements[item]=dictionary['code'][item]['og']

    # Replace text in the code
        replaced_code = replace_text_in_code(code, replacements)

    # Split the code into statements
        split_statements = split_code_by_semicolon(replaced_code)

        # Print each statement
        print("Modified and Split Statements:")
        for statement in split_statements:
            print(statement)
        return replaced_code



def create_js_file(file_name_js, js_code):
    """
    Creates a JavaScript file with the provided code.
    
    :param file_name: Name of the JavaScript file to create
    :param js_code: JavaScript code to write into the file
    """
    with open(file_name_js, 'w') as js_file:
        js_file.write(js_code)
    print(f"JavaScript file '{file_name_js}' created successfully.")

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

if __name__ == '__main__':
    file_path = 'code.json'
    custom_code = """
    def hi(name){
        print('hi');
        error('errir');
        print('done');
        //hello(name)
        if(name=='Ethan' and name not== 'jo'){
        print('hi Ethan')
        }elif(name not== 'Ethan' and name not== 'jo'){
        print('imposter')}else{
        print('hi jo')}
    }
    hi('Ethan')
    hi('jo')
    hi('michal')
    """
    js_file_name = "run.js"
    js_code = convert(custom_code)
    # Create and run the JavaScript file
    create_js_file(js_file_name, js_code)
    run_js_file(js_file_name)
    #build()
###########################################################

import tokenize
import token
from io import StringIO

# Define the conversion dictionary (custom language -> JavaScript)
conversion_dict = {
    "def": "function",
    "print": "console.log",
    "True": "true",
    "False": "false",
    "None": "null"
    # Add more mappings as needed
}

def custom_language_converter(code, conversion_dict):
    converted_code = []  # To store the output as a list

    def transform(token_type, token_string):
        # Replace tokens based on the conversion dictionary
        if token_type == token.NAME and token_string in conversion_dict:
            return conversion_dict[token_string]
        return token_string  # Leave other tokens unchanged

    code_stream = StringIO(code)
    tokens = tokenize.generate_tokens(code_stream.readline)

    for tok in tokens:
        tok_type, tok_string, start, end, line = tok

        # Preserve comments and strings
        if tok_type in (token.COMMENT, token.STRING):
            converted_code.append(tok_string)
        else:
            # Transform tokens using the dictionary
            transformed = transform(tok_type, tok_string)
            converted_code.append(transformed)

    return converted_code

# Example usage
python_code = """
# This is a comment
def hello_world():
    is_true = True
    print("Hello, world!")
    return None
"""

result = custom_language_converter(python_code, conversion_dict)
print("Converted Code as List:")
print(result)
