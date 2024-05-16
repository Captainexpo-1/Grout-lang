import tokens as token
from parserNode import *


UNARY_OPERATORS = [
    token.TOKENTYPE.MINUS,
    token.TOKENTYPE.BANG
]
ORDER_OF_OPERATIONS: dict = {
    token.TOKENTYPE.RANGE: ("LEFT",8),   # Range operator should have the highest precedence
    token.TOKENTYPE.CARET: ("LEFT",7),  # Assuming ^ is for exponentiation and is right-associative
    token.TOKENTYPE.STAR: ("LEFT",6),    # *, /, % should have the same precedence
    token.TOKENTYPE.SLASH: ("LEFT",6),
    token.TOKENTYPE.PERCENT: ("LEFT",6),
    token.TOKENTYPE.PLUS: ("LEFT",5),    # + and - should have the same precedence
    token.TOKENTYPE.MINUS: ("LEFT",5),
    token.TOKENTYPE.GREATER: ("LEFT",4), # Comparisons
    token.TOKENTYPE.LESS: ("LEFT",4),
    token.TOKENTYPE.GREATER_EQUAL: ("LEFT",4),
    token.TOKENTYPE.LESS_EQUAL: ("LEFT",4),
    token.TOKENTYPE.EQUAL_EQUAL: ("LEFT",3), # Equality checks
    token.TOKENTYPE.NOT_EQUAL: ("LEFT",3),
    token.TOKENTYPE.AND: ("LEFT",2),    # Logical AND
    token.TOKENTYPE.OR: ("LEFT",1),     # Logical OR
}
LITERAL_TO_TYPE_MAP = {
    IntLiteral: IntType,
    FloatLiteral: FloatType,
    BooleanLiteral: BoolType,
    StringLiteral: StringType,
    StructLiteral: StructType
}
DATA_TYPES_TO_LITERAL_MAP = {
    token.TOKENTYPE.INT: IntLiteral,
    token.TOKENTYPE.FLOAT: FloatLiteral,
    token.TOKENTYPE.BOOL: BooleanLiteral,
    token.TOKENTYPE.STRING: StringLiteral,
    token.TOKENTYPE.STRUCT: StructLiteral
}

TOKEN_TO_DATA_TYPE_MAP = {
    tokens.TOKENTYPE.LIST : ListType,
    tokens.TOKENTYPE.INT : IntType,
    tokens.TOKENTYPE.FLOAT : FloatType,
    tokens.TOKENTYPE.BOOL : BoolType,
    tokens.TOKENTYPE.STRING : StringType,
    tokens.TOKENTYPE.STRUCT : StructType,
    tokens.TOKENTYPE.VOID : VoidType
}