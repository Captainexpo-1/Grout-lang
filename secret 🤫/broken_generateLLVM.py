import uuid
from parserNode import *
from parserOptions import *
from lang_parser import Parser
from lexer import *
from sys import argv
import uuid

class LLVMIRGenerator:
    def __init__(self):
        self.output = []  # Accumulate generated code
        self.variables = {}  # Track variables and their LLVM types

    def generate(self, node):
        node_type = type(node).__name__
        handler_method = f"generate_{node_type.lower()}"
        handler = getattr(self, handler_method, self.unhandled_node)
        return handler(node)

    def generate_program(self, program):
        for statement in program.statements:
            self.output.append(self.generate(statement))
        return "\n".join(self.output)

    def generate_functiondefinition(self, function):
        args = ", ".join(f"{self.map_type(arg.data_type)} %{arg.name}" for arg in function.args)
        signature = f"define {self.map_type(function.return_type)} @{function.name}({args}) {{\n"
        body = "\n".join(self.generate(stmt) for stmt in function.body)
        return f"{signature}{body}\n}}\n"

    def generate_ifstatement(self, if_statement):
        cond_code = self.generate(if_statement.condition)
        body_code = "\n".join(self.generate(stmt) for stmt in if_statement.body)
        if if_statement.else_body:
            else_code = "\n".join(self.generate(stmt) for stmt in if_statement.else_body)
            else_label = uuid.uuid4().hex
        else:
            else_code = ""
        end_label = uuid.uuid4().hex
        return (f"br i1 {cond_code}, label %then, label %else{else_label}\n"
                f"then:\n{body_code}\n"
                f"br label %ifend{end_label}\n"
                f"else{else_label}:\n{else_code}\n"
                f"br label %ifend{end_label}\n"
                f"ifend{end_label}:\n")

    def generate_whilestatement(self, while_statement):
        cond_code = self.generate(while_statement.condition)
        body_code = "\n".join(self.generate(stmt) for stmt in while_statement.body)
        while_label = uuid.uuid4().hex
        end_label = uuid.uuid4().hex
        return (f"br label %start{while_label}\n"
                f"start{while_label}:\n"
                f"br i1 {cond_code}, label %body{while_label}, label %end{end_label}\n"
                f"body{while_label}:\n{body_code}\n"
                f"br label %start{while_label}\n"
                f"end{end_label}:\n")

    def generate_returnstatement(self, return_statement):
        value_code = self.generate(return_statement.expression)
        return f"ret {value_code}"

    def generate_variabledeclaration(self, declaration):
        type_code = self.map_type(declaration.data_type)
        value_code = self.generate(declaration.value)
        var_name = f"%{declaration.name.name}"
        self.variables[declaration.name] = type_code
        return f"{var_name} = alloca {type_code}\nstore {value_code}, {type_code}* {var_name}"

    def generate_assignment(self, assignment):
        var_name = f"%{assignment.variable.name}"
        value_code = self.generate(assignment.value)
        return f"store {self.variables[assignment.variable.name]} {value_code}, {self.variables[assignment.variable.name]}* {var_name}"
    def generate_binaryexpression(self, binary_expression):
        left_code = self.generate(binary_expression.left)
        right_code = self.generate(binary_expression.right)
        operator = binary_expression.operator.value
        return f"{operator} {self.variables[binary_expression]} {left_code}, {right_code}"
    def generate_variable(self, variable):
        return f"load {self.variables[variable.name]}* %{variable.name}"
    def generate_intliteral(self, literal):
        return f"i32 {literal.value}"

    # Additional generators as needed for each node type

    def unhandled_node(self, node):
        return f"; Unhandled node type: {type(node).__name__}"

    def map_type(self, dtype):
        # Simplified type mapping; expand as necessary
        type_mappings = {
            'IntType': 'i32',
            'FloatType': 'float',
            'BoolType': 'i1',
            'StringType': 'i8*',  # LLVM representation for strings
        }
        return type_mappings.get(dtype.__class__.__name__, 'void')

if __name__ == "__main__":

    text = open(argv[1], "r").read()
    tokens = tokenize(text)
    parser = Parser()
    program = parser.parse(tokens)
    generator = LLVMIRGenerator()
    print(generator.generate(program))
    with open("./output/llvmout.ll", "w") as f:
        f.write(generator.generate(program))