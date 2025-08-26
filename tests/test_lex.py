"""Lexer test module"""

import unittest

from src.token_type import TokenType
from src.lex import Lexer


class TestLex(unittest.TestCase):
    """Tests functions of Lexer"""

    def test_next_char(self):
        """Points to next character"""
        lexer = Lexer(source="Hi")
        lexer.next_char()
        self.assertEqual(lexer.cur_pos, 1)

    def test_peek_char(self):
        """Peeks the next character in source"""

        lexer = Lexer(source="Hi")
        self.assertEqual(lexer.cur_char, "H")
        self.assertEqual(lexer.peek(), "i")

    def test_peek_eof(self):
        """Peeks to end of line of string"""

        lexer = Lexer(source="H")
        self.assertEqual(lexer.cur_char, "H")
        self.assertEqual(lexer.peek(), "\n")

    def test_get_token(self):
        """Test for right token recognition"""

        lexer = Lexer(source="IF")
        token = lexer.get_token()
        print(token)
        if token is not None:
            self.assertEqual(token.kind, TokenType.IF)
