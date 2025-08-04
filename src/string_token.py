"""Class defines a token object"""

from token_type import TokenType


class Token:
    """Token contains the original text and the type of token"""

    def __init__(self, token_text, token_kind):
        self.text = token_text
        self.kind = token_kind

    @staticmethod
    def check_if_keyword(token_text):
        """Checks if text contains token"""

        for kind in TokenType:
            if kind.name == token_text and kind.value >= 100 and kind.value < 200:
                return kind

        return None
