from parser_1 import Parser
from lexical_analyzer import tokenize
from Standerizer.ast import AST
from Standerizer.node import Node

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
        
        
        
        # Create an AST object with the root node
        ast[0] = Node()
        ast_obj = AST(ast[0])

        # Standardize the AST
        ast_obj.standardize()

        # Print the standardized AST
        ast_obj.print_ast()
        
        

        string_ast = parser.convert_ast_to_string_ast()
        for string in string_ast:
            print(string)

    except Exception as e:
        print(str(e))

if __name__ == "__main__":
    main()
