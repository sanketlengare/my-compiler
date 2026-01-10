"""Represents server"""

import os
from flask import Flask, request, jsonify
from flask_cors import CORS

from src.code_gen import CodeGenerator
from src.lex import Lexer
from src.parse import Parser

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})


@app.route("/compile", methods=["POST"])
def compile_code():
    """Endpoint for source code"""

    data = request.json
    source_code = data.get("code", "")

    if not source_code:
        return jsonify({"error", "No code provided"}), 400

    try:

        lexer = Lexer(source_code)
        parser = Parser(lexer)

        program = parser.program()

        generator = CodeGenerator()
        c_code = generator.visit_program(program)

        ast_json = program.to_dict()

        return jsonify({"c_code": c_code, "ast": ast_json})

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    # Use the PORT provided by the cloud, or default to 5000 locally
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
