#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <unordered_map>
#include <regex>

// Function to read a file and return its content as a string
std::string get_file_content(const std::string& file_name) {
    std::ifstream file(file_name);
    if (!file.is_open()) {
        throw std::runtime_error("Error: Could not open file " + file_name);
    }
    std::ostringstream content;
    content << file.rdbuf();
    return content.str();
}

// Function to load a JSON-like dictionary from a file
std::unordered_map<std::string, std::string> load_conversion_dict(const std::string& file_name) {
    std::ifstream file(file_name);
    if (!file.is_open()) {
        throw std::runtime_error("Error: Could not open file " + file_name);
    }

    std::unordered_map<std::string, std::string> conversion_dict;
    std::string line;
    while (std::getline(file, line)) {
        size_t colon_pos = line.find(":");
        if (colon_pos != std::string::npos) {
            std::string key = line.substr(0, colon_pos);
            std::string value = line.substr(colon_pos + 1);

            // Remove quotes and trailing commas
            key.erase(std::remove(key.begin(), key.end(), '\"'), key.end());
            value.erase(std::remove(value.begin(), value.end(), '\"'), value.end());
            value.erase(std::remove(value.begin(), value.end(), ','), value.end());

            conversion_dict[key] = value;
        }
    }
    return conversion_dict;
}

// Custom language converter function
std::string custom_language_converter(const std::string& code, const std::unordered_map<std::string, std::string>& conversion_dict) {
    std::string converted_code = code;

    // Replace tokens based on the conversion dictionary
    for (const auto& [key, value] : conversion_dict) {
        std::regex token_regex("\\b" + key + "\\b"); // Match whole words only
        converted_code = std::regex_replace(converted_code, token_regex, value);
    }

    // Fix syntax issues like replacing 'and' with '&&' and other logical operators
    std::unordered_map<std::string, std::string> logical_operators = {
        {"and", "&&"},
        {"or", "||"},
        {"not", "!"}
    };

    for (const auto& [key, value] : logical_operators) {
        std::regex token_regex("\\b" + key + "\\b");
        converted_code = std::regex_replace(converted_code, token_regex, value);
    }

    return converted_code;
}

int main() {
    try {
        // Load the conversion dictionary from a JSON-like file
        auto conversion_dict = load_conversion_dict("code.json");

        // Read the input code from a file
        std::string input_code = get_file_content("code.nnc");

        // Convert the custom language code
        std::string converted_code = custom_language_converter(input_code, conversion_dict);

        // Output the converted code
        std::cout << "Converted Code:" << std::endl;
        std::cout << converted_code << std::endl;

    } catch (const std::exception& e) {
        std::cerr << e.what() << std::endl;
    }

    return 0;
}
