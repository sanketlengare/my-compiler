"""This module is the starting point of my compiler"""

import sys
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
    parser = Parser(lexer)

    parser.program()
    print("Parsing completed.")


main()
