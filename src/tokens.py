import re

class TOKENTYPE:
    # Keywords
    IF = "IF"
    ELSE = "ELSE"
    ELIF = "ELIF"
    FUNCTION = "FUNCTION",
    RETURN = "RETURN"
    NULL = "NULL"
    STRUCT = "STRUCT"
    STRUCT_LITERAL = "STRUCT_LITERAL"
    WHILE = "WHILE"
    CREATE = "CREATE"
    VOID = "VOID"
    # Special characters
    LPAREN = "LPAREN"
    RPAREN = "RPAREN"
    LBRACE = "LBRACE"
    RBRACE = "RBRACE"
    LBRACKET = "LBRACKET"
    RBRACKET = "RBRACKET"
    COMMA = "COMMA"
    COLON = "COLON"
    SEMICOLON = "SEMICOLON"
    RANGE = "RANGE"
    DOT = "DOT"
    PLUS = "PLUS"
    MINUS = "MINUS"
    STAR = "STAR"
    SLASH = "SLASH"
    PERCENT = "PERCENT"
    CARET = "CARET"
    EQUAL = "EQUAL"
    BANG = "BANG"
    GREATER = "GREATER"
    LESS = "LESS"
    GREATER_EQUAL = "GREATER_EQUAL"
    LESS_EQUAL = "LESS_EQUAL"
    EQUAL_EQUAL = "EQUAL_EQUAL"
    NOT_EQUAL = "NOT_EQUAL"
    AND = "AND"
    OR = "OR"
    FOR = "FOR"
    ARROW = "ARROW"
    COMMENT = "COMMENT"



    # Data types
    INT = "INT"
    FLOAT = "FLOAT"
    STRING = "STRING"
    BOOL = "BOOL"
    LIST = "LIST"

    # Literals
    INT_LITERAL = "INT_LITERAL"
    FLOAT_LITERAL = "FLOAT_LITERAL"
    STRING_LITERAL = "STRING_LITERAL"
    BOOL_LITERAL = "BOOL_LITERAL"
    
    # Other
    NAME = "NAME"
    EOF = "EOF"
    NEWLINE = "NEWLINE"

    

