"""Pygments lexer for OpenSSL configuration files

With inspiration from IniLexer and BashLexer.
"""

from pygments.lexer import Lexer, LexerContext, RegexLexer, ExtendedRegexLexer, \
    bygroups, include, using, this, do_insertions
from pygments.token import Punctuation, Text, Comment, Keyword, Name, String, \
    Generic, Operator, Number, Whitespace, Literal

T_LHS = Name.Attribute
T_RHS = String
T_SPACE = Text


class OpenSSLConfLexer(RegexLexer):
    """
    Lexer for `OpenSSL <http://openssl.org/docs/apps/config.html>`_ configuration files.
    """

    name = 'OpenSSL'
    aliases = ['openssl']
    filenames = ['*.cnf', '*.conf']
    mimetypes = ['text/x-openssl']

    tokens = {
        'root': [
            # Comment
            (r'#.*\n', Comment),
            # Section header
            (r'\[.*?\]\n', Keyword),
            # Left hand side
            (r'(\b[^\s]+)(\s*)', bygroups(T_LHS, T_SPACE)),
            # Operator
            (r'(=)(\s*)', bygroups(Operator, T_SPACE), 'rhs'),
            # Line continuation
            (r'\\(?=\n)', String.Escape),
            # Whitespace
            (r'\s+', T_SPACE),
            # Catch all
            (r'.', T_LHS),
        ],
        'rhs': [
            # Comment
            (r'#.*(?=\n)', Comment),
            # Exit condition
            (r'(?<!\\)\n', T_SPACE, '#pop'),
            # Double-quoted string
            (r'(?s)"(\\\\|\\[0-7]+|\\.|[^"\\])*"', String.Double),
            # Single-quoted string
            (r"(?s)'(\\\\|\\[0-7]+|\\.|[^'\\])*'", String.Single),
            # Variable name inside curly braces
            (r'\${', Name.Variable, 'curly-brace'),
            # Variable name
            (r'\$\w+(?:::\w+)?', Name.Variable),
            # OID
            (r'(?<=\W)\d+\.(?:\d+\.?)*(?=\W)', Name.Function),
            # Number
            (r'(?<=\W)\d+(?=\W)', T_RHS),
            # Section reference
            (r'\@\w+', Name.Constant),
            # Critical keyword
            (r'(?i)(?<=\W)critical(?=\W)', Keyword.Pseudo),
            # Line continuation
            (r'\\(?=\n)', String.Escape),
            # Whitespace
            (r'\s+', T_SPACE),
            # Catch all
            (r'.', T_RHS),
        ],
        'curly-brace': [
            # Exit condition
            (r'}', Name.Variable, '#pop'),
            # Variable name
            (r'\w+(?:::\w+)?', Name.Variable, 'close-brace'),
            # Catch all
            (r'[^}]+', T_RHS),
        ],
        'close-brace': [
            # Exit condition
            (r'}', Name.Variable, '#pop:2'),
            # Catch all
            (r'[^}]+', T_RHS),
        ],
    }

    def analyse_text(text):
        npos = text.find('\n')
        if npos < 3:
            return False
        return text[0] == '[' and text[npos-1] == ']'

