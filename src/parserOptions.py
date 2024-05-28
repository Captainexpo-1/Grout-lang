import tokens as token
from parserNode import *


UNARY_OPERATORS = [
    token.TOKENTYPE.MINUS,
    token.TOKENTYPE.BANG
]
ORDER_OF_OPERATIONS: dict = {
    token.TOKENTYPE.RANGE: ("LEFT",8), # Range operator has the highest precedence
    token.TOKENTYPE.CARET: ("LEFT",7),
    token.TOKENTYPE.CARET_EQUAL: ("LEFT",7),
    token.TOKENTYPE.STAR: ("LEFT",6),
    token.TOKENTYPE.SLASH: ("LEFT",6),
    token.TOKENTYPE.SLASH_EQUAL: ("LEFT",6),
    token.TOKENTYPE.PERCENT: ("LEFT",6),
    token.TOKENTYPE.STAR_EQUAL: ("LEFT",6),
    token.TOKENTYPE.PLUS: ("LEFT",5),
    token.TOKENTYPE.PLUS_EQUAL: ("LEFT",5),
    token.TOKENTYPE.MINUS: ("LEFT",5),
    token.TOKENTYPE.MINUS_EQUAL: ("LEFT",5),
    token.TOKENTYPE.GREATER: ("LEFT",4), # Comparisons
    token.TOKENTYPE.LESS: ("LEFT",4),
    token.TOKENTYPE.GREATER_EQUAL: ("LEFT",4),
    token.TOKENTYPE.LESS_EQUAL: ("LEFT",4),
    token.TOKENTYPE.EQUAL_EQUAL: ("LEFT",3), # Equality checks
    token.TOKENTYPE.NOT_EQUAL: ("LEFT",3),
    token.TOKENTYPE.AND: ("LEFT",2),
    token.TOKENTYPE.OR: ("LEFT",1),  # Logical OR has the lowest precedence
}
LITERAL_TO_TYPE_MAP = {
    IntLiteral: IntType,
    FloatLiteral: FloatType,
    BooleanLiteral: BoolType,
    StringLiteral: StringType,
}
DATA_TYPES_TO_LITERAL_MAP = {
    token.TOKENTYPE.INT: IntLiteral,
    token.TOKENTYPE.FLOAT: FloatLiteral,
    token.TOKENTYPE.BOOL: BooleanLiteral,
    token.TOKENTYPE.STRING: StringLiteral,
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