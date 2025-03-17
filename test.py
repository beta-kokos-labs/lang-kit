import re
import json

def replace_with_json(code, json_string=None):
    # Sample JSON string if none provided
    json_string = json_string or '''
    {
        "x":"replaced_x",
        "y":"replaced_y"
    }
    '''
    
    # Parse the JSON string into a Python dictionary
    data = json.loads(json_string)
    
    # First pass: Replace keys with their corresponding values
    for key, value in data.items():
        print(f"Replacing key '{key}' with value '{value}'")
        code = replace_outside_quotes(code, key, value)
    
    # Second pass: Replace values with their corresponding keys
    for key, value in data.items():
        print(f"Replacing value '{value}' with key '{key}'")
        code = replace_outside_quotes(code, value, key)
    
    return code

def replace_outside_quotes(code, to_replace, replacement):
    # Regular expression to match strings inside single or double quotes
    string_pattern = r'".*?"|\'.*?\''
    
    # Regular expression to match the exact word
    word_pattern = rf'\b{re.escape(to_replace)}\b'
    
    # Split the code into parts: those inside quotes and everything else
    parts = re.split(f'({string_pattern})', code)
    
    # Apply the replacement only to the non-quoted parts
    for i in range(len(parts)):
        if not re.match(string_pattern, parts[i]):  # if it's not a quoted string
            parts[i] = re.sub(word_pattern, replacement, parts[i])
    
    # Join the parts back together
    return ''.join(parts)

# Example usage:
code = '''
x = 10  # This is some code
string1 = "This is a string with code x = 20"
y = 15  # Replace x outside quotes
replaced_y = 25  # This will be replaced with y
string2 = 'This is another string with code y = 30'
happy = True  # This is a boolean
replaced_x = 'test string'
'''

print("Original Code:")
print(code)

# Test with both key->value and value->key replacements
modified_code = replace_with_json(code, '''
    {
        "x":"replaced_x",
        "y":"replaced_y"
    }
    ''')

print("\nModified Code:")
print(modified_code)
