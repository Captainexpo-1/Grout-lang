import tokens as token
from tokens import TOKENTYPE
from lexer import Lexer
import std
from parserNode import *
from parserOptions import ORDER_OF_OPERATIONS, TOKEN_TO_DATA_TYPE_MAP, UNARY_OPERATORS
from sys import argv
class Parser:
    def __init__(self):
        self.tokens = []
        self.ast = []
        self.current = 0
        self.function_returns = {
            "print": "void",
            "input": "string"
        }
        self.variable_types = {

        }

    def throwError(self, message):
        std.error(message)

    def peek(self, a=1) -> token.Token:
        if self.current + a >= len(self.tokens):
            return token.Token(TOKENTYPE.EOF, "")
        return self.tokens[self.current + a]
    def advance(self):
        if self.current < len(self.tokens):
            self.current += 1

    def curToken(self):
        if self.current < len(self.tokens):
            return self.tokens[self.current]
        return token.Token(TOKENTYPE.EOF, "")

    def eat(self, tokentype):
        if self.curToken().type != tokentype:
            self.throwError(f"Expected {tokentype} but got {self.curToken().type}")
        
        a=self.curToken()
        self.advance()
        return a
    def eatAny(self, tokentypes):
        if self.curToken().type not in tokentypes:
            self.throwError(f"Expected {tokentypes} but got {self.curToken().type}")
        a = self.curToken()
        self.advance()
        return a

    def addNode(self, node):
        self.ast.append(node)

    def parse(self, tokens: list[token.Token]):
        self.tokens = tokens
        self.current = 0  # Ensure current index is reset
        while self.curToken().type != TOKENTYPE.EOF:
            parsed = self.parseNode()
            if parsed == None:
                break
            self.addNode(parsed)
        return Program(self.ast)


    def parseNode(self):

        if self.curToken().type in token.DATA_TYPES:
            return self.parseVariableDeclaration()
        elif self.curToken().type == TOKENTYPE.NAME:
            return self.handleName()
        elif self.curToken().type == TOKENTYPE.STRUCT_DEFINITION:
            return self.parseStructDefinition()
        elif self.curToken().type == TOKENTYPE.FOR:
            return self.parseForStatement()
        elif self.curToken().type == TOKENTYPE.FUNCTION:
            return self.parseFunctionDefinition()
        elif self.curToken().type == TOKENTYPE.RETURN:
            return self.parseReturnStatement()
        elif self.curToken().type == TOKENTYPE.IF:
            return self.parseIfStatement()
        elif self.curToken().type == TOKENTYPE.WHILE:
            return self.parseWhileStatement()
        elif self.curToken().type == TOKENTYPE.NEWLINE:
            self.eat(TOKENTYPE.NEWLINE)
            return self.parseNode()
        elif self.curToken().type in token.ATOMS:
            try:
                return self.parseExpression()
            except:
                return self.parseNode()

        elif self.curToken().type == TOKENTYPE.EOF:
            return None
        self.throwError(f"Unexpected token {self.curToken().type} on line: {self.curToken().line} col: {self.curToken().column}")
    def handleName(self):
        if self.peek().type == TOKENTYPE.EQUAL :
            return self.parseVariableAssignment()
        elif self.peek().type in ORDER_OF_OPERATIONS.keys():
            return self.parseExpression()
        
        # Again, this is a hack to impliment the grammar. What the fuck.
        elif self.peek().type == TOKENTYPE.COLON and self.curToken().value in self.function_returns:
            return self.parseFunctionCall()
        elif self.peek().type == TOKENTYPE.DOT:
            return self.handle_struct_variable_access(self.eat(TOKENTYPE.NAME).value)
        else:
            self.throwError(f"Unexpected token {self.curToken().type} on line: {self.curToken().line} col: {self.curToken().column}")
    def parseBlock(self):

        # Eat leading brace
        self.skipWhitespace()
        self.eat(TOKENTYPE.LBRACE)

        # Init block list
        block = []
        self.skipWhitespace()
        # While the block is not finished
        while self.curToken().type != TOKENTYPE.RBRACE: 
            # Parse the line
            block.append(self.parseNode())
            self.skipWhitespace()

        # Return the block
        self.eat(TOKENTYPE.RBRACE)

        return block
    def parseStructDefinition(self):
        self.eat(TOKENTYPE.STRUCT_DEFINITION)
        name = self.eat(TOKENTYPE.NAME).value
        body = self.parseBlock()
        return StructDefinition(name, body)
    def parseWhileStatement(self):
        self.eat(TOKENTYPE.WHILE)
        condition = self.parseExpression()
        body = self.parseBlock()
        return WhileStatement(condition, body)
    def parseFunctionParameters(self):
        params = []
        while self.curToken().type != TOKENTYPE.LBRACE:
            # Skip newline
            self.skipWhitespace()
            if self.curToken().type == TOKENTYPE.NULL: 
                self.eat(TOKENTYPE.NULL)
                params.append(TOKENTYPE.NULL.lower())
                continue
            datatype = self.parseDataType()
            if self.peek().type == TOKENTYPE.NULL:
                self.eat(TOKENTYPE.NULL)
                return []
            name = self.eat(TOKENTYPE.NAME).value
            self.variable_types[name] = datatype
            params.append(
                Variable(
                    name,
                    datatype
                )
            )
                
            if self.curToken().type == TOKENTYPE.COMMA: self.eat(TOKENTYPE.COMMA)
        return params
    def parseFunctionDefinition(self):
        self.eat(TOKENTYPE.FUNCTION)
        name = self.eat(TOKENTYPE.NAME).value
        self.eat(TOKENTYPE.ARROW)
        return_type = self.parseDataType()
        self.function_returns[name] = return_type
        params = []

        if self.curToken().type == TOKENTYPE.COLON:
            self.eat(TOKENTYPE.COLON)
            params = self.parseFunctionParameters()
        body = self.parseBlock()

        return FunctionDefinition(name, params, return_type, body)
    def parseFunctionArgs(self):
        
        self.eat(TOKENTYPE.LPAREN)
        params = []
        while self.curToken().type != TOKENTYPE.RPAREN:
            params.append(self.parseExpression())

            if self.curToken().type == TOKENTYPE.COMMA: 
                self.eat(TOKENTYPE.COMMA)

        self.eat(TOKENTYPE.RPAREN)

        return params
    def parseFunctionCall(self):

        name = self.eat(TOKENTYPE.NAME).value
        self.eat(TOKENTYPE.COLON)
        args = self.parseFunctionArgs()
        return FunctionCall(name, self.function_returns[name], args)
        
    def parseReturnStatement(self):
        self.eat(TOKENTYPE.RETURN)
        exp = self.parseExpression()
        return ReturnStatement(exp)
    def skipWhitespace(self):
        while self.tokens[self.current].type == TOKENTYPE.NEWLINE: 
            self.advance()
    def parseElifStatement(self):
        self.eat(TOKENTYPE.ELIF)
        condition = self.parseExpression()
        block = self.parseBlock()
        else_block = None
        self.skipWhitespace()
        if self.curToken().type == TOKENTYPE.ELIF:
            else_block = self.parseElifStatement()
        elif self.curToken().type == TOKENTYPE.ELSE:
            else_block = self.parseElseStatement()
        return ElifStatement(condition, block, else_block)
    def parseElseStatement(self):
        self.eat(TOKENTYPE.ELSE)
        block = self.parseBlock()
        return ElseStatment(block)
    def parseIfStatement(self):

        # Advance without eating just to make sure we can handle elif and else
        self.eat(TOKENTYPE.IF)
        condition: Expression = self.parseExpression()

        block: list[Statement] = self.parseBlock()
        else_block: list[Statement] = None
        self.skipWhitespace()

        if self.curToken().type == TOKENTYPE.ELIF:
            else_block = self.parseElifStatement()
        elif self.curToken().type == TOKENTYPE.ELSE:
            else_block = self.parseElseStatement()
        
        return IfStatement(condition, block, else_block)
    
    def parseVariableAssignment(self):
        variable = self.eat(TOKENTYPE.NAME).value
        # Check for struct variable access
        if self.curToken().type == TOKENTYPE.DOT:
            self.eat(TOKENTYPE.DOT)
            access = self.eat(TOKENTYPE.NAME).value
            variable = VariableAccess(variable, access)
        else:
            variable = Variable(variable, self.variable_types[variable])
        self.eat(TOKENTYPE.EQUAL)
        expression = self.parseExpression()
        return Assignment(variable, expression)
    
    def parseDataType(self):
        data_type = self.eatAny(token.DATA_TYPES)
        sub_type = None
        if data_type.type in (TOKENTYPE.LIST, TOKENTYPE.STRUCT) :
            sub_type = self.eatAny(token.DATA_TYPES) if data_type.type == TOKENTYPE.LIST else self.eat(TOKENTYPE.NAME)
            return TOKEN_TO_DATA_TYPE_MAP[data_type.type](
                TOKEN_TO_DATA_TYPE_MAP[sub_type.type] if sub_type.type in TOKEN_TO_DATA_TYPE_MAP else sub_type.value
            )
        else: return TOKEN_TO_DATA_TYPE_MAP[data_type.type]()
    def parseVariableDeclaration(self):
        data_type = self.parseDataType()
        variable = self.curToken().value
        variable = variable
        self.eat(TOKENTYPE.NAME)
        expression = NullLiteral()
        if self.curToken().type == TOKENTYPE.EQUAL:
            self.eat(TOKENTYPE.EQUAL)
            expression = self.parseExpression()
        self.variable_types[variable] = data_type
        return VariableDeclaration(variable, data_type, expression)
    def parseForStatement(self):
        self.eat(TOKENTYPE.FOR)
        start = self.parseNode()
        self.eat(TOKENTYPE.COLON)
        end = self.parseNode()
        self.eat(TOKENTYPE.COLON)
        step = self.parseNode()
        body = self.parseBlock()
        return ForStatement(start, end, step, body)
    def parseExpression(self, precedence=0):
        cur = self.curToken()
        if cur.type in UNARY_OPERATORS:
            self.advance()
            operand = self.parseExpression(ORDER_OF_OPERATIONS[cur.type][1])
            return UnaryOperation(cur.value, operand)

        left = self.parseAtom()
        while True:
            cur = self.curToken()
            if cur.type not in ORDER_OF_OPERATIONS or ORDER_OF_OPERATIONS[cur.type][1] < precedence:
                break

            associativity, op_precedence = ORDER_OF_OPERATIONS[cur.type]
            next_precedence = op_precedence + 1 if associativity == 'LEFT' else op_precedence
            self.advance()
            right = self.parseExpression(next_precedence)
            left = BinaryOperation(left, cur.value, right)

        return left
    def handle_struct_variable_access(self, struct):
        self.eat(TOKENTYPE.DOT)
        access = self.eat(TOKENTYPE.NAME).value
        sv = VariableAccess(struct, access)
        
        while self.curToken().type == TOKENTYPE.DOT:
            self.eat(TOKENTYPE.DOT)
            access = self.eat(TOKENTYPE.NAME).value
            sv = VariableAccess(sv, access)
        
        if self.curToken().type == TOKENTYPE.EQUAL:
            self.eat(TOKENTYPE.EQUAL)
            expression = self.parseExpression()
            return AccessAssignment(sv, expression)
        
        # Handle binary operations like a.x += 1
        if self.curToken().type in ORDER_OF_OPERATIONS:
            operator = self.eatAny(ORDER_OF_OPERATIONS).value
            right_expression = self.parseExpression()
            expression = BinaryOperation(sv, operator, right_expression)
            return AccessAssignment(sv, expression)
        
        return sv
    def parseStructCreationBlock(self):
        self.eat(TOKENTYPE.LBRACE)
        block = []
        while self.curToken().type != TOKENTYPE.RBRACE:
            # get declarations
            data_type = self.parseDataType()
            variable = self.eat(TOKENTYPE.NAME).value
            expression = NullLiteral()
            if self.curToken().type == TOKENTYPE.EQUAL:
                self.eat(TOKENTYPE.EQUAL)
                expression = self.parseExpression()
            block.append(VariableDeclaration(variable, data_type, expression))
            self.eat(TOKENTYPE.COLON)
        return block
    def parseAtom(self):
        cur = self.curToken()
        if cur.type == TOKENTYPE.INT_LITERAL:
            self.advance()
            return IntLiteral(int(cur.value))
        elif cur.type == TOKENTYPE.NULL:
            self.eat(TOKENTYPE.NULL)
            return NullLiteral()
        elif cur.type == TOKENTYPE.FLOAT_LITERAL:
            self.advance()
            return FloatLiteral(float(cur.value))
        elif cur.type == TOKENTYPE.CREATE:
            self.eat(TOKENTYPE.CREATE)
            name = self.eat(TOKENTYPE.NAME).value
            body = self.parseStructCreationBlock()
            return StructCreation(name, body)
        elif cur.type == TOKENTYPE.NAME:

            # Shit hack to fix shit grammar. What the fuck is this: <name> : (<arg1>,<arg2>,etc.)
            if self.peek().type == TOKENTYPE.COLON and cur.value in self.function_returns:
                # function call
                return self.parseFunctionCall()

            if self.peek().type == TOKENTYPE.DOT:
                # Struct variable access
                struct = self.eat(TOKENTYPE.NAME).value
                return self.handle_struct_variable_access(struct)
            name = self.eat(TOKENTYPE.NAME).value
            return Variable(name)
        elif cur.type == TOKENTYPE.LPAREN:
            self.advance()
            expr = self.parseExpression()
            if self.curToken().type != TOKENTYPE.RPAREN:
                self.throwError("Expected ')'")
            self.advance()
            return expr
        elif cur.type == TOKENTYPE.STRING_LITERAL:
            self.advance()
            # Pre-processing for special escape characters
            cur.value = cur.value\
                        .replace("\\n","\n")\
                        .replace("\\t","\t")\
                        .replace("\\r","\r")\
                        .replace("\\\\","\\")\
                        .replace("\\\"","\"")\
                        .replace("\\'","'")



            return StringLiteral(cur.value)
        elif cur.type == TOKENTYPE.BOOL_LITERAL:
            self.advance()
            return BooleanLiteral(cur.value == "true")
        elif cur.type == TOKENTYPE.LBRACKET:
            self.eat(TOKENTYPE.LBRACKET)
            items = []
            while self.curToken().type != TOKENTYPE.RBRACKET:
                items.append(self.parseExpression())
                if self.curToken().type != TOKENTYPE.RBRACKET: self.eat(TOKENTYPE.COMMA)
            self.eat(TOKENTYPE.RBRACKET)
            return ListLiteral(items)
        else:
            self.throwError(f"Unexpected token {cur.type} on line: {cur.line} col: {cur.column}")


