import tokens
from parserNode import *


UNARY_OPERATORS = [
    tokens.TOKENTYPE.MINUS,
    tokens.TOKENTYPE.BANG
]
ORDER_OF_OPERATIONS: dict = {
    tokens.TOKENTYPE.RANGE: ("LEFT",8), # Range operator has the highest precedence
    tokens.TOKENTYPE.CARET: ("LEFT",7),
    tokens.TOKENTYPE.CARET_EQUAL: ("LEFT",7),
    tokens.TOKENTYPE.STAR: ("LEFT",6),
    tokens.TOKENTYPE.SLASH: ("LEFT",6),
    tokens.TOKENTYPE.SLASH_EQUAL: ("LEFT",6),
    tokens.TOKENTYPE.PERCENT: ("LEFT",6),
    tokens.TOKENTYPE.STAR_EQUAL: ("LEFT",6),
    tokens.TOKENTYPE.PLUS: ("LEFT",5),
    tokens.TOKENTYPE.PLUS_EQUAL: ("LEFT",5),
    tokens.TOKENTYPE.MINUS: ("LEFT",5),
    tokens.TOKENTYPE.MINUS_EQUAL: ("LEFT",5),
    tokens.TOKENTYPE.GREATER: ("LEFT",4), # Comparisons
    tokens.TOKENTYPE.LESS: ("LEFT",4),
    tokens.TOKENTYPE.GREATER_EQUAL: ("LEFT",4),
    tokens.TOKENTYPE.LESS_EQUAL: ("LEFT",4),
    tokens.TOKENTYPE.EQUAL_EQUAL: ("LEFT",3), # Equality checks
    tokens.TOKENTYPE.NOT_EQUAL: ("LEFT",3),
    tokens.TOKENTYPE.AND: ("LEFT",2),
    tokens.TOKENTYPE.OR: ("LEFT",1),  # Logical OR has the lowest precedence
}
LITERAL_TO_TYPE_MAP = {
    IntLiteral: IntType,
    FloatLiteral: FloatType,
    BooleanLiteral: BoolType,
    StringLiteral: StringType,
}
DATA_TYPES_TO_LITERAL_MAP = {
    tokens.TOKENTYPE.INT: IntLiteral,
    tokens.TOKENTYPE.FLOAT: FloatLiteral,
    tokens.TOKENTYPE.BOOL: BooleanLiteral,
    tokens.TOKENTYPE.STRING: StringLiteral,
}

TOKEN_TO_DATA_TYPE_MAP = {
    tokens.TOKENTYPE.LIST : ListType,
    tokens.TOKENTYPE.INT : IntType,
    tokens.TOKENTYPE.FLOAT : FloatType,
    tokens.TOKENTYPE.BOOL : BoolType,
    tokens.TOKENTYPE.STRING : StringType,
    tokens.TOKENTYPE.STRUCT : StructType,
    tokens.TOKENTYPE.VOID : VoidType,
}

PYTHON_DATA_TYPE_TO_DATA_TYPE_MAP = {
    int : IntType,
    float : FloatType,
    bool : BoolType,
    str : StringType,
    list : ListType,
    dict : StructType,
    type(None) : VoidType
}