from parser_1 import Parser
from lexical_analyzer import tokenize
from Standarizing_AST.standarize_AST import AST



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
        print(ast)

        # Standardize the AST
        root_node = ast[0]  # Choose the first node as the root node
        ast_instance = AST(root_node)
        ast_instance.standardize()
        ast_instance.print()
    

        string_ast = parser.convert_ast_to_string_ast()
        for string in string_ast:
            print(string)

    except Exception as e:
        print(str(e))

if __name__ == "__main__":
    main()
