from parserNode import *
from lexer import Lexer, tokenize
from lang_parser import Parser
from std import LangError
class Scope:
    def __init__(self):
        self.variables = {}



class Evaluator:
    def __init__(self):
        self.ast: list[Statement|Expression] = []
        self.global_scope = Scope()
        self.current_scope = self.global_scope

    def evaluate(self, ast: list[Statement|Expression]):
        self.ast = ast
        for node in self.ast:
            if isinstance(node, Statement):
                self.evaluate_statement(node)
            elif isinstance(node, Expression):
                self.evaluate_expression(node)

    def evaluate_statement(self, statement: Statement):
        if type(statement) == FunctionDefinition:
            self.evaluate_function_definition(statement)
        elif type(statement) == ReturnStatement:
            self.evaluate_return_statement(statement)
        elif type(statement) == IFStatement:
            self.evaluate_if_statement(statement)
        elif type(statement) == ElseStatment:
            self.evaluate_else_statement(statement)
        elif type(statement) == ElifStatement:
            self.evaluate_elif_statement(statement)
        elif type(statement) == ForStatement:
            self.evaluate_for_statement(statement)
        elif type(statement) == WhileStatement:
            self.evaluate_while_statement(statement)
        else:
            raise LangError(f"Unknown statement type: {type(statement)}")

    def evaluate_expression(self, expression: Expression):
        if type(expression) == FunctionCall:
            self.evaluate_function_call(expression)
        elif type(expression) == Variable:
            return self.current_scope.variables[expression.name]
        elif type(expression) == IntLiteral:
            return int(expression.value)
        elif type(expression) == StringLiteral:
            return str(expression.value)
        elif type(expression) == BinaryOperation:
            self.evaluate_binary_operation(expression)
        elif type(expression) == UnaryOperation:
        
        else:
            raise LangError(f"Unknown expression type: {type(expression)}")
