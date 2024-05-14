import tokens as token
from parserNode import *


ORDER_OF_OPERATIONS: dict = {
    # key = operator, value = order of operation (0 = first, 1 = second, etc.)
    token.TOKENTYPE.RANGE: ("LEFT",0),
    token.TOKENTYPE.CARET: ("LEFT",0),
    token.TOKENTYPE.STAR: ("LEFT",1),
    token.TOKENTYPE.SLASH: ("LEFT",1),
    token.TOKENTYPE.PERCENT: ("LEFT",1),
    token.TOKENTYPE.PLUS: ("LEFT",2),
    token.TOKENTYPE.MINUS: ("LEFT",2),
    token.TOKENTYPE.GREATER: ("LEFT",3),
    token.TOKENTYPE.LESS: ("LEFT",3),
    token.TOKENTYPE.EQUAL: ("LEFT",4),
    token.TOKENTYPE.EQUAL_EQUAL: ("LEFT",5),
    token.TOKENTYPE.NOT_EQUAL: ("LEFT",5),
    token.TOKENTYPE.GREATER_EQUAL: ("LEFT",5),
    token.TOKENTYPE.LESS_EQUAL: ("LEFT",5),
    token.TOKENTYPE.AND: ("LEFT",6),
    token.TOKENTYPE.OR: ("LEFT",7),


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
    tokens.TOKENTYPE.STRUCT : StructType
}