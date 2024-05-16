import re
from enum import Enum

class TokenType(Enum):
    KEYWORD = 1
    IDENTIFIER = 2
    INTEGER = 3
    STRING = 4
    END_OF_TOKENS = 5
    PUNCTUATION = 6
    OPERATOR = 7

class MyToken:
    def __init__(self, token_type, value):
        if not isinstance(token_type, TokenType):
            raise ValueError("token_type must be an instance of TokenType enum")
        self.type = token_type
        self.value = value

    # Getters for type and value
    def get_type(self):
        return self.type

    def get_value(self):
        return self.value



def tokenize(input_str):
    tokens = []
    keywords = {
        'COMMENT': r'//.*',
        'KEYWORD': r'(let|in|fn|where|aug|or|not|gr|ge|ls|le|eq|ne|true|false|nil|dummy|within|and|rec)\b',
        'STRING': r'\'(?:\\\'|[^\'])*\'',
        'IDENTIFIER': r'[a-zA-Z][a-zA-Z0-9_]*',
        'INTEGER': r'\d+',
        'OPERATOR': r'[+\-*<>&.@/:=~|$\#!%^_\[\]{}"\'?]+',
        'SPACES': r'[ \t\n]+',
        'PUNCTUATION': r'[();,]'
    }
    
    while input_str:
        matched = False
        for key, pattern in keywords.items():
            match = re.match(pattern, input_str)
            if match:
                print(key, match.group(0))
                if key != 'SPACES':
                    if key == 'COMMENT':
                        comment = match.group(0)
                        input_str = input_str[match.end():]
                        matched = True
                        break
                    else:
                        token_type = getattr(TokenType, key)  # Get TokenType enum value
                        if not isinstance(token_type, TokenType):
                            raise ValueError(f"Token type '{key}' is not a valid TokenType")
                        tokens.append(MyToken(token_type, match.group(0)))
                        input_str = input_str[match.end():]
                        matched = True
                        break
                input_str = input_str[match.end():]
                matched = True
                break
        if not matched:
            print("Error: Unable to tokenize input")
    return tokens

# #Example usage

# #read input from input.txt
# input_file = open("input.txt", "r")
# input_str = input_file.read()
# input_file.close()

# tokens = tokenize(input_str)

# for token in tokens:
#     print(token.type, token.value)  # Print each token
