"""This module is the starting point of my compiler"""

import sys
from src.emitter import Emitter
from src.lex import Lexer
from src.parse import Parser


def main():
    """Runs the compiler"""

    print("My compiler")

    if len(sys.argv) != 2:
        sys.exit("Error: Compiler needs source file as argument.")

    with open(sys.argv[1], "r", encoding="utf-8") as input_file:
        source = input_file.read()

    lexer = Lexer(source)
    emitter = Emitter("out.c")
    parser = Parser(lexer, emitter)

    parser.program()
    emitter.write_file()
    print("Parsing completed.")


main()
