import llvmlite.ir as ir
import llvmlite.binding as llvm
from typing import List

# Initialize the LLVM
llvm.initialize()
llvm.initialize_native_target()
llvm.initialize_native_asmprinter()

class ASTNode:
    def __init__(self):
        pass

    
class Expression(ASTNode):
    def __init__(self):
        pass

class Statement(ASTNode):
    def __init__(self):
        pass

class Program(ASTNode):
    def __init__(self, body: List[Statement]):
        self.body = body

    def __repr__(self):
        return f"Program({self.body})"

    
class Variable(Expression):
    def __init__(self, name: str, data_type = None):
        self.name = name
        assert data_type is not None, "Data type must be provided"
        self.data_type = data_type

    def __repr__(self):
        return f"Variable({self.name},{self.data_type})"

    
class IfStatement(Statement):
    def __init__(self, condition: Expression, body: List[Statement], else_body: List[Statement] = None):
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

    
class VariableDeclaration(Statement):
    def __init__(self, name: str, data_type, value: Expression):
        self.name = name
        self.value = value
        self.data_type = data_type

    def __repr__(self):
        return f"VariableDeclaration(Name: {self.name}, Value: {self.value}, DataType: {self.data_type})"

    
class BinaryOperation(Expression):
    def __init__(self, left: Expression, operator: str, right: Expression):
        self.left = left
        self.operator = operator
        self.right = right

    def __repr__(self):
        return f"BinaryExpression({self.left}, {self.operator}, {self.right})"

    
class IntLiteral(Expression):
    def __init__(self, value: int):
        self.value = value

    def __repr__(self):
        return f"IntLiteral({self.value})"

    
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

    
class BooleanLiteral(Expression):
    def __init__(self, value: bool):
        self.value = value

    def __repr__(self):
        return f"BooleanLiteral({self.value})"

    
class UnaryOperation(Expression):
    def __init__(self, operator: str, expression: Expression):
        self.operator = operator
        self.expression = expression

    def __repr__(self):
        return f"UnaryOperation({self.operator}, {self.expression})"

    
class ListLiteral(Expression):
    def __init__(self, items):
        self.items = items

    def __repr__(self):
        return f"ListLiteral({self.items})"

    
class ListAccess(Expression):
    def __init__(self, name, index):
        self.name = name
        self.index = index

    def __repr__(self):
        return f"ListAccess({self.name},{self.index})"

    
class NullLiteral(Expression):
    def __init__(self):
        self.value = "null"

    def __repr__(self):
        return f"NullLiteral({self.value})"

    
class VariableAccess(Expression):
    def __init__(self, struct, name):
        self.struct = struct
        self.name = name

    def __repr__(self):
        return f"VariableAccess({self.struct}, {self.name})"

    
class RangeLiteral(Expression):
    def __init__(self, start, end, step):
        self.start = start
        self.end = end
        self.step = step

    def __repr__(self):
        return f"RangeLiteral({self.start},{self.end},{self.step})"

    
class StructDefinition(Statement):
    def __init__(self, name, body):
        self.name = name
        self.body = body

    def __repr__(self):
        return f"StructDefinition({self.name},{self.body})"

    
class StructCreation(Statement):
    def __init__(self, name, body):
        self.name = name
        self.body = body

    def __repr__(self):
        return f"StructCreation({self.name}, {self.body})"

    
class Assignment(Statement):
    def __init__(self, variable: Variable, value: Expression):
        self.name = variable
        self.value = value

    def __repr__(self):
        return f"Assignment({self.name}, {self.value})"

    
class AccessAssignment(Assignment):
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __repr__(self):
        return f"AccessAssignment({self.name},{self.value})"

    
class ForStatement(Statement):
    def __init__(self, start, condition, step, body):
        self.start = start
        self.condition = condition
        self.body = body
        self.step = step

    def __repr__(self):
        return f"ForStatement({self.start},{self.condition},{self.step},{self.body})"

    
        builder.branch(loop_cond)
        builder.position_at_start(loop_cond)
        cond_result = builder.icmp_signed("==", cond_val, ir.Constant(cond_val.type, 1))
        builder.cbranch(cond_result, loop_body, loop_end)

        builder.position_at_start(loop_body)
        for stmt in self.body:
            stmt.to_llvm(module, builder)
        builder.branch(loop_cond)

        builder.position_at_start(loop_end)

class WhileStatement(Statement):
    def __init__(self, condition: Expression, body: List[Statement]):
        self.condition = condition
        self.body = body

    def __repr__(self):
        return f"WhileStatement({self.condition},{self.body})"

    
        builder.branch(loop_cond)
        builder.position_at_start(loop_cond)
        cond_result = builder.icmp_signed("==", cond_val, ir.Constant(cond_val.type, 1))
        builder.cbranch(cond_result, loop_body, loop_end)

        builder.position_at_start(loop_body)
        for stmt in self.body:
            stmt.to_llvm(module, builder)
        builder.branch(loop_cond)

        builder.position_at_start(loop_end)

class ElifStatement(Statement):
    def __init__(self, condition: Expression, body: List[Statement], else_body: List[Statement] = None):
        self.condition = condition
        self.body = body
        self.else_body = else_body

    def __repr__(self):
        return f"ElifStatement({self.condition}, {self.body}, {self.else_body})"

    
class ElseStatement(Statement):
    def __init__(self, body: List[Statement]):
        self.body = body

    def __repr__(self):
        return f"ElseStatement({self.body})"

    
class ListElementAssignment(Statement):
    def __init__(self, name, index, value):
        self.name = name
        self.index = index
        self.value = value

    def __repr__(self):
        return f"ListElementAssignment({self.name},{self.index},{self.value})"

    
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
    def __init__(self, subType):
        self.subType = subType

    def __repr__(self):
        return f"StructType({self.subType})"

    
class ListType(DataType):
    def __init__(self):
        pass

    def __repr__(self):
        return f"ListType()"

        