TOKEN_RULES = {
    # Keywords
    TOKENTYPE.IF: r"if",
    TOKENTYPE.ELSE: r"else",
    TOKENTYPE.ELIF: r"elif",
    TOKENTYPE.FUNCTION: r"fn",
    TOKENTYPE.RETURN: r"return",
    TOKENTYPE.FOR: r"for",
    TOKENTYPE.NULL: r"null",
    TOKENTYPE.STRUCT_LITERAL: r"structure",
    TOKENTYPE.STRUCT: r"struct",
    TOKENTYPE.WHILE: r"while",
    TOKENTYPE.CREATE: r"create",
    TOKENTYPE.VOID: r"void",
    # Special characters
    TOKENTYPE.GREATER: r">",
    TOKENTYPE.LESS: r"<",
    TOKENTYPE.GREATER_EQUAL: r">=",
    TOKENTYPE.LESS_EQUAL: r"<=",
    TOKENTYPE.EQUAL_EQUAL: r"==",
    TOKENTYPE.NOT_EQUAL: r"!=",
    TOKENTYPE.AND: r"&&",
    TOKENTYPE.OR: r"\|\|",
    TOKENTYPE.ARROW: r"->",

    TOKENTYPE.NAME: r"[_a-zA-Z][_a-zA-Z0-9]*",
    TOKENTYPE.LPAREN: r"\(",
    TOKENTYPE.RPAREN: r"\)",
    TOKENTYPE.LBRACE: r"\{",
    TOKENTYPE.RBRACE: r"\}",
    TOKENTYPE.LBRACKET: r"\[",
    TOKENTYPE.RBRACKET: r"\]",
    TOKENTYPE.COMMA: r",",
    TOKENTYPE.COLON: r":",
    TOKENTYPE.SEMICOLON: r";",
    TOKENTYPE.RANGE: r"\.\.",
    TOKENTYPE.DOT: r"\.",
    TOKENTYPE.PLUS: r"\+",
    TOKENTYPE.MINUS: r"-",
    TOKENTYPE.STAR: r"\*",
    TOKENTYPE.SLASH: r"/",
    TOKENTYPE.PERCENT: r"%",
    TOKENTYPE.CARET: r"\^",

    TOKENTYPE.EQUAL: r"=",
    TOKENTYPE.BANG: r"!",

    # Data types
    TOKENTYPE.INT: r"int",
    TOKENTYPE.FLOAT: r"float",
    TOKENTYPE.STRING: r"string",
    TOKENTYPE.BOOL: r"bool",
    TOKENTYPE.LIST: r"list",

    # Literals
    TOKENTYPE.INT_LITERAL: r"\d+",
    TOKENTYPE.FLOAT_LITERAL: r"\d+\.\d+",
    TOKENTYPE.STRING_LITERAL: r"(\"|\').*(\"|\')",
    TOKENTYPE.BOOL_LITERAL: r"true|false",

    TOKENTYPE.EOF: r"$",
    TOKENTYPE.NEWLINE: r"\n",
    TOKENTYPE.COMMENT: r"//.*"
}
TOKEN_PRIORITY = [
    TOKENTYPE.COMMENT,
    TOKENTYPE.STRUCT_LITERAL,

    # Keywords
    TOKENTYPE.IF,
    TOKENTYPE.ELSE,
    TOKENTYPE.ELIF,
    TOKENTYPE.FUNCTION,
    TOKENTYPE.RETURN,
    TOKENTYPE.FOR,
    TOKENTYPE.NULL,
    TOKENTYPE.STRUCT,
    TOKENTYPE.WHILE,
    TOKENTYPE.CREATE,
    TOKENTYPE.VOID,
    
    # Literals
    TOKENTYPE.FLOAT_LITERAL,
    TOKENTYPE.INT_LITERAL,
    TOKENTYPE.STRING_LITERAL,
    TOKENTYPE.BOOL_LITERAL,


    # Data types
    TOKENTYPE.FLOAT,
    TOKENTYPE.INT,
    TOKENTYPE.STRING,
    TOKENTYPE.BOOL,
    TOKENTYPE.LIST,

    # Special characters
    TOKENTYPE.AND,
    TOKENTYPE.OR,
    TOKENTYPE.GREATER_EQUAL,
    TOKENTYPE.LESS_EQUAL,
    TOKENTYPE.EQUAL_EQUAL,
    TOKENTYPE.NOT_EQUAL,
    TOKENTYPE.GREATER,
    TOKENTYPE.LESS,
    TOKENTYPE.ARROW,


    TOKENTYPE.LPAREN,
    TOKENTYPE.RPAREN,
    TOKENTYPE.LBRACE,
    TOKENTYPE.RBRACE,
    TOKENTYPE.LBRACKET,
    TOKENTYPE.RBRACKET,
    TOKENTYPE.COMMA,
    TOKENTYPE.COLON,
    TOKENTYPE.SEMICOLON,
    TOKENTYPE.RANGE,
    TOKENTYPE.DOT,
    TOKENTYPE.PLUS,
    TOKENTYPE.MINUS,
    TOKENTYPE.STAR,
    TOKENTYPE.SLASH,
    TOKENTYPE.PERCENT,
    TOKENTYPE.CARET,
    TOKENTYPE.EQUAL,
    TOKENTYPE.BANG,

    # Name
    TOKENTYPE.NAME,

    # Other
    TOKENTYPE.NEWLINE,
    TOKENTYPE.EOF,
]


DATA_TYPES = (
    TOKENTYPE.INT,
    TOKENTYPE.FLOAT,
    TOKENTYPE.STRING,
    TOKENTYPE.BOOL,
    TOKENTYPE.LIST,
    TOKENTYPE.STRUCT,
    TOKENTYPE.VOID
)

ATOMS = (
    TOKENTYPE.INT_LITERAL,
    TOKENTYPE.FLOAT_LITERAL,
    TOKENTYPE.STRING_LITERAL,
    TOKENTYPE.BOOL_LITERAL,
    TOKENTYPE.NAME,
    TOKENTYPE.LPAREN,
    TOKENTYPE.NULL
)


for key, value in TOKEN_RULES.items():
    TOKEN_RULES[key] = re.compile(value)

class Token:
    def __init__(self, type, value, line=0, column=0):
        self.type = type
        self.value = value
        self.line = line
        self.column = column
    def __repr__(self):
        return f"Token({self.type}, \"{self.value}\")"
    
    def __str__(self):
        return self.__repr__()
    
