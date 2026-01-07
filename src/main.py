"""This module is the starting point of my compiler"""

import sys
import json
from src.code_gen import CodeGenerator
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
    code_generator = CodeGenerator()

    # parser.program()
    tree = parser.program()
    json_output = tree.to_dict()
    c_output = code_generator.generate(tree)

    with open("ast.json", "w") as output_file:
        json.dump(json_output, output_file, indent=4)

    with open("out.c", "w") as file:
        file.write(c_output)

    print("Parsing completed.")


main()
