from sys import argv
from parserNode import *
from lexer import Lexer,tokenize
from lang_parser import Parser
class Environment:
    def __init__(self, parent=None, type='function', global_env=None):
        self.variables = {}
        self.functions = {}
        self.parent = parent
        self.type = type
        self.global_env = global_env

    def get(self, name):
        if type(name) == Variable: name = name.name
        if name in self.variables:
            return self.variables[name]
        elif self.parent:
            return self.parent.get(name)
        else:
            raise NameError(f"Undefined variable: {name}")

    def set(self, name, value):
        if type(name) == Variable: name = name.name
        self.variables[name] = value

    def get_function(self, name):
        if name in self.functions:
            return self.functions[name]
        elif name in self.global_env.functions:
            return self.global_env.functions[name]
        elif self.parent:
            return self.parent.get_function(name)
        else:
            raise NameError(f"Undefined function: {name}")

    def set_function(self, name, value):
        self.functions[name] = value

class ReturnValue(Exception):
    def __init__(self, value):
        self.value = value

class Evaluator:
    def __init__(self):
        self.global_env = Environment()
        self.builtins = {
            "print": lambda *args: print(*args),
            "input": lambda prompt: input(prompt),
        }
        self.call_stack = []

    def evaluate(self, node, env=None):
        if env is None:
            env = self.global_env
        if isinstance(node, Program):
            return self.visit_program(node, env)
        elif isinstance(node, IntLiteral):
            return self.visit_int_literal(node)
        elif isinstance(node, FloatLiteral):
            return self.visit_float_literal(node)
        elif isinstance(node, StringLiteral):
            return self.visit_string_literal(node)
        elif isinstance(node, BooleanLiteral):
            return self.visit_boolean_literal(node)
        elif isinstance(node, Variable):
            return self.visit_variable(node, env)
        elif isinstance(node, BinaryOperation):
            return self.visit_binary_operation(node, env)
        elif isinstance(node, UnaryOperation):
            return self.visit_unary_operation(node, env)
        elif isinstance(node, VariableDeclaration):
            return self.visit_variable_declaration(node, env)
        elif isinstance(node, Assignment):
            return self.visit_assignment(node, env)
        elif isinstance(node, IfStatement):
            return self.visit_if_statement(node, env)
        elif isinstance(node, WhileStatement):
            return self.visit_while_statement(node, env)
        elif isinstance(node, ForStatement):
            return self.visit_for_statement(node, env)
        elif isinstance(node, FunctionCall):
            return self.visit_function_call(node, env)
        elif isinstance(node, ReturnStatement):
            return self.visit_return_statement(node, env)
        elif isinstance(node, FunctionDefinition):
            return self.visit_function_definition(node, env)
        elif isinstance(node, NullLiteral):
            return None
        elif isinstance(node, list):
            for stmt in node:
                self.evaluate(stmt, env)
        else:
            raise ValueError(f"Unknown node type: {node}")

    def visit_program(self, node, env):
        result = None
        for stmt in node.statements:
            result = self.evaluate(stmt, env)
        return result

    def visit_int_literal(self, node):
        return node.value

    def visit_float_literal(self, node):
        return node.value

    def visit_string_literal(self, node):
        return node.value

    def visit_boolean_literal(self, node):
        return node.value

    def visit_variable(self, node, env):
        return env.get(node.name)

    def visit_binary_operation(self, node, env):
        left = self.evaluate(node.left, env)
        right = self.evaluate(node.right, env)
        operator = node.operator
        if operator == '+':
            return left + right
        elif operator == '-':
            return left - right
        elif operator == '*':
            return left * right
        elif operator == '^':
            return left ** right
        elif operator == '/':
            return left / right
        elif operator == '%':
            return left % right
        elif operator == '==':
            return left == right
        elif operator == '!=':
            return left != right
        elif operator == '<':
            return left < right
        elif operator == '>':
            return left > right
        elif operator == '<=':
            return left <= right
        elif operator == '>=':
            return left >= right
        elif operator == '&&':
            return left and right
        elif operator == '||':
            return left or right
        else:
            raise ValueError(f"Unknown operator: {operator}")

    def visit_unary_operation(self, node, env):
        operand = self.evaluate(node.expression, env)
        operator = node.operator
        if operator == '-':
            return -operand
        elif operator == '!':
            return not operand
        else:
            raise ValueError(f"Unknown operator: {operator}")

    def visit_variable_declaration(self, node, env):
        value = self.evaluate(node.value, env)
        env.set(node.name, value)

    def visit_assignment(self, node, env):
        value = self.evaluate(node.value, env)
        env.set(node.name.name, value)

    def visit_if_statement(self, node, env):
        condition = self.evaluate(node.condition, env)
        if condition:
            for stmt in node.body:
                self.evaluate(stmt, env)
        elif node.else_body:
            eb = node.else_body
            if isinstance(eb, ElifStatement):
                self.visit_if_statement(eb, env)
            elif isinstance(eb, ElseStatment):
                for stmt in eb.body:
                    self.evaluate(stmt, env)

    def visit_while_statement(self, node, env):
        while self.evaluate(node.condition, env):
            for stmt in node.body:
                self.evaluate(stmt, env)

    def visit_for_statement(self, node, env):
        """
        For loop: start: Statement|Expression, end: Statement|Expression, step: Statement|Expression, body: Statement[] 
        """
        self.evaluate(node.start, env)
        while self.evaluate(node.condition, env) == True:
            for stmt in node.body:
                self.evaluate(stmt, env)
            self.evaluate(node.step, env)

    def visit_function_call(self, node, env):
        args = [self.evaluate(arg, env) for arg in node.args]
        if node.name in self.builtins:
            return self.builtins[node.name](*args)
        func = env.get_function(node.name)
        func_env = Environment(env, global_env=self.global_env, type='function')
        for param, arg in zip(func.args, args):
            func_env.set(param.name, arg)
        
        # Push the function environment onto the call stack
        self.call_stack.append(func_env)
        
        try:
            for stmt in func.body:
                self.evaluate(stmt, func_env)
        except ReturnValue as rv:
            self.call_stack.pop()
            return rv.value
        
        # Pop the function environment off the call stack when done
        self.call_stack.pop()
        return NullLiteral()

    def visit_return_statement(self, node, env):
        value = self.evaluate(node.expression, env)
        raise ReturnValue(value)

    def visit_function_definition(self, node, env):
        env.set_function(node.name, node)

# Example usage
if __name__ == "__main__":
    text = open(argv[1],'r').read()
    t = Lexer(text).tokenize()
    parser = Parser()
    ast = parser.parse(t)
    print(ast)
    evaluator = Evaluator()
    evaluator.evaluate(ast)
