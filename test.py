import re
import json

def replace_with_json(code, json_string=None):
    # Sample JSON string
    json_string = '''
    {
        "x":"replaced_x",
        "y":"replaced_y"
    }
    '''
    
    # Parse the JSON string into a Python dictionary
    data = json.loads(json_string)

   ''' 
   for key, value in data.items():
        code = replace_outside_quotes(code, value, key)
    print(code)'''
    
    # Replace keys with their corresponding values
    for key, value in data.items():
        print(f"Key: {key}, Value: {value}")
        code = replace_outside_quotes(code, key, value)
    print(code)
    # Replace values with their corresponding keys

    # Convert the dictionary back to a JSON string
    #modified_json_string = code
    
    return code#modified_json_string


def replace_outside_quotes(code, to_replace, replacement):
    # Regular expression to match strings inside single or double quotes
    string_pattern = r'".*?"|\'.*?\''
    
    # Regular expression to match the key as a standalone word
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
string2 = 'This is another string with code y = 30'
happy = True  # This is a boolean
replace_x = 'test string'
'''

print("Original Code:")
print(code)

# Replace 'x' with 'replaced_x' outside of strings
modified_code = replace_with_json(code, '''
    {
        "x":"replaced_x",
        "y":"replaced_y"
    }
    ''')

print("\nModified Code:")
print(modified_code)
