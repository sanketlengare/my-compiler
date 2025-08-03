"""Lexer class to break input string into tokens"""


class Lexer:
    """Lexer needs to keep track of the current position in the input
    string and characters at that position"""

    def __init__(self, source):
        self.source = (
            source + "\n"
        )  # Source code. Newline to simplify lexing/ parsing the last token
        self.cur_char = ""
        self.cur_pos = -1
        self.next_char()

    def next_char(self):
        """Process the next character"""

        self.cur_pos += 1
        if self.cur_pos + 1 >= len(self.source):
            self.cur_char = "\0"  # EOF
        else:
            self.cur_char = self.source[self.cur_pos]

    def peek(self):
        """Return the lookahead charcter."""

        if self.cur_pos + 1 >= len(self.source):
            return "\0"
        return self.source[self.cur_pos + 1]

    def abort(self, message):
        """Invalid token found, print error message and exit."""

    def skip_whitespace(self):
        """Skip whitespace except newlines, which we will use to indicate the end of a statement"""

    def skip_comment(self):
        """Skip commnets in the code."""

    def get_token(self):
        """Return the next token
        Will do the work of classifying tokens"""
