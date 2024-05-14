import tokens

class LLVMInstruction:
    def __init__(self, instruction):
        self.instruction = instruction
    def __repr__(self):
        return f"LLVMInstruction({self.instruction})"
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

class Variable(Expression):
    def __init__(self, name: str):
        self.name = name

    def __repr__(self):
        return f"Variable({self.name})"

class IFStatement(Statement):
    def __init__(self, condition: Expression, body: list[Statement], else_body: list[Statement] = None):
        self.condition = condition
        self.body = body
        self.else_body = else_body

    def __repr__(self):
        return f"IFStatement({self.condition}, {self.body}, {self.else_body})"
    
class FunctionDefinition(Statement):
    def __init__(self, name, args, body):
        self.name = name
        self.args = args
        self.body = body
    def __repr__(self):
        return f"FunctionDefinition({self.name},{self.args},{self.body})"
class FunctionCall(Expression):
    def __init__(self, name, args):
        self.name = name
        self.args = args
    def __repr__(self):
        return f"FunctionCall({self.name},{self.args})"
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
        

class FloatLiteral(Expression):
    def __init__(self, value: float):
        self.value = value

    def __repr__(self):
        return f"FloatLiteral({self.value})"
    

class StringLiteral(Expression):
    def __init__(self, value: str):
        self.value = value

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
    def __init__(self,start,end):
        self.start = start
        self.end = end
    def __repr__(self) -> str:
        return f"RangeLiteral({self.start},{self.end})"

class ForStatement(Statement):
    def __init__(self, variable, range, body):
        self.variable = variable
        self.range = range
        self.body = body
    def __repr__(self):
        return f"ForStatement({self.variable},{self.range},{self.body})"


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
