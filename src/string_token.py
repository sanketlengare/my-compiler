"""Class defines a token object"""


class Token:
    """Token contains the original text and the type of token"""

    def __init__(self, token_text, token_kind):
        self.text = token_text
        self.kind = token_kind
