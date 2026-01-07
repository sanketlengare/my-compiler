"""Class defines an emitter"""

from .ast import *


class CodeGenerator:
    """Represents a code generator object that goes through the AST to emit C code"""

    def __init__(self):
        self.code = ""
        self.vars_declared = {}

    def generate(self, node):
        """Calls visit function respective to node"""

        method_name = f"visit_{node.__class__.__name__.lower()}"
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def visit_num(self, node):
        """Emits value at AST node type Num"""
        return node.value

    def visit_float(self, node):
        """Emits value at AST node type Float"""
        return node.value

    def visit_string(self, node):
        """Emits value at AST node type String"""
        return f'"{node.value}"'

    def visit_var(self, node):
        """Emits value at AST node type Var"""
        return node.value

    def visit_bin_op(self, node):
        """Emits value at AST node type Bin_Op"""
        return f"{self.generate(node.left)} {node.op.text} {self.generate(node.right)}"

    def visit_print(self, node):
        """Emits value at AST node type Print"""

        expr_code = self.generate(node.expression)

        if expr_code.startswith('"'):
            return f'printf("%s\\n", {expr_code});'

        else:
            return f'printf("%.2f\\n", (float) {expr_code});'

    def visit_program(self, node):
        """Emits value at AST node type Program"""

        full_code = "#include <stdio.h>\n\n"
        full_code += "int main(void) {\n"

        for stm in node.statements:
            code_segment = self.generate(stm)
            full_code += "  " + code_segment + "\n"

        full_code += "    return 0; \n"
        full_code += "}"

        return full_code

    def visit_let(self, node):
        """Emits value at AST node type Let"""

        rhs = self.generate(node.expression)
        var_name = node.name_token.text
        c_type = self.get_c_type(node.expression)

        if var_name not in self.vars_declared:
            self.vars_declared[var_name] = c_type
            return f"{c_type} {var_name} = {rhs};"

        else:
            return f"{var_name} = {rhs};"

    def visit_input(self, node):
        """Emits value at node type Input"""

        var_name = node.input_token.text

        if var_name not in self.vars_declared:
            self.vars_declared[var_name] = "float"
            return f'float {var_name};\n  scanf("%f", &{var_name});'

        else:

            curr_type = self.vars_declared[var_name]

            match curr_type:
                case "int":
                    return f'scanf("%d", &{var_name})'

                case "float":
                    return f'scanf("%f", &{var_name})'

                case _:
                    return f'scanf("%f", &{var_name})'

    def visit_label(self, node):
        """Emits value at AST node type Label"""

        value = node.value.text
        return f"{value}:"

    def visit_goto(self, node):
        """Emits value at AST node type Goto"""

        value = node.value.text
        return f"goto {value};"

    def visit_if(self, node):
        """Emits value at AST node type If"""

        cond = self.generate(node.condition)

        full_code = "if (" + cond + ") {\n"

        for b in node.body:
            b_segment = self.generate(b)
            full_code += "    " + b_segment + "\n"

        full_code += "  }"
        return full_code

    def visit_while(self, node):
        """Emits value at AST node type While"""

        cond = self.generate(node.condition)

        full_code = "while (" + cond + ") {\n"

        for b in node.body:
            b_segment = self.generate(b)
            full_code += "    " + b_segment + "\n"

        full_code += "  }"
        return full_code

    def get_c_type(self, node):
        """Helper to infer C type of node"""

        if isinstance(node, String):
            return "char *"

        if isinstance(node, Num):
            return "int"

        if isinstance(node, Float):
            return "float"

        if isinstance(node, Bin_Op):
            return "float"

        if isinstance(node, Var):
            if node.value in self.vars_declared:
                return self.vars_declared[node.value]
            else:
                raise Exception(f"Variable '{node.value}' not found")

        raise Exception(f"Cannot determine type for {node}")

    def generic_visit(self, node):
        raise Exception(f"No visit__{node.__class__.__name__.lower()} method")
