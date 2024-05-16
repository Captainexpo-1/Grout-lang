import tokens


class ASTNode:
    # base class for all AST nodes
    def __init__(self):
        pass

class Expression(ASTNode):
    # base class for all expressions
    def __init__(self):
        pass

class Statement(ASTNode):
    # base class for all statements
    def __init__(self):
        pass
class Program(ASTNode):
    def __init__(self, statements: list[Statement]):
        self.statements = statements

    def __repr__(self):
        return f"Program({self.statements})"
class Variable(Expression):
    def __init__(self, name: str, data_type = None):
        self.name = name
        self.data_type = data_type

    def __repr__(self):
        return f"Variable({self.name},{self.data_type})"

class IfStatement(Statement):
    def __init__(self, condition: Expression, body: list[Statement], else_body: list[Statement] = None):
        self.condition = condition
        self.body = body
        self.else_body = else_body

    def __repr__(self):
        return f"IFStatement({self.condition}, {self.body}, {self.else_body})"
    
class FunctionDefinition(Statement):
    def __init__(self, name, args, return_type, body):
        self.name = name
        self.args = args
        self.body = body
        self.return_type = return_type
    def __repr__(self):
        return f"FunctionDefinition({self.name},{self.args},{self.return_type},{self.body})"

class FunctionCall(Expression):
    def __init__(self, name, return_type, args):
        self.name = name
        self.args = args
        self.return_type = return_type
    def __repr__(self):
        return f"FunctionCall({self.name},{self.return_type},{self.args})"
class ReturnStatement(Statement):
    def __init__(self, expression):
        self.expression = expression
    def __repr__(self):
        return f"ReturnStatement({self.expression})"
class ElseStatment(Statement):
    def __init__(self, body: list[Statement]):
            self.body = body

    def __repr__(self):
        return f"ElseStatement({self.body})"
class UnaryOperation(Expression):
    def __init__(self, operator: str, expression: Expression):
        self.operator = operator
        self.expression = expression

    def __repr__(self):
        return f"UnaryOperation({self.operator}, {self.expression})"
class ElifStatement(Statement):
    def __init__(self, condition: Expression, body: list[Statement], else_body: list[Statement] = None):
            self.condition = condition
            self.body = body
            self.else_body = else_body

    def __repr__(self):
        return f"ElifStatement({self.condition}, {self.body}, {self.else_body})"
class WhileStatement(Statement):
    def __init__(self, condition: Expression, body: list[Statement]):
        self.condition = condition
        self.body = body
    def __repr__(self):
        return f"WhileStatement({self.condition},{self.body})"
class IntLiteral(Expression):
    def __init__(self, value: int):
        self.value = value

    def __repr__(self):
        return f"IntLiteral({self.value})"
    
class StructLiteral(Expression):
    def __init__(self,value):
        self.value = value
    def __repr__(self):
        return f"StructLiteral({self.value})"
    
class ListLiteral(Expression):
    def __init__(self, items):
        self.items = items

    def __repr__(self):
        return f"ListLiteral({self.items})"
        
class NullLiteral(Expression):
    def __init__(self):
        self.value = "null"
    def __repr__(self):
        return f"NullLiteral({self.value})"
    
class FloatLiteral(Expression):
    def __init__(self, value: float):
        self.value = value

    def __repr__(self):
        return f"FloatLiteral({self.value})"
    

class StringLiteral(Expression):
    def __init__(self, value: str):
        
        self.value = value[1:-1]

    def __repr__(self):
        return f"StringLiteral({self.value})"

class StructCreation(Statement):
    def __init__(self, name):
        self.name = name
    def __repr__(self):
        return f"StructCreation({self.name})"
    
class BooleanLiteral(Expression):
    def __init__(self, value: bool):
        self.value = value

    def __repr__(self):
        return f"BooleanLiteral({self.value})"
    
    
class BinaryOperation(Expression):
    def __init__(self, left: Expression, operator: str, right: Expression):
        self.left = left
        self.operator = operator
        self.right = right

    def __repr__(self):
        return f"BinaryExpression({self.left}, {self.operator}, {self.right})"


class VariableDeclaration(Statement):
    def __init__(self, name: str, data_type, value: Expression):
        self.name = name
        self.value = value
        self.data_type = data_type

    def __repr__(self):
        return f"VariableDeclaration(Name: {self.name}, Value: {self.value}, DataType: {self.data_type})"
    
class Assignment:
    def __init__(self, variable: Variable, value: Expression):
        self.name = variable
        self.value = value

    def __repr__(self):
        return f"Assignment({self.name}, {self.value})"
class RangeLiteral(Expression):
    def __init__(self,start,end,step):
        self.start = start
        self.end = end
        self.step = step
    def __repr__(self) -> str:
        return f"RangeLiteral({self.start},{self.end},{self.step})"

class ForStatement(Statement):
    def __init__(self, start, condition, step, body):
        self.start = start
        self.condition = condition
        self.body = body
        self.step = step
    def __repr__(self):
        return f"ForStatement({self.start},{self.condition},{self.step},{self.body})"


class StructMethodCall(Expression):
    def __init__(self, struct, name, args):
        self.struct = struct
        self.name = name
        self.args = args
    def __repr__(self):
        return f"MethodCall({self.struct}, {self.name}, {self.args})"
class StructVariable(Variable):
    def __init__(self, struct, name):
        self.struct = struct
        self.name = name
    def __repr__(self):
        return f"StructVariable({self.struct}.{self.name})"
    
class DataType:
    def __init__(self):
        pass
    def __str__(self):
        return self.__repr__()
class VoidType(DataType):
    def __init__(self):
        pass
    def __repr__(self):
        return f"VoidType()"
class ListType(DataType):
    def __init__(self, subType):
        self.subType = subType
    def __repr__(self):
        return f"ListType({self.subType.__repr__(self.subType)})"
    
class IntType(DataType):
    def __init__(self):
        pass
    def __repr__(self):
        return f"IntType()"
    
class FloatType(DataType):
    def __init__(self):
        pass
    def __repr__(self):
        return f"FloatType()"
    
class BoolType(DataType):
    def __init__(self):
        pass
    def __repr__(self):
        return f"BoolType()"
    
class StringType(DataType):
    def __init__(self):
        pass
    def __repr__(self):
        return f"StringType()"
class StructType(DataType):
    def __init__(self):
        pass
    def __repr__(self):
        return f"StructType()"
