import unittest


class LexerTests(unittest.TestCase):

    def lex(self, code, lexer_name):
        from pygments import lex, lexers
        return list(lex(code, lexers.get_lexer_by_name(lexer_name)))

    def test_lex_comment(self):
        from pygments import token

        tokens = self.lex('# Comment\n', 'openssl')
        self.assertEqual(tokens[0], (token.Comment, '# Comment'))
        self.assertEqual(tokens[1], (token.Text, '\n'))

        tokens = self.lex('# Comment\n', 'ini')
        self.assertEqual(tokens[0], (token.Comment.Single, '# Comment'))
        self.assertEqual(tokens[1], (token.Text, '\n'))

        tokens = self.lex('# Comment\n', 'bash')
        self.assertEqual(tokens[0], (token.Comment.Single, '# Comment\n'))

    def test_lex_section_header(self):
        from pygments import token

        tokens = self.lex('[ default ]\n', 'openssl')
        self.assertEqual(tokens[0], (token.Keyword, '[ default ]'))
        self.assertEqual(tokens[1], (token.Text, '\n'))

        tokens = self.lex('[ default ]\n', 'ini')
        self.assertEqual(tokens[0], (token.Keyword, '[ default ]'))
        self.assertEqual(tokens[1], (token.Text, '\n'))

    def test_lex_lhs_and_operator(self):
        from pygments import token

        tokens = self.lex('dir = .\n', 'openssl')
        self.assertEqual(tokens[0], (token.Name.Attribute, 'dir'))
        self.assertEqual(tokens[1], (token.Text, ' '))
        self.assertEqual(tokens[2], (token.Operator, '='))
        self.assertEqual(tokens[3], (token.Text, ' '))

        tokens = self.lex('dir = .\n', 'ini')
        self.assertEqual(tokens[0], (token.Name.Attribute, 'dir'))
        self.assertEqual(tokens[1], (token.Text, ' '))
        self.assertEqual(tokens[2], (token.Operator, '='))
        self.assertEqual(tokens[3], (token.Text, ' '))

    def test_lex_lhs_line_continuation(self):
        from pygments import token

        tokens = self.lex('dir \\\n = .\n', 'openssl')
        self.assertEqual(tokens[0], (token.Name.Attribute, 'dir'))
        self.assertEqual(tokens[1], (token.Text, ' '))
        self.assertEqual(tokens[2], (token.String.Escape, '\\'))
        self.assertEqual(tokens[3], (token.Text, '\n '))
        self.assertEqual(tokens[4], (token.Operator, '='))
        self.assertEqual(tokens[5], (token.Text, ' '))

    def test_lex_rhs_line_continuation(self):
        from pygments import token

        tokens = self.lex('dir = \\\n.\n', 'openssl')
        self.assertEqual(tokens[0], (token.Name.Attribute, 'dir'))
        self.assertEqual(tokens[1], (token.Text, ' '))
        self.assertEqual(tokens[2], (token.Operator, '='))
        self.assertEqual(tokens[3], (token.Text, ' '))
        self.assertEqual(tokens[4], (token.String.Escape, '\\'))
        self.assertEqual(tokens[5], (token.Text, '\n'))

    def test_lex_rhs_string(self):
        from pygments import token

        tokens = self.lex('dir = .\n', 'openssl')
        self.assertEqual(tokens[0], (token.Name.Attribute, 'dir'))
        self.assertEqual(tokens[1], (token.Text, ' '))
        self.assertEqual(tokens[2], (token.Operator, '='))
        self.assertEqual(tokens[3], (token.Text, ' '))
        self.assertEqual(tokens[4], (token.String, '.'))
        self.assertEqual(tokens[5], (token.Text, '\n'))

        tokens = self.lex('dir = .\n', 'ini')
        self.assertEqual(tokens[0], (token.Name.Attribute, 'dir'))
        self.assertEqual(tokens[1], (token.Text, ' '))
        self.assertEqual(tokens[2], (token.Operator, '='))
        self.assertEqual(tokens[3], (token.Text, ' '))
        self.assertEqual(tokens[4], (token.String, '.'))
        self.assertEqual(tokens[5], (token.Text, '\n'))

    def test_lex_rhs_comment(self):
        from pygments import token

        tokens = self.lex('dir = . # Comment\n', 'openssl')
        self.assertEqual(tokens[0], (token.Name.Attribute, 'dir'))
        self.assertEqual(tokens[1], (token.Text, ' '))
        self.assertEqual(tokens[2], (token.Operator, '='))
        self.assertEqual(tokens[3], (token.Text, ' '))
        self.assertEqual(tokens[4], (token.String, '.'))
        self.assertEqual(tokens[5], (token.Text, ' '))
        self.assertEqual(tokens[6], (token.Comment, '# Comment'))
        self.assertEqual(tokens[7], (token.Text, '\n'))

        tokens = self.lex('dir = . # Comment\n', 'ini')
        self.assertEqual(tokens[0], (token.Name.Attribute, 'dir'))
        self.assertEqual(tokens[1], (token.Text, ' '))
        self.assertEqual(tokens[2], (token.Operator, '='))
        self.assertEqual(tokens[3], (token.Text, ' '))
        self.assertEqual(tokens[4], (token.String, '. # Comment'))
        self.assertEqual(tokens[5], (token.Text, '\n'))

    def test_lex_rhs_double_quoted_string(self):
        from pygments import token

        tokens = self.lex('dir = "foo bar"\n', 'openssl')
        self.assertEqual(tokens[0], (token.Name.Attribute, 'dir'))
        self.assertEqual(tokens[1], (token.Text, ' '))
        self.assertEqual(tokens[2], (token.Operator, '='))
        self.assertEqual(tokens[3], (token.Text, ' '))
        self.assertEqual(tokens[4], (token.String.Double, '"foo bar"'))
        self.assertEqual(tokens[5], (token.Text, '\n'))

        tokens = self.lex('dir = "foo bar"\n', 'ini')
        self.assertEqual(tokens[0], (token.Name.Attribute, 'dir'))
        self.assertEqual(tokens[1], (token.Text, ' '))
        self.assertEqual(tokens[2], (token.Operator, '='))
        self.assertEqual(tokens[3], (token.Text, ' '))
        self.assertEqual(tokens[4], (token.String, '"foo bar"'))
        self.assertEqual(tokens[5], (token.Text, '\n'))

    def test_lex_rhs_single_quoted_string(self):
        from pygments import token

        tokens = self.lex("dir = 'foo bar'\n", 'openssl')
        self.assertEqual(tokens[0], (token.Name.Attribute, 'dir'))
        self.assertEqual(tokens[1], (token.Text, ' '))
        self.assertEqual(tokens[2], (token.Operator, '='))
        self.assertEqual(tokens[3], (token.Text, ' '))
        self.assertEqual(tokens[4], (token.String.Single, "'foo bar'"))
        self.assertEqual(tokens[5], (token.Text, '\n'))

        tokens = self.lex("dir = 'foo bar'\n", 'ini')
        self.assertEqual(tokens[0], (token.Name.Attribute, 'dir'))
        self.assertEqual(tokens[1], (token.Text, ' '))
        self.assertEqual(tokens[2], (token.Operator, '='))
        self.assertEqual(tokens[3], (token.Text, ' '))
        self.assertEqual(tokens[4], (token.String, "'foo bar'"))
        self.assertEqual(tokens[5], (token.Text, '\n'))

    def test_lex_rhs_variable_name(self):
        from pygments import token

        tokens = self.lex('foo = $variable\n', 'openssl')
        self.assertEqual(tokens[0], (token.Name.Attribute, 'foo'))
        self.assertEqual(tokens[1], (token.Text, ' '))
        self.assertEqual(tokens[2], (token.Operator, '='))
        self.assertEqual(tokens[3], (token.Text, ' '))
        self.assertEqual(tokens[4], (token.Name.Variable, '$variable'))
        self.assertEqual(tokens[5], (token.Text, '\n'))

    def test_lex_rhs_variable_name_curly_braces(self):
        from pygments import token

        tokens = self.lex('foo = ${ENV::variable}\n', 'openssl')
        self.assertEqual(tokens[0], (token.Name.Attribute, 'foo'))
        self.assertEqual(tokens[1], (token.Text, ' '))
        self.assertEqual(tokens[2], (token.Operator, '='))
        self.assertEqual(tokens[3], (token.Text, ' '))
        self.assertEqual(tokens[4], (token.Name.Variable, '${'))
        self.assertEqual(tokens[5], (token.Name.Variable, 'ENV::variable'))
        self.assertEqual(tokens[6], (token.Name.Variable, '}'))
        self.assertEqual(tokens[7], (token.Text, '\n'))

    def test_lex_rhs_oid(self):
        from pygments import token

        tokens = self.lex('oid = 1.2.3.4.5\n', 'openssl')
        self.assertEqual(tokens[0], (token.Name.Attribute, 'oid'))
        self.assertEqual(tokens[1], (token.Text, ' '))
        self.assertEqual(tokens[2], (token.Operator, '='))
        self.assertEqual(tokens[3], (token.Text, ' '))
        self.assertEqual(tokens[4], (token.Name.Function, '1.2.3.4.5'))
        self.assertEqual(tokens[5], (token.Text, '\n'))

    def test_lex_rhs_number(self):
        from pygments import token

        tokens = self.lex('num = 12\n', 'openssl')
        self.assertEqual(tokens[0], (token.Name.Attribute, 'num'))
        self.assertEqual(tokens[1], (token.Text, ' '))
        self.assertEqual(tokens[2], (token.Operator, '='))
        self.assertEqual(tokens[3], (token.Text, ' '))
        self.assertEqual(tokens[4], (token.String, '12'))
        self.assertEqual(tokens[5], (token.Text, '\n'))

    def test_lex_rhs_section_reference(self):
        from pygments import token

        tokens = self.lex('foo = @section\n', 'openssl')
        self.assertEqual(tokens[0], (token.Name.Attribute, 'foo'))
        self.assertEqual(tokens[1], (token.Text, ' '))
        self.assertEqual(tokens[2], (token.Operator, '='))
        self.assertEqual(tokens[3], (token.Text, ' '))
        self.assertEqual(tokens[4], (token.Name.Constant, '@section'))
        self.assertEqual(tokens[5], (token.Text, '\n'))

    def test_lex_rhs_critical_keyword(self):
        from pygments import token

        tokens = self.lex('foo = critical,bar\n', 'openssl')
        self.assertEqual(tokens[0], (token.Name.Attribute, 'foo'))
        self.assertEqual(tokens[1], (token.Text, ' '))
        self.assertEqual(tokens[2], (token.Operator, '='))
        self.assertEqual(tokens[3], (token.Text, ' '))
        self.assertEqual(tokens[4], (token.Keyword.Pseudo, 'critical'))
        self.assertEqual(tokens[5], (token.String, ','))
        self.assertEqual(tokens[6], (token.String, 'b'))
        self.assertEqual(tokens[7], (token.String, 'a'))
        self.assertEqual(tokens[8], (token.String, 'r'))
        self.assertEqual(tokens[9], (token.Text, '\n'))

