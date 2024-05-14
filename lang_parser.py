import tokens as token
from tokens import TOKENTYPE
from lexer import Lexer
import std
from parserOptions import ORDER_OF_OPERATIONS
from parserNode import *

import tokens as token
from lexer import Lexer
import std
from parserOptions import ORDER_OF_OPERATIONS, TOKEN_TO_DATA_TYPE_MAP
from parserNode import *
from sys import argv
class Parser:
    def __init__(self):
        self.tokens = []
        self.ast = []
        self.current = 0

    def throwError(self, message):
        raise std.LangError(message)

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
        return self.ast


    def parseNode(self):

        if self.curToken().type in token.DATA_TYPES:
            return self.parseVariableDeclaration()
        elif self.curToken().type == TOKENTYPE.NAME:
            return self.handleName()
        elif self.curToken().type == TOKENTYPE.FOR:
            return self.parseForStatement()
        elif self.curToken().type == TOKENTYPE.FUNCTION:
            return self.parseFunctionDefinition()
        elif self.curToken().type == TOKENTYPE.RETURN:
            return self.parseReturnStatement()
        elif self.curToken().type in token.ATOMS:
            return self.parseExpression()
        elif self.curToken().type == TOKENTYPE.IF:
            return self.parseIfStatement()
        elif self.curToken().type == TOKENTYPE.WHILE:
            return self.parseWhileStatement()
        elif self.curToken().type == TOKENTYPE.NEWLINE:
            self.eat(TOKENTYPE.NEWLINE)
            return self.parseNode()
        elif self.curToken().type == TOKENTYPE.EOF:
            return None
        self.throwError(f"Unexpected token {self.curToken().type}")
    def parseMethodCall(self):
        """
        requires: curToken == TOKENTYPE.NAME
        """
        struct = self.eat(TOKENTYPE.NAME).value
        self.eat(TOKENTYPE.DOT)
        func = self.eat(TOKENTYPE.NAME).value
        self.eat(TOKENTYPE.COLON)
        args = self.parseFunctionArgs()
        return StructMethodCall(struct, func, args)
    def handleName(self):
        print("HANDLING NAME",self.curToken(),self.peek())
        if self.peek().type == TOKENTYPE.EQUAL :
            return self.parseVariableAssignment()
        elif self.peek().type == TOKENTYPE.COLON:
            print("FUNC CALL")
            return self.parseFunctionCall()
        elif self.peek().type == TOKENTYPE.DOT and self.peek(3).type == TOKENTYPE.COLON:
            print("METHOD CALL")
            return self.parseMethodCall()
        elif self.peek().type == TOKENTYPE.DOT:
            print("STRUCT VARIABLE ASSIGNMENT")
            return self.parseVariableAssignment()
        else:
            self.throwError(f"Unexpected token {self.curToken().type}")
    def parseBlock(self):

        # Eat leading brace
        self.skipWhitespace()
        self.eat(TOKENTYPE.LBRACE)

        # Init block list
        block = []
        self.skipWhitespace()
        #print(self.curToken())
        # While the block is not finished
        while self.curToken().type != TOKENTYPE.RBRACE: 
            # Parse the line
            block.append(self.parseNode())
            self.skipWhitespace()

        # Return the block
        self.eat(TOKENTYPE.RBRACE)

        return block
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
            params.append(self.eatAny([TOKENTYPE.NAME, TOKENTYPE.NULL]).value)
            if self.curToken().type == TOKENTYPE.COMMA: self.eat(TOKENTYPE.COMMA)
        if len(params) == 1 and params[0] == TOKENTYPE.NULL.lower(): return []
        return params
    def parseFunctionDefinition(self):
        self.eat(TOKENTYPE.FUNCTION)
        name = self.eat(TOKENTYPE.NAME).value
        params = []
        if self.curToken().type == TOKENTYPE.COLON:
            self.eat(TOKENTYPE.COLON)
            params = self.parseFunctionParameters()
        body = self.parseBlock()
        return FunctionDefinition(name, params, body)
    def parseFunctionArgs(self):
        params = []
        while self.curToken().type != TOKENTYPE.NEWLINE:
            try:
                params.append(self.parseExpression())
            except:
                self.curToken().type == TOKENTYPE.NULL
                params.append(TOKENTYPE.NULL.lower())
                self.eat(TOKENTYPE.NULL)
            if self.curToken().type == TOKENTYPE.COMMA: self.eat(TOKENTYPE.COMMA)
        if len(params) == 1 and params[0] == TOKENTYPE.NULL.lower(): return []
        return params
    def parseFunctionCall(self):
        print("FUNC CALL")
        name = self.eat(TOKENTYPE.NAME)
        self.eat(TOKENTYPE.COLON)
        args = self.parseFunctionArgs()
        return FunctionCall(name, args)
        
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
        
        return IFStatement(condition, block, else_block)
    
    def parseVariableAssignment(self):
        variable = self.eat(TOKENTYPE.NAME).value
        # Check for struct variable access
        #print("ASSIGNMENT", self.curToken(),self.peek(),self.peek(2))
        if self.curToken().type == TOKENTYPE.DOT:
            self.eat(TOKENTYPE.DOT)
            access = self.eat(TOKENTYPE.NAME).value
            variable = StructVariable(variable, access)
        else:
            variable = Variable(variable)
        self.eat(TOKENTYPE.EQUAL)
        expression = self.parseExpression()
        return Assignment(variable, expression)
    def parseDataType(self):
        data_type = self.eatAny(token.DATA_TYPES)
        sub_type = None
        if data_type.type in (TOKENTYPE.LIST):
            sub_type = self.eatAny(token.DATA_TYPES)
        if sub_type: return TOKEN_TO_DATA_TYPE_MAP[data_type.type](TOKEN_TO_DATA_TYPE_MAP[sub_type.type])
        else: return TOKEN_TO_DATA_TYPE_MAP[data_type.type]()
    def parseVariableDeclaration(self):
        data_type = self.parseDataType()
        variable = self.curToken().value
        variable = Variable(variable)
        self.eat(TOKENTYPE.NAME)
        expression = None
        if self.curToken().type == TOKENTYPE.EQUAL:
            self.eat(TOKENTYPE.EQUAL)
            expression = self.parseExpression()
        return VariableDeclaration(variable, data_type, expression)
    def parseForStatement(self):
        self.eat(TOKENTYPE.FOR)
        variable = self.parseVariableDeclaration()
        self.eat(TOKENTYPE.COLON)
        range = self.parseExpression()
        body = self.parseBlock()
        return ForStatement(variable, range, body)

    def parseExpression(self, precedence=0):
        left = self.parseAtom()

        while True:
            cur = self.curToken()
            if cur.type not in ORDER_OF_OPERATIONS or ORDER_OF_OPERATIONS[cur.type][1] < precedence:
                break

            associativity, op_precedence = ORDER_OF_OPERATIONS[cur.type]
            if associativity == 'LEFT':
                next_precedence = op_precedence + 1
            else:
                next_precedence = op_precedence

            self.advance()
            right = self.parseExpression(next_precedence)
            left = BinaryOperation(left, cur, right)

        return left

    def parseAtom(self):
        cur = self.curToken()
        if cur.type == TOKENTYPE.INT_LITERAL:
            self.advance()
            return IntLiteral(int(cur.value))
        elif cur.type == TOKENTYPE.STRUCT_LITERAL:
            self.advance()
            return StructLiteral(self.parseBlock())
        elif cur.type == TOKENTYPE.FLOAT_LITERAL:
            self.advance()
            return FloatLiteral(float(cur.value))
        elif cur.type == TOKENTYPE.CREATE:
            self.advance()
            return StructCreation(self.eat(TOKENTYPE.NAME).value)
        elif cur.type == TOKENTYPE.NAME:

            print("GOT NAME EXPRESSION", cur, self.curToken(), self.peek())
            if self.peek().type == TOKENTYPE.COLON:
                # function call
                return self.parseFunctionCall()

            if self.peek().type == TOKENTYPE.DOT:
                print("GOT DOT")
                if self.peek(3).type == TOKENTYPE.COLON:
                    print("COLONNNN")
                    # Struct method call
                    return self.parseMethodCall()
                # Struct variable access
                struct = self.eat(TOKENTYPE.NAME).value
                self.eat(TOKENTYPE.DOT)
                name = self.eat(TOKENTYPE.NAME)
                return StructVariable(struct, name)
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
            self.throwError(f"Unexpected token {cur.type}")





if __name__ == "__main__":
    text = open(argv[1],'r').read()
    t = Lexer(text).tokenize()
    parser = Parser()
    ast = parser.parse(t)
    print("-"*10 + " AST " + "-"*10)
    print(ast)
