from lang_parser import Parser
from lexer import Lexer, tokenize
from evaluator import Evaluator
from sys import argv

show_tokens = False
show_ast = False

def _repl_mode():
    lexer = Lexer()
    parser = Parser()
    while True:
        try:
            text = input(">> ")
        except EOFError:
            break
        if not text:
            continue
        tokens = lexer.tokenize(text)
        tree = parser.parse(tokens)
        evaluator = Evaluator()
        evaluator.evaluate(tree)
def print_tokens(tokens):
    for token in tokens:
        print(token,end=" ")
        if token.type == "NEWLINE":
            print()
    print()
    
def _print_ast(tree):
    def print_node(node, indent=0):
        print("  " * indent + str(node))
        try: 
            for child in node.body:
                print_node(child, indent + 1)
        except: 
            pass
    print_node(tree)

def run_file(file):
    lexer = Lexer()
    parser = Parser()
    with open(file) as f:
        text = f.read()
    tokens = lexer.tokenize(text)
    if show_tokens:
        print_tokens(tokens)
    tree = parser.parse(tokens)
    if show_ast:
        print(tree)
    evaluator = Evaluator()
    evaluator.evaluate(tree)

def main():
    # parse args:
    args = argv[1:]
    if "-ast" in args:
        global show_ast
        show_ast = True
    if "-tokens" in args:
        global show_tokens
        show_tokens = True
    if "-f" in args:
        run_file(args[args.index("-f") + 1])
    else:
        print("Invalid arguments")
        print("Usage: python main.py [-f file]")
        print("Options:")
        print("  -f file: Execute the file")
    
if __name__ == "__main__":
    main()
