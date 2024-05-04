from Parser.parser_1 import Parser
from Lexer.lexical_analyzer import tokenize
from Standerizer.ast_factory import ASTFactory
from CSEM.csemachine import CSEMachine
from CSEM.cse_factory import CSEMachineFactory
# import inspect


def main():
    input_file = open("input.txt", "r")
    input_text = input_file.read()
    input_file.close()
    # Tokenize the input text
    tokens = tokenize(input_text)

    try:
        parser = Parser(tokens)
        ast_nodes = parser.parse()
        if ast_nodes is None:
            return


        # Print the generated AST
        # for node in ast:
        #     print(node)
    
        
        # Create an AST object with the root node
        # ast = AST(ast[0])
        # # Standardize the AST
        # ast.standardize()
        # ast.print_ast()
        
        print('''
              ========================================================
              |            Abstract Syntax Tree                      |
              ========================================================
              ''')
   
        string_ast = parser.convert_ast_to_string_ast()
        for string in string_ast:
            print(string)
            
        print('''\n
              ========================================================
              |            Standardized Abstract Syntax Tree         |
              ========================================================
              ''')
        ast_factory = ASTFactory()
        ast = ast_factory.get_abstract_syntax_tree(string_ast)
        ast.standardize()
        ast.print_ast()
        
        print('\n')
        
        cse_machine_factory = CSEMachineFactory()
        cse_machine = cse_machine_factory.get_cse_machine(ast)
        print('Output of the program: ', cse_machine.get_answer())


    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()
