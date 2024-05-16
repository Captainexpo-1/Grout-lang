import tokens as token

class Lexer:
    def __init__(self, text=None):
        self.text = text+("\n" if text[-1] != "\n" else "")
        self.pos = 0
        self.current_line = 1
        self.current_column = 1
        self.current_char = self.text[self.pos] if self.text else None
        self.tokens = []
        self.token_rules = token.TOKEN_RULES
        self.token_priority = token.TOKEN_PRIORITY

    def error(self, character=''):
        raise Exception(f"Invalid character: {character} at line {self.current_line}, column {self.current_column}")

    def advance(self):
        if self.current_char == '\n':
            self.current_line += 1
            self.current_column = 0
        self.pos += 1
        self.current_column += 1

        if self.pos > len(self.text) - 1:
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            if self.current_char == '\n':
                self.current_line += 1
                self.current_column = 0
                self.tokens.append(token.Token(token.TOKENTYPE.NEWLINE, "\\n", line=self.current_line, column=self.current_column))
            else:
                self.current_column += 1
            self.advance()

    def get_next_token(self):
        while self.current_char is not None:
            for token_type in self.token_priority:
                match = self.token_rules[token_type].match(self.text, self.pos)
                
                if match:
                    token_value = match.group(0)
                    token_start = match.start()
                    token_end = match.end()
                    line = self.current_line
                    column = self.current_column + (token_start - self.pos)
                    self.pos = token_end

                    if self.pos >= len(self.text):
                        self.current_char = None
                    else:
                        self.current_char = self.text[self.pos]

                    if token_value:
                        return token.Token(token_type, token_value, line=line, column=column)
            self.error(self.current_char)

    def tokenize(self):
        while self.current_char is not None:
            self.skip_whitespace()
            next_token = self.get_next_token()
            if next_token:
                if next_token.type != token.TOKENTYPE.COMMENT:
                    self.tokens.append(next_token)
            else:
                self.tokens.append(token.Token(token.TOKENTYPE.EOF, ""))
        return self.tokens

def tokenize(text):
    lexer = Lexer(text)
    return lexer.tokenize()

if __name__ == "__main__":
    t=tokenize(
"""
fn factorial -> int : int n {
    if n == 0 {
        return 1
    }
    return n * factorial : (n - 1)
}


fn main -> int : {
    int n = 5
    int result = factorial : (n)
    print : ("Factorial of", n, "is", result)
    return 0
}

main: ()
"""
    )
    for i in t:
        if i.type != token.TOKENTYPE.NEWLINE:
            print(i,end=" ")
        else:
            print(end="\n")