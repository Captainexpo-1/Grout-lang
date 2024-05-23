from sys import argv
from parserNode import *
from lexer import Lexer,tokenize
from lang_parser import Parser
import std
from parserOptions import *

class Struct:
    def __init__(self, env, name):
        self.env = env
        self.name = name
    def get(self, name):
        return self.env.get(name)
    def set(self, name, value):
        self.env.set(name, value)
    def __repr__(self):
        return f"Struct({self.name},{self.env.variables})"
class TypeStruct:
    def __init__(self, fields):
        self.fields = fields # <name>: <data type>
    def __repr__(self):
        return f"TypeStruct({self.fields})"
    
PYTHON_DATA_TYPE_TO_DATA_TYPE_MAP.update (
    {
        Struct: StructType
    }
)
class Environment:
    def __init__(self, parent=None, type='function', global_env=None, verbose_override=None):
        self.variables = {}
        self.var_data_types = {}
        self.functions = {}
        self.structs = {}
        self.parent = parent
        self.type = type
        self.global_env = global_env
        self.verbose_override = verbose_override
        
    def throwError(self, message, verbose=False, t="Runtime"):
        verbose = self.verbose_override if self.verbose_override is not None else verbose
        if not verbose: std.error(message,t)
        raise std.LangError(message)
    
    def get(self, name):
        if type(name) == Variable: name = name.name
        if name in self.variables:
            return self.variables[name]
        elif self.parent:
            return self.parent.get(name)
        else:
            self.throwError(f"Undefined variable: {name}")
    def get_struct(self, name):
        if name in self.structs:
            return self.structs[name]
        elif self.parent:
            return self.parent.get_struct(name)
        else:
            self.throwError(f"Undefined struct: {name}")
    def set_struct(self, name, value):
        self.structs[name] = value
    def set(self, name, value, dtype=None):
        if type(name) == Variable: 
            self.var_data_types[name.name] = name.data_type
            name = name.name
        if value == None:
            self.variables[name] = None
            return  
        if dtype:
            if type(dtype) == ListType:
                subType = self.var_data_types[name].subType
                for i in value:
                    if PYTHON_DATA_TYPE_TO_DATA_TYPE_MAP[type(i)] != subType:
                        self.throwError(f"Cannot set variable {name} of type {self.var_data_types[name]} to {value}")
            elif type(dtype) == StructType:
                expectedStruct = dtype.subType
                realStruct = value.name
                if realStruct != expectedStruct:
                    self.throwError(f"Cannot set variable {name} of type {dtype} to {value}")
            elif type(self.var_data_types[name]) != PYTHON_DATA_TYPE_TO_DATA_TYPE_MAP[type(value)]:
                self.throwError(f"Cannot set variable {name} of type {self.var_data_types[name]} to {value}")
        elif dtype:
            if type(dtype) != PYTHON_DATA_TYPE_TO_DATA_TYPE_MAP[type(value)]:
                self.throwError(f"Cannot set variable {name} of type {dtype} to {value}")
        
        self.variables[name] = value

    def get_function(self, name):
        if name in self.functions:
            return self.functions[name]
        elif name in self.global_env.functions:
            return self.global_env.functions[name]
        elif self.parent:
            return self.parent.get_function(name)
        else:
            self.throwError(f"Undefined function: {name}")

    def set_function(self, name, value):
        self.functions[name] = value
    def __repr__(self):
        return f"Environment(\n\tVars: {self.variables}\n\tTypes: {self.var_data_types}\n\tFuncs: {self.functions}\n\tStructs: {self.structs}\n\tParent: {self.parent}\n\tType: {self.type}\n\tGlobal: {self.global_env}\n)"
class ReturnValue(Exception):
    def __init__(self, value):
        self.value = value

