from parser_1 import Parser
from lexical_analyzer import tokenize
from Standarizing_AST.standarize_AST import AST
from Standarizing_AST.AST_node import ASTNode
from Standarizing_AST.AST_node_type import ASTNodeType



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
            print("Failed to generate AST. Parsing process returned None.")
            return

        # Print the generated AST
        # for node in ast:
        #     print(node)
        # Standardize the AST
        
        
        
        ast_standardizer = AST(ast)
        ast_standardizer.standardize()

        # Print the standardized AST
        print("Standardized AST:")
        ast_standardizer.print()

        
        


        # string_ast = parser.convert_ast_to_string_ast()
        # for string in string_ast:
        #     print(string)

    except Exception as e:
        print(str(e))

if __name__ == "__main__":
    main()
