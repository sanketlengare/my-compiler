class AST:
    """Represemts an AST node"""

    def to_dict(self):
        """*"""


class Num(AST):
    """Represents a Num type node"""

    def __init__(self, token):
        self.token = token
        self.value = token.text

    def to_dict(self):
        """Return a dictionary format of current object"""
        return {"type": "Num", "value": self.value}

    def __repr__(self):
        return f"Num({self.value})"


class Float(AST):
    """Represents a Float type node"""

    def __init__(self, token):
        self.token = token
        self.value = token.text

    def to_dict(self):
        """Return a dictionary format of current object"""
        return {"type": "Float", "value": self.value}

    def __repr__(self):
        return f"Float({self.value})"


class String(AST):
    """Represents a String type node"""

    def __init__(self, token):
        self.token = token
        self.value = token.text

    def to_dict(self):
        """Return a dictionary format of current object"""
        return {"type": "String", "value": self.value}

    def __repr__(self):
        return f"String({self.value})"


class Var(AST):
    """Represents a Var type node"""

    def __init__(self, token):
        self.token = token
        self.value = token.text

    def to_dict(self):
        """Return a dictionary format of current object"""
        return {"type": "Var", "value": self.value}

    def __repr__(self):
        return f"Var({self.value})"


class Bin_Op(AST):
    """Represents conjunction of right and left children in the tree"""

    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

    def to_dict(self):
        """Return a dictionary format of current object"""

        return {
            "type": "Bin_Op",
            "operator": self.op.text,
            "left": self.left.to_dict(),
            "right": self.right.to_dict(),
        }

    def __repr__(self):
        return f"Bin_Op{self.left, self.op.text, self.right}"


class Print(AST):
    """Represents the print token"""

    def __init__(self, expression):
        self.expression = expression

    def to_dict(self):
        return {"type": "Print", "expression": self.expression.to_dict()}

    def __repr__(self):
        return f"Print({self.expression})"


class Program(AST):
    """Represents a program (collection of statements)"""

    def __init__(self, statements):
        self.statements = statements

    def to_dict(self):
        """Return a dictionary format of current object"""
        return {
            "type": "Program",
            "statements": [stm.to_dict() for stm in self.statements],
        }

    def __repr__(self):
        return f"Program({self.statements})"


class Let(AST):
    """Represets a LET token"""

    def __init__(self, name_token, expression):
        self.name_token = name_token
        self.expression = expression

    def to_dict(self):
        return {
            "type": "Let",
            "name_token": self.name_token.text,
            "value": self.expression.to_dict(),
        }

    def __repr__(self):
        return f"Let({self.name_token.text}, {self.expression})"


class Input(AST):
    """Represents an Input token"""

    def __init__(self, input_token):
        self.input_token = input_token

    def to_dict(self):
        return {"type": "Input", "value": self.input_token.text}

    def __repr__(self):
        return f"Input({self.input_token.text})"


class Label(AST):
    """Represents a Label token"""

    def __init__(self, token):
        self.value = token

    def to_dict(self):
        return {"type": "Label", "value": self.value.text}

    def __repr__(self):
        return f"Label({self.value.text})"


class Goto(AST):
    """Represents a Goto token"""

    def __init__(self, token):
        self.value = token

    def to_dict(self):
        return {"type": "Goto", "value": self.value.text}

    def __repr__(self):
        return f"Goto({self.value.text})"


class If(AST):
    """Represents an If token"""

    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

    def to_dict(self):
        return {
            "type": "If",
            "condition": self.condition.to_dict(),
            "body": [b.to_dict() for b in self.body],
        }

    def __repr__(self):
        return f"If{self.condition, self.body}"


class While(AST):
    """Represents a While token"""

    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

    def to_dict(self):
        return {
            "type": "While",
            "condition": self.condition.to_dict(),
            "body": [b.to_dict() for b in self.body],
        }

    def __repr__(self):
        return f"While({self.condition, self.body})"
