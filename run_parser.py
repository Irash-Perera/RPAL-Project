import sys
import os
from dotenv import load_dotenv

load_dotenv()

project_dir = os.getenv("PROJECT_DIR")


sys.path.append(project_dir)

from parser_1 import Parser
from lexical_analyzer import tokenize


def main():
    input_file = open("input.txt", "r")
    input_text = input_file.read()
    input_file.close()
    # Tokenize the input text
    tokens = tokenize(input_text)

    try:
        parser = Parser(tokens)
        ast = parser.parse()
        if ast is None:
            return


        # Print the generated AST
        # for node in ast:
        #     print(node)

        string_ast = parser.convert_ast_to_string_ast()
        for string in string_ast:
            print(string)

    except Exception as e:
        print(str(e))

if __name__ == "__main__":
    main()