class Evaluator:
    def __init__(self, verbose_override=None):
        self.global_env = Environment(type='global')
        self.builtins = {
            "print": lambda *args: print(*args),
            "input": lambda prompt: input(prompt),
            "parseNumber": lambda num: int(num) if num.isnumeric() else float(num) if num.replace('.','',1).isnumeric() else None,
            "str": lambda s: str(s),
        }
        self.call_stack = []
        self.verbose_override = verbose_override
        
    def throwError(self, message, verbose=False, t="Runtime"):
        verbose = self.verbose_override if self.verbose_override is not None else verbose
        if not verbose: std.error(message,t)
        raise std.LangError(message)
    def isAllowed(self, node, env):
        t = type(node)
        disallowed_struct = [VariableAccess, FunctionDefinition]
        dissalowed_function = []
        dissalowed_global = []
        if t in disallowed_struct and env.type == 'struct':
            self.throwError(f"Structs cannot contain {t.__name__}")
        elif t in dissalowed_function and env.type == 'function':
            self.throwError(f"Functions cannot contain {t.__name__}")
        elif t in dissalowed_global and env.type == 'global':
            self.throwError(f"Global cannot contain {t.__name__}")

    def evaluate(self, node, env=None):
        if env is None:
            env = self.global_env
        self.isAllowed(node, env)
        if isinstance(node, Program):
            return self.visit_program(node, env)
        elif isinstance(node, str):
            return node
        elif isinstance(node, ListLiteral):
            return self.visit_list_literal(node)
        elif isinstance(node, IntLiteral):
            return self.visit_int_literal(node)
        elif isinstance(node, FloatLiteral):
            return self.visit_float_literal(node)
        elif isinstance(node, StringLiteral):
            return self.visit_string_literal(node)
        elif isinstance(node, BooleanLiteral):
            return self.visit_boolean_literal(node)
        elif isinstance(node, StructCreation):
            return self.visit_struct_creation(node, env)
        elif isinstance(node, StructDefinition):
            return self.visit_struct_definition(node)
        elif isinstance(node, BinaryOperation):
            return self.visit_binary_operation(node, env)
        elif isinstance(node, UnaryOperation):
            return self.visit_unary_operation(node, env)
        elif isinstance(node, VariableDeclaration):
            return self.visit_variable_declaration(node, env)
        elif isinstance(node, AccessAssignment):
            return self.visit_access_assignment(node, env)
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
        elif isinstance(node, VariableAccess):
            return self.visit_struct_variable(node, env)
        elif isinstance(node, Variable):
            return self.visit_variable(node, env)
        elif isinstance(node, NullLiteral):
            return None
        elif isinstance(node, list):
            for stmt in node:
                self.evaluate(stmt, env)
        else:
            self.throwError(f"Unknown node type: {node}")

    def visit_program(self, node, env):
        result = None
        for stmt in node.body:
            result = self.evaluate(stmt, env)
        return result
    def visit_list_literal(self, node):
        return [self.evaluate(item) for item in node.items]
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
    def visit_struct_creation(self, node: StructCreation, env):
        struct = env.get_struct(node.name)
        if not struct:
            self.throwError(f"Struct {node.name} not found")
        # Create a new environment for the struct and set it to the fields
        s_env = Environment(env, type='struct')
        for i in struct.fields:
            s_env.set(i, None)
            s_env.var_data_types[i] = struct.fields[i]
        
        # Evaluate the struct creation body
        for stmt in node.body:
            self.evaluate(stmt, s_env)
        return Struct(s_env, node.name)
    def visit_struct_definition_block(self, node):
        # get all the fields in the struct and their data types
        structFields = {}
        for s in node.body:
            structFields[s.name] = s.data_type
        return TypeStruct(structFields)
        
    def visit_struct_definition(self, node):
        struct = self.visit_struct_definition_block(node)
        self.global_env.set_struct(node.name, struct)
        return struct
    def visit_struct_variable(self, node, env, ret_env=False):
        """
        class VariableAccess(Expression):
            def __init__(self, struct, name):
                self.struct = struct
                self.name = name
            def __repr__(self):
                return f"VariableAccess({self.struct}, {self.name})"
        """
        #VariableAccess(
        #   VariableAccess(
        #        a, 
        #        b
        #   ), 
        #   c
        #)
        # a.b.c
        struct = self.evaluate(node.struct, env)
        if isinstance(struct, Struct):
            if ret_env:
                return struct
            return struct.get(node.name)
        elif isinstance(struct, str):
            # Got the name of a struct
            struct = env.get(struct)
            if ret_env:
                return struct
            return struct.get(node.name)
        else:
            self.throwError(f"Variable {node.name} not found in struct {struct}")
    def visit_access_assignment(self, node, env):
        """
        class AccessAssignment(Assignment):
            def __init__(self, name, value):
                self.name = name
                self.value = value
        """
        struct = self.visit_struct_variable(node.name, env, ret_env=True)
        value = self.evaluate(node.value, env)
        struct.set(node.name.name, value)
        return value


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
        elif operator == '+=':
            env.set(node.left.name, left + right)
            return left + right
        elif operator == '-=':
            env.set(node.left.name, left - right)
            return left - right
        elif operator == '/=':
            env.set(node.left.name, left / right)
            return left / right
        elif operator == '*=':
            env.set(node.left.name, left * right)
            return left * right
        elif operator == '^=':
            env.set(node.left.name, left ** right)
            return left ** right
        elif operator == '%=':
            env.set(node.left.name, left % right)
            return left % right
        else:
            self.throwError(f"Unknown operator: {operator}")

    def visit_unary_operation(self, node, env):
        operand = self.evaluate(node.expression, env)
        operator = node.operator
        if operator == '-':
            return -operand
        elif operator == '!':
            return not operand
        else:
            self.throwError(f"Unknown operator: {operator}")

    def visit_variable_declaration(self, node, env):
        value = self.evaluate(node.value, env)
        env.set(node.name, value, dtype=node.data_type)

    def visit_assignment(self, node, env):
        value = self.evaluate(node.value, env)
        env.set(node.name, value)

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
