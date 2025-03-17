import tokenize
import token
from io import StringIO
import json
import os
from functools import lru_cache
from typing import List, Dict, Optional
import subprocess

@lru_cache(maxsize=32)
def json_to_dict(file_name: str) -> Optional[Dict]:
    """Load and cache JSON file content."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, file_name)

    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: File '{file_name}' not found in {current_dir}")
        return None
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in '{file_name}'")
        return None

def split_code(code: str) -> List[str]:
    """Split code by function blocks more accurately."""
    if not code:
        return []
    
    # More robust function splitting using brace counting
    functions = []
    current_function = []
    brace_count = 0
    
    for char in code:
        current_function.append(char)
        if char == '{':
            brace_count += 1
        elif char == '}':
            brace_count -= 1
            if brace_count == 0:
                functions.append(''.join(current_function))
                current_function = []
    print([f.strip() for f in functions if f.strip()])
    
    return [f.strip() for f in functions if f.strip()]

def import_file(file_json: str) -> Optional[List[str]]:
    global custom_code
    """Import and process JSON configuration file."""
    file_import = json_to_dict(file_json)
    if not file_import:
        return None
    
    try:
        importable = file_import['start']['import_custom']
        code = get_code(importable)
        if code:
            print('CODE',code)
            custom_code=code
            return 
        return None
    except KeyError as e:
        print(f"Error: Missing key in JSON structure: {e}")
        return None

def execute_code(code: str, language: str) -> Optional[str]:
    """Execute code in specified language and return output."""
    supported = {
        'python': ('python3', '.py'),
        'javascript': ('node', '.js'),
        'ruby': ('ruby', '.rb')
    }
    
    if language not in supported:
        print(f"Error: Unsupported language {language}")
        return None
        
    runner, ext = supported[language]
    temp_file = f"temp_execute{ext}"
    
    try:
        # Write code to temp file
        with open(temp_file, 'w') as f:
            f.write(code)
            
        # Execute code
        process = subprocess.run(
            [runner, temp_file],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        return process.stdout
        
    except subprocess.TimeoutExpired:
        print("Execution timed out after 30 seconds")
    except subprocess.CalledProcessError as e:
        print(f"Execution error: {e.stderr}")
    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        if os.path.exists(temp_file):
            os.remove(temp_file)
            
    return None

def get_code(file_name):
    # Get the directory of the current script
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, file_name)

    try:
        with open(file_path, 'r') as file:
            data = file.read()
        #print(f"Successfully loaded data from {file_name}:")
        #print(data)
        return data
    except FileNotFoundError:
        print(f"Error: The file '{file_name}' was not found in {current_dir}.")

# Define the conversion dictionary (custom language -> JavaScript), json_to_dict('code.json')
print('CODEsss',json_to_dict('code.json')['code'])
print('START',json_to_dict('code.json')['start'])
print('BUILD',json_to_dict('code.json')['build'])
print(import_file('code.json'))
conversion_dict = json_to_dict('code.json')['code']
'''{
    "def": "function",
    "print": "console.log",
    "True": "true",
    "False": "false",
    "None": "null",
    "#": "//"
}
'''
def custom_language_converter(code, conversion_dict):# convert the code to custom language
    converted_code = []  # To store the output as lines of code
    current_line = []
    indent_level = 0

    def transform(token_type, token_string):
        # Replace tokens based on the conversion dictionary
        if token_type == token.NAME and token_string in conversion_dict:
            return conversion_dict[token_string]
        return token_string  # Leave other tokens unchanged

    code_stream = StringIO(code)
    tokens = tokenize.generate_tokens(code_stream.readline)

    for tok in tokens:
        tok_type, tok_string, start, end, line = tok

        if tok_type in (token.NEWLINE, tokenize.NL):  # End of a logical line
            if current_line:
                formatted_line = "".join(current_line).strip()
                # Replace colons at the end of a line with opening braces
                if formatted_line.endswith(":"):
                    formatted_line = formatted_line[:-1] + " {"
                    indent_level += 1
                converted_code.append(("    " * indent_level) + formatted_line)
            current_line = []
        elif tok_type == token.INDENT:  # Handle increasing indentation
            indent_level += 1
        elif tok_type == token.DEDENT:  # Handle decreasing indentation
            indent_level -= 1
        elif tok_type == token.COMMENT:  # Preserve comments
            current_line.append(f" {tok_string}")
        elif tok_type == token.STRING:  # Preserve strings
            current_line.append(tok_string)
        else:
            # Transform tokens using the dictionary
            transformed = transform(tok_type, tok_string)
            if transformed not in {",", "(", ")", ";", "{"}:  # Add space before most tokens
                current_line.append(f" {transformed}")
            else:
                current_line.append(transformed)

    # Add the last line and close open blocks
    if current_line:
        formatted_line = "".join(current_line).strip()
        if formatted_line.endswith(":"):
            formatted_line = formatted_line[:-1] + " {"
            indent_level += 1
        converted_code.append(("    " * indent_level) + formatted_line)

    # Close any unclosed blocks
    while indent_level > 0:
        indent_level -= 1
        converted_code.append(("    " * indent_level) + "}")

    return "\n".join(converted_code)

# Example usage get_code('code.nnc')

python_code =get_code('code.nnc')
'''
func hi(name){
    printout('hi');
    error('errir');
    printout('done');
    //hello(name)
    if(name=='Ethan' and name !== 'jo') //'--' is and, '|' is or and not is '!'
    {
    printout('hi Ethan')
    }
    elif(name !== 'Ethan' and name !== 'jo')
    {
    printout('imposter')
    }
    else{
    printout('hi jo')
    }
}
hi('Ethan')
hi('jo')
hi('michal')

printout('complete')'''

################

"""
# This is a comment
def hello_world(){
    is_true = True
    print("Hello, world!")
    return None
}

hello_world()
"""


if __name__ == '__main__':
    code = get_code('code.nnc')
    #print(f"Original code loaded: {'yes' if code else 'no'}")
    #print(f"Code content:\n{code}")  # Debug original code
    
    if code:
        # Debug conversion dictionary
        #print(f"Conversion dictionary:\n{json.dumps(conversion_dict, indent=2)}")
        
        converted = custom_language_converter(code, conversion_dict)
        converted = converted.replace('!= =','!==').replace('== =','===')
        converted=custom_code+converted
        print('iunjh9uobko',custom_code)
        print(f"Converted JavaScript code:\n{converted}")

        if converted:
            # Write to file for inspection
            debug_file = "run.js"
            with open(debug_file, 'w') as f:
                f.write(converted)
               # print(f"Debug file written to: {debug_file}")
            
            # Execute with more detailed error handling
            output = execute_code(converted, 'javascript')
            if output:
                print(f"Success output:\n{output}")
            else:
                # Try direct Node.js execution for better error messages
                try:
                    result = subprocess.run(
                        ['node', debug_file], 
                        capture_output=True, 
                        text=True, 
                        check=False
                    )
                    print(f"Exit code: {result.returncode}")
                    print(f"Error output:\n{result.stderr}")
                except Exception as e:
                    print(f"Execution error: {str(e)}")
            
        else:
            print("Conversion failed")
            
        result = custom_language_converter(python_code, conversion_dict)
        if result:
            print("Converted Code as String:")
            print(result.replace('!= =','!==').replace('== =','==='))
        else:
            print("Python code conversion failed")