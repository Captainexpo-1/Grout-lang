from langParser import Parser
from lexer import Lexer, tokenize

from sys import argv, setrecursionlimit
import time
import os

# Finding bottleneck
import cProfile
import pstats

if "-eval" in argv: Evaluator = __import__("evaluator_v"+argv[argv.index("-eval")+1]).Evaluator

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


evaluator = None
tree = None
def run_evaluator():
    evaluator.evaluate(tree)

def run_file(file):
    lexer = Lexer()
    parser = Parser()
    with open(file) as f:
        text = f.read()
    tokens = lexer.tokenize(text)
    if show_tokens:
        print_tokens(tokens)
    global evaluator, tree # Just for profiling
    
    tree = parser.parse(tokens)
    if show_ast:
        print(tree)

    evaluator = Evaluator(verbose_override=("-v" in argv))

    #evaluator.evaluate(tree)
    if not do_profile:
        evaluator.evaluate(tree)
    else:
        # Create the profiling folder if it doesn't exist
        if "profiles" not in os.listdir(os.path.dirname(__file__)):
            os.mkdir(profile_dir_name)

        # Run the evaluator with the profiler
        cProfile.run("evaluator.evaluate(tree)", "./profiles/profile.prof")
        
        # Dump the stats
        p = pstats.Stats("./profiles/profile.prof")
        p.sort_stats("cumulative").print_stats(10)
        
        # Cleanup the profiles directory
        if delete_profile_after:
            for i in os.listdir(profile_dir_name):
                os.remove(profile_dir_name+"/"+i )
            os.rmdir(profile_dir_name)


    if do_time:
        print(f"\nTime taken: {time.time() - start}")

    if "-vars" in argv:
        print(evaluator.global_env)

    
do_time = False
do_profile, delete_profile_after = False, True
profile_dir_name = os.path.dirname(__file__)+"/profiles"
start = time.time()
def main():
    # parse args:
    args = argv[1:]
    if "-ast" in args:
        global show_ast
        show_ast = True
    if "-profile" in args:
        global do_profile
        do_profile = True
    if "-no-profile-delete" in args:
        global delete_profile_after
        delete_profile_after = False
    if "-tokens" in args:
        global show_tokens
        show_tokens = True
    if "-no-recursion-limit" in args:
        setrecursionlimit(10**6)
    if "-time" in args:
        global do_time
        do_time = True
    if "-f" in args:
        run_file(args[args.index("-f") + 1])
    else:
        print("Invalid arguments")
        print("Usage: python main.py [-f file]")
        print("Options:")
        print("  -f file: Execute the file")
    
if __name__ == "__main__":
    main()
