"""Pygments lexer for OpenSSL configuration files

With inspiration from IniLexer and BashLexer.
"""

from pygments.lexer import Lexer, LexerContext, RegexLexer, ExtendedRegexLexer, \
    bygroups, include, using, this, do_insertions, default
from pygments.token import Punctuation, Text, Comment, Keyword, Name, String, \
    Generic, Operator, Number, Whitespace, Literal

T_LHS = Name.Attribute
T_RHS = String

# Pygments 2.11 changed the whitespace token type
from pygments import lex, lexers
T_SPACE = list(lex(' ', lexers.get_lexer_by_name('ini')))[0][0]

T_NUMBER = T_RHS
T_EMAIL = T_RHS
T_IP = T_RHS
T_HEX = T_RHS

T_KNOWNDIR = Name.Builtin
T_OTHERDIR = T_LHS

T_KNOWNNAME = Keyword.Pseudo
T_OTHERNAME = T_RHS


class OpenSSLConfLexer(RegexLexer):
    """Pygments lexer for OpenSSL configuration files.
    """

    name = 'OpenSSL'
    aliases = ['openssl']
    filenames = ['*.cnf', '*.conf']
    mimetypes = ['text/x-openssl']

    tokens = {
        'comment': [
            # Comment
            (r'#.*(?=\n)', Comment),
        ],
        'string': [
            # Double-quoted string
            (r'(?s)"(\\\\|\\[0-7]+|\\.|[^"\\])*"', String.Double),
            # Single-quoted string
            (r"(?s)'(\\\\|\\[0-7]+|\\.|[^'\\])*'", String.Single),
        ],
        'variable': [
            # Variable name inside curly braces
            (r'\${', Name.Variable, 'curly-brace'),
            # Variable name inside parentheses
            (r'\$\(', Name.Variable, 'paren'),
            # Variable name
            (r'\$\w+(?:::\w+)?', Name.Variable),
        ],
        'number': [
            # Float
            (r'(?<=\W)\d+\.\d+(?=\W)', T_NUMBER),
            # Int
            (r'(?<=\W)\d+(?=\W)', T_NUMBER),
        ],
        'email': [
            # Email
            (r'[\w\.+-]+\@[\w\.-]+', T_EMAIL),
            default('#pop'),
        ],
        'ip': [
            # IP4
            (r'[\d\.]+', T_IP),
            # IP6
            (r'[\da-fA-F:\.]+', T_IP),
            default('#pop'),
        ],
        'hex': [
            # Hex
            (r'[\da-fA-F:]+', T_HEX),
            default('#pop'),
        ],
        'curly-brace': [
            # Exit condition
            (r'}', Name.Variable, '#pop'),
            # Variable name
            (r'\w+(?:::\w+)?', Name.Variable, 'close-brace'),
            # Whitespace
            (r'\s+', T_SPACE),
            # Catch all
            (r'[^}]+', T_RHS),
        ],
        'close-brace': [
            # Exit condition
            (r'}', Name.Variable, '#pop:2'),
            # Whitespace
            (r'\s+', T_SPACE),
            # Catch all
            (r'[^}]+', T_RHS),
        ],
        'paren': [
            # Exit condition
            (r'\)', Name.Variable, '#pop'),
            # Variable name
            (r'\w+(?:::\w+)?', Name.Variable, 'close-paren'),
            # Whitespace
            (r'\s+', T_SPACE),
            # Catch all
            (r'[^)]+', T_RHS),
        ],
        'close-paren': [
            # Exit condition
            (r'\)', Name.Variable, '#pop:2'),
            # Whitespace
            (r'\s+', T_SPACE),
            # Catch all
            (r'[^)]+', T_RHS),
        ],
        'lhs-default': [
            # Line continuation
            (r'\\(?=\n)', String.Escape),
            # Whitespace
            (r'\s+', T_SPACE),
            # Catch all
            (r'.', T_LHS),
        ],
        'rhs-default': [
            # Line continuation
            (r'\\(?=\n)', String.Escape),
            # Whitespace
            (r'\s+', T_SPACE),
            # Catch all
            (r'.', T_RHS),
        ],
        'root': [
            include('comment'),
            # Section header
            (r'\[.*?\](?=\n)', Keyword),
            # Pragma directive
            (r'(?i)(\.pragma)(?=[\s=\\])([^\S\n]*)(=)([^\S\n]*)',
                bygroups(T_KNOWNDIR, T_SPACE, Operator, T_SPACE), 'pragma'),
            (r'(?i)(\.pragma)(?=[\s\\])([^\S\n]*)',
                bygroups(T_KNOWNDIR, T_SPACE), 'pragma'),
            # Include directive
            (r'(?i)(\.include)(?=[\s=\\])([^\S\n]*)(=)([^\S\n]*)',
                bygroups(T_KNOWNDIR, T_SPACE, Operator, T_SPACE), 'other'),
            (r'(?i)(\.include)(?=[\s\\])([^\S\n]*)',
                bygroups(T_KNOWNDIR, T_SPACE), 'other'),
            # Other directives
            (r'(\.[\w-]+)([^\S\n]*)(=)([^\S\n]*)',
                bygroups(T_OTHERDIR, T_SPACE, Operator, T_SPACE), 'other'),
            (r'(\.[\w-]+)([^\S\n]*)',
                bygroups(T_OTHERDIR, T_SPACE), 'other'),
            # Left hand side
            (r'([\w\.;-]+)(\s*)', bygroups(T_LHS, T_SPACE)),
            # Operator
            (r'(=)([^\S\n]*)', bygroups(Operator, T_SPACE), 'rhs'),
            include('lhs-default'),
        ],
        'rhs': [
            include('comment'),
            # Exit condition
            (r'(?<!\\)\n', T_SPACE, '#pop'),
            # Email
            (r'(?i)(?<=\W)(email)(?=\W)([^\S\n]*)(:)([^\S\n]*)',
                bygroups(T_RHS, T_SPACE, T_RHS, T_SPACE), 'email'),
            # IP
            (r'(?i)(?<=\W)(IP)(?=\W)([^\S\n]*)(:)([^\S\n]*)',
                bygroups(T_RHS, T_SPACE, T_RHS, T_SPACE), 'ip'),
            # DER
            (r'(?i)(?<=\W)(DER)(?=\W)([^\S\n]*)(:)([^\S\n]*)',
                bygroups(T_RHS, T_SPACE, T_RHS, T_SPACE), 'hex'),
            include('string'),
            include('variable'),
            # OID
            (r'(?<=\W)\d+\.(?:\d+\.?)*(?=\W)', Name.Function),
            include('number'),
            # Section reference
            (r'(?<=\W)\@\w+', Name.Constant),
            # Critical keyword
            (r'(?i)(?<=\W)critical(?=\W)', Keyword.Pseudo),
            include('rhs-default'),
        ],
        'pragma': [
            include('comment'),
            # Exit condition
            (r'(?<!\\)\n', T_SPACE, '#pop'),
            # Known directive names
            (r'(?i)(?<=\W)(abspath|dollarid|includedir)(?=\W)([^\S\n]*)(:)([^\S\n]*)',
                bygroups(T_KNOWNNAME, T_SPACE, Operator, T_SPACE), 'value'),
            # Other directive names
            (r'([\w-]+)([^\S\n]*)(:)([^\S\n]*)',
                bygroups(T_OTHERNAME, T_SPACE, T_RHS, T_SPACE), 'value'),
            include('string'),
            include('variable'),
            include('number'),
            include('rhs-default'),
        ],
        'other': [
            include('comment'),
            # Exit condition
            (r'(?<!\\)\n', T_SPACE, '#pop'),
            include('string'),
            include('variable'),
            include('number'),
            include('rhs-default'),
        ],
        'value': [
            include('comment'),
            # Exit condition
            (r'(?<!\\)\n', T_SPACE, '#pop:2'),
            include('string'),
            include('variable'),
            include('number'),
            include('rhs-default'),
        ],
    }

    def __init__(self, **options):
        super(OpenSSLConfLexer, self).__init__(**options)
        # Always apply tokenmerge filter
        self.add_filter('tokenmerge')

    def analyse_text(text):
        npos = text.find('\n')
        if npos < 3:
            return False
        return text[0] == '[' and text[npos-1] == ']'
