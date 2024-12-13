import tokenize
import token
from io import StringIO

# Define the conversion dictionary (custom language -> JavaScript)
conversion_dict = {
    "def": "function",
    "print": "console.log",
    "True": "true",
    "False": "false",
    "None": "null",
    "#": "//"
}

def custom_language_converter(code, conversion_dict):
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

# Example usage
python_code = """
# This is a comment
def hello_world(){
    is_true = True
    print("Hello, world!")
    return None
}

hello_world()
"""

result = custom_language_converter(python_code, conversion_dict)
print("Converted Code as String:")
print(result)
