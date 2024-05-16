from enum import Enum
from Lexer.lexical_analyzer import TokenType, MyToken

class NodeType(Enum):
    let = 1
    fcn_form = 2
    identifier = 3
    integer = 4
    string = 5
    where = 6
    gamma = 7
    lambda_expr = 8
    tau = 9
    rec = 10
    aug = 11
    conditional = 12
    op_or = 13
    op_and = 14
    op_not = 15
    op_compare = 16
    op_plus = 17
    op_minus = 18
    op_neg = 19
    op_mul = 20
    op_div = 21
    op_pow = 22
    at = 23
    true_value = 24
    false_value = 25
    nil = 26
    dummy = 27
    within = 28
    and_op = 29
    equal = 30
    comma = 31
    empty_params = 32


class Node:
    def __init__(self, node_type, value, children):
        self.type = node_type
        self.value = value
        self.no_of_children = children

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.ast = []
        self.string_ast = []

    def parse(self):
        self.tokens.append(MyToken(TokenType.END_OF_TOKENS, ""))  # Add an End Of Tokens marker
        self.E()  # Start parsing from the entry point
        if self.tokens[0].type == TokenType.END_OF_TOKENS:
            return self.ast
        else:
            print("Parsing Unsuccessful!...........")
            print("REMAINIG UNPARSED TOKENS:")
            for token in self.tokens:
                print("<" + str(token.type) + ", " + token.value + ">")
            return None

    def convert_ast_to_string_ast(self):
        dots = ""
        stack = []

        while self.ast:
            if not stack:
                if self.ast[-1].no_of_children == 0:
                    self.add_strings(dots, self.ast.pop())
                else:
                    node = self.ast.pop()
                    stack.append(node)
            else:
                if self.ast[-1].no_of_children > 0:
                    node = self.ast.pop()
                    stack.append(node)
                    dots += "."
                else:
                    stack.append(self.ast.pop())
                    dots += "."
                    while stack[-1].no_of_children == 0:
                        self.add_strings(dots, stack.pop())
                        if not stack:
                            break
                        dots = dots[:-1]
                        node = stack.pop()
                        node.no_of_children -= 1
                        stack.append(node)

        # Reverse the list
        self.string_ast.reverse()
        return self.string_ast

    def add_strings(self, dots, node):
        if node.type in [NodeType.identifier, NodeType.integer, NodeType.string, NodeType.true_value,
                         NodeType.false_value, NodeType.nil, NodeType.dummy]:
            self.string_ast.append(dots + "<" + node.type.name.upper() + ":" + node.value + ">")
        elif node.type == NodeType.fcn_form:
            self.string_ast.append(dots + "function_form")
        else:
            self.string_ast.append(dots + node.value)

    # Expressions 
                
    # E	->'let' D 'in' E		=> 'let'
    # 	->'fn' Vb+ '.' E		=> 'lambda'
    # 	->Ew;

    def E(self):
        if self.tokens:  # Ensure tokens list is not empty
            token = self.tokens[0]
            if hasattr(token, 'type') and hasattr(token, 'value'):  # Check if token has type and value attributes
                if token.type == TokenType.KEYWORD and token.value in ["let", "fn"]:
                    # print('Entering if block in E...')
                    if token.value == "let":
                        # print('Entering let block...')
                        self.tokens.pop(0)  # Remove "let"
                        self.D()
                        if self.tokens[0].value != "in":
                            print("Parse error at E : 'in' Expected")
                        self.tokens.pop(0)  # Remove "in"
                        self.E()
                        self.ast.append(Node(NodeType.let, "let", 2))
                    else:
                        self.tokens.pop(0)  # Remove "fn"
                        n = 0
                        while self.tokens and (self.tokens[0].type == TokenType.IDENTIFIER or self.tokens[0].value == "("):
                            self.Vb()
                            n += 1
                        if self.tokens and self.tokens[0].value != ".":
                            print("Parse error at E : '.' Expected")
                        if self.tokens:
                            self.tokens.pop(0)  # Remove "."
                            self.E()
                            self.ast.append(Node(NodeType.lambda_expr, "lambda", n + 1))
                else:
                    # print('Entering else block...')
                    self.Ew()
            else:
                print("Invalid token format.")
        else:
            print("Tokens list is empty.")


    # Ew	->T 'where' Dr			=> 'where'
    # 		->T;

    def Ew(self):
        self.T()
        if self.tokens[0].value == "where":
            self.tokens.pop(0)  # Remove "where"
            self.Dr()
            self.ast.append(Node(NodeType.where, "where", 2))

    # Tuple Expressions

    # T 	-> Ta ( ',' Ta )+ => 'tau'
    # 		-> Ta ;
            
    def T(self):
        self.Ta()
        n = 1
        while self.tokens[0].value == ",":
            self.tokens.pop(0)  # Remove comma(,)
            self.Ta()
            n += 1
        if n > 1:
            self.ast.append(Node(NodeType.tau, "tau", n))

    '''
    # Ta 	-> Ta 'aug' Tc => 'aug'
    # 		-> Tc ;
    Avoid left recursion by converting the grammar to right recursion
    Ta -> Tc ('aug' Tc)*
    '''
    def Ta(self):
        self.Tc()
        while self.tokens[0].value == "aug":
            self.tokens.pop(0)  # Remove "aug"
            self.Tc()
            self.ast.append(Node(NodeType.aug, "aug", 2))

    '''
    Tc 	-> B '->' Tc '|' Tc => '->'
     		-> B ;
    '''    
    def Tc(self):
        self.B()
        if self.tokens[0].value == "->":
            self.tokens.pop(0)  # Remove '->'
            self.Tc()
            if self.tokens[0].value != "|":
                print("Parse error at Tc: conditional '|' expected")
                # return
            self.tokens.pop(0)  # Remove '|'
            self.Tc()
            self.ast.append(Node(NodeType.conditional, "->", 3))

    # Boolean Expressions
    '''
    # B 	-> B 'or' Bt 	=> 'or'
    #     -> Bt ;	
    
    B -> Bt ('or' Bt)*
    '''
    def B(self):
        self.Bt()
        while self.tokens[0].value == "or":
            self.tokens.pop(0)  # Remove 'or'
            self.Bt()
            self.ast.append(Node(NodeType.op_or, "or", 2))

    '''
    # Bt	-> Bt '&' Bs => '&'
    # 			-> Bs ;
    
    Bt -> Bs ('&' Bs)*
    '''
    def Bt(self):
        self.Bs()
        while self.tokens[0].value == "&":
            self.tokens.pop(0)  # Remove '&'
            self.Bs()
            self.ast.append(Node(NodeType.op_and, "&", 2))

    # Bs	-> 'not' Bp => 'not'
    # 		-> Bp ;

    def Bs(self):
        if self.tokens[0].value == "not":
            self.tokens.pop(0)  # Remove 'not'
            self.Bp()
            self.ast.append(Node(NodeType.op_not, "not", 1))
        else:
            self.Bp()

    #  Bp 	-> A ('gr' | '>' ) A => 'gr'
    # 			-> A ('ge' | '>=') A => 'ge'
    # 			-> A ('ls' | '<' ) A => 'ls'
    # 			-> A ('le' | '<=') A => 'le'
    # 			-> A 'eq' A => 'eq'
    # 			-> A 'ne' A => 'ne'
    # 			-> A ;
            

    def Bp(self):
        self.A()
        token = self.tokens[0]
        if token.value in [">", ">=", "<", "<=", "gr", "ge", "ls", "le", "eq", "ne"]:
            self.tokens.pop(0)
            self.A()
            if token.value == ">":
                self.ast.append(Node(NodeType.op_compare, "gr", 2))
            elif token.value == ">=":
                self.ast.append(Node(NodeType.op_compare, "ge", 2))
            elif token.value == "<":
                self.ast.append(Node(NodeType.op_compare, "ls", 2))
            elif token.value == "<=":
                self.ast.append(Node(NodeType.op_compare, "le", 2))
            else:
                self.ast.append(Node(NodeType.op_compare, token.value, 2))

    # Arithmetic Expressions

    # A 	-> A '+' At => '+'
    # 		-> A '-' At => '-'
    # 		-> '+' At
    # 		-> '-'At =>'neg'
    # 		-> At ;

    def A(self):
        if self.tokens[0].value == "+":
            self.tokens.pop(0)  # Remove unary plus
            self.At()
        elif self.tokens[0].value == "-":
            self.tokens.pop(0)  # Remove unary minus
            self.At()
            self.ast.append(Node(NodeType.op_neg, "neg", 1))
        else:
            self.At()

        while self.tokens[0].value in {"+", "-"}:
            current_token = self.tokens[0]  # Save present token
            self.tokens.pop(0)  # Remove plus or minus operators
            self.At()
            if current_token.value == "+":
                self.ast.append(Node(NodeType.op_plus, "+", 2))
            else:
                self.ast.append(Node(NodeType.op_minus, "-", 2))

    '''
    At 	-> At '*' Af => '*'
    				-> At '/' Af => '/'
    				-> Af ;

    At -> Af ('*' Af | '/' Af)*
    '''           
    def At(self):
        self.Af()
        while self.tokens[0].value in {"*", "/"}:
            current_token = self.tokens[0]  # Save present token
            self.tokens.pop(0)  # Remove multiply or divide operators
            self.Af()
            if current_token.value == "*":
                self.ast.append(Node(NodeType.op_mul, "*", 2))
            else:
                self.ast.append(Node(NodeType.op_div, "/", 2))

    '''
    Af 	-> Ap '**' Af => '**'
    				-> Ap ;
        
    Af -> Ap ('**' Af)*
    '''

    def Af(self):
        self.Ap()
        if self.tokens[0].value == "**":
            self.tokens.pop(0)  # Remove power operator
            self.Af()
            self.ast.append(Node(NodeType.op_pow, "**", 2))

    '''
    Ap 	-> Ap '@' '<IDENTIFIER>' R => '@'
    				-> R ;
    
    Ap -> R ('@' '<IDENTIFIER>' R)*
    '''   
    def Ap(self):
        self.R()
        while self.tokens[0].value == "@":
            self.tokens.pop(0)  # Remove @ operator
            
            if self.tokens[0].type != TokenType.IDENTIFIER:
                print("Parsing error at Ap: IDENTIFIER EXPECTED")
                # Handle parsing error here
                return
            
            self.ast.append(Node(NodeType.identifier, self.tokens[0].value, 0))
            self.tokens.pop(0)  # Remove IDENTIFIER
            
            self.R()
            self.ast.append(Node(NodeType.at, "@", 3))

    # Rators And Rands
    '''
    R 	-> R Rn => 'gamma'
    		-> Rn ;
    
    R -> Rn ('gamma' Rn)*
    '''
            
    def R(self):
        self.Rn()
        while (self.tokens[0].type in [TokenType.IDENTIFIER, TokenType.INTEGER, TokenType.STRING] or
            self.tokens[0].value in ["true", "false", "nil", "dummy"] or
            self.tokens[0].value == "("):
            
            self.Rn()
            self.ast.append(Node(NodeType.gamma, "gamma", 2))

    #        Rn 	-> '<IDENTIFIER>'
    # 				-> '<INTEGER>'
    # 				-> '<STRING>'
    # 				-> 'true' => 'true'
    # 				-> 'false' => 'false'
    # 				-> 'nil' => 'nil'
    # 				-> '(' E ')'
    # 				-> 'dummy' => 'dummy' ;
            
    def Rn(self):
        token_type = self.tokens[0].type
        token_value = self.tokens[0].value

        # print(f"Processing token: {token_type}, {token_value}")
        
        if token_type == TokenType.IDENTIFIER:
            self.ast.append(Node(NodeType.identifier, token_value, 0))
            # print(token_value)
            self.tokens.pop(0)
        elif token_type == TokenType.INTEGER:
            self.ast.append(Node(NodeType.integer, token_value, 0))
            # print(token_value)
            self.tokens.pop(0)
        elif token_type == TokenType.STRING:
            self.ast.append(Node(NodeType.string, token_value, 0))
            # print(token_value)
            self.tokens.pop(0)
        elif token_type == TokenType.KEYWORD:
            if token_value == "true":
                self.ast.append(Node(NodeType.true_value, token_value, 0))
                # print(token_value)
                self.tokens.pop(0)
            elif token_value == "false":
                self.ast.append(Node(NodeType.false_value, token_value, 0))
                # print(token_value)
                self.tokens.pop(0)
            elif token_value == "nil":
                self.ast.append(Node(NodeType.nil, token_value, 0))
                # print(token_value)
                self.tokens.pop(0)
            elif token_value == "dummy":
                self.ast.append(Node(NodeType.dummy, token_value, 0))
                # print(token_value)
                self.tokens.pop(0)
            else:
                print("Parse Error at Rn: Unexpected KEYWORD")
        elif token_type == TokenType.PUNCTUATION:
            if token_value == "(":
                # # print(token_value)
                self.tokens.pop(0)  # Remove '('
                
                self.E()
                
                if self.tokens[0].value != ")":
                    print("Parsing error at Rn: Expected a matching ')'")
                    # return
                # # print(tokens[0].value)
                self.tokens.pop(0)  # Remove ')'
            else:
                print("Parsing error at Rn: Unexpected PUNCTUATION")
        else:
            print(token_type, token_value)
            print("Parsing error at Rn: Expected a Rn, but got different")

    # Definitions

    # D 	-> Da 'within' D => 'within'
    # 				-> Da ;
            
    def D(self):
        self.Da()
        if self.tokens[0].value == "within":
            # # print(tokens[0].value)
            self.tokens.pop(0)  # Remove 'within'
            self.D()
            self.ast.append(Node(NodeType.within, "within", 2))

    # Da  -> Dr ( 'and' Dr )+ => 'and'
    # 					-> Dr ;
            
    def Da(self): 
        self.Dr()
        n = 1
        while self.tokens[0].value == "and":
            # # print(tokens[0].value)
            self.tokens.pop(0)
            self.Dr()
            n += 1
        if n > 1:
            self.ast.append(Node(NodeType.and_op, "and", n))

    # Dr  -> 'rec' Db => 'rec'
    # 	-> Db ;
            
    def Dr(self):
        is_rec = False
        if self.tokens[0].value == "rec":
            # # print(tokens[0].value)
            self.tokens.pop(0)
            is_rec = True
        self.Db()
        if is_rec:
            self.ast.append(Node(NodeType.rec, "rec", 1))

    # Db  -> Vl '=' E => '='
    # 				-> '<IDENTIFIER>' Vb+ '=' E => 'fcn_form'
    # 				-> '(' D ')' ; 
            
    def Db(self): 
        if self.tokens[0].type == TokenType.PUNCTUATION and self.tokens[0].value == "(":
            # print(self.tokens[0].value)
            self.tokens.pop(0)
            self.D()
            if self.tokens[0].value != ")":
                print("Parsing error at Db #1")
                # return
            # print(tokens[0].value)
            self.tokens.pop(0)
        elif self.tokens[0].type == TokenType.IDENTIFIER:
            # print(self.tokens[0].value)
            if self.tokens[1].value == "(" or self.tokens[1].type == TokenType.IDENTIFIER:
                # Expect a fcn_form
                self.ast.append(Node(NodeType.identifier, self.tokens[0].value, 0))
                # print(self.tokens[0].value)
                self.tokens.pop(0)  # Remove ID

                n = 1  # Identifier child
                while self.tokens[0].type == TokenType.IDENTIFIER or self.tokens[0].value == "(":
                    self.Vb()
                    n += 1
                if self.tokens[0].value != "=":
                    print("Parsing error at Db #2")
                    # return
                # print(tokens[0].value)
                self.tokens.pop(0)
                self.E()

                self.ast.append(Node(NodeType.fcn_form, "fcn_form", n+1))
            elif self.tokens[1].value == "=":
                self.ast.append(Node(NodeType.identifier, self.tokens[0].value, 0))
                # print(tokens[0].value)
                self.tokens.pop(0)  # Remove identifier
                # print(tokens[0].value)
                self.tokens.pop(0)  # Remove equal
                self.E()
                self.ast.append(Node(NodeType.equal, "=", 2))
            elif self.tokens[1].value == ",":
                self.Vl()
                if self.tokens[0].value != "=":
                    print("Parsing error at Db")
                    # return
                # print(tokens[0].value)
                self.tokens.pop(0)
                self.E()

                self.ast.append(Node(NodeType.equal, "=", 2))

    # Variables
                
    # Vb  -> '<IDENTIFIER>'
    # 	  -> '(' Vl ')'
    # 	  -> '(' ')' => '()';

    def Vb(self):
        if self.tokens[0].type == TokenType.PUNCTUATION and self.tokens[0].value == "(":
            # print(self.tokens[0].value)
            self.tokens.pop(0)
            isVl = False

            if self.tokens[0].type == TokenType.IDENTIFIER:
                # print(self.tokens[0].value)
                self.Vl()
                isVl = True
            
            if self.tokens[0].value != ")":
                print("Parse error unmatch )")
                # return
            # print(self.tokens[0].value)
            self.tokens.pop(0)
            if not isVl:
                self.ast.append(Node(NodeType.empty_params, "()", 0))
        elif self.tokens[0].type == TokenType.IDENTIFIER:
            self.ast.append(Node(NodeType.identifier, self.tokens[0].value, 0))
            # print(tokens[0].value)
            self.tokens.pop(0)

    # Vl -> '<IDENTIFIER>' list ',' => ','?;
            
    def Vl(self):
        n = 0
        while True:
            # print(self.tokens[0].value)
            if n > 0:
                self.tokens.pop(0)
            if not self.tokens[0].type == TokenType.IDENTIFIER:
                print("Parse error: an identifier was expected")
            # print(self.tokens[0].value)
            self.ast.append(Node(NodeType.identifier, self.tokens[0].value, 0))
            
            self.tokens.pop(0)
            n += 1
            if not self.tokens[0].value == ",":
                break
        
        if n > 1:
            self.ast.append(Node(NodeType.comma, ",", n))

