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

    def test_lex_rhs_variable_name_parentheses(self):
        from pygments import token

        tokens = self.lex('foo = $(ENV::variable)\n', 'openssl')
        self.assertEqual(tokens[0], (token.Name.Attribute, 'foo'))
        self.assertEqual(tokens[1], (token.Text, ' '))
        self.assertEqual(tokens[2], (token.Operator, '='))
        self.assertEqual(tokens[3], (token.Text, ' '))
        self.assertEqual(tokens[4], (token.Name.Variable, '$('))
        self.assertEqual(tokens[5], (token.Name.Variable, 'ENV::variable'))
        self.assertEqual(tokens[6], (token.Name.Variable, ')'))
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

    def test_lex_incomplete_lhs(self):
        from pygments import token

        tokens = self.lex('dir\ndir = .\n', 'openssl')
        self.assertEqual(tokens[0], (token.Name.Attribute, 'dir'))
        self.assertEqual(tokens[1], (token.Text, '\n'))
        self.assertEqual(tokens[2], (token.Name.Attribute, 'dir'))
        self.assertEqual(tokens[3], (token.Text, ' '))
        self.assertEqual(tokens[4], (token.Operator, '='))
        self.assertEqual(tokens[5], (token.Text, ' '))
        self.assertEqual(tokens[6], (token.String, '.'))
        self.assertEqual(tokens[7], (token.Text, '\n'))

    def test_lex_incomplete_lhs_and_operator(self):
        from pygments import token

        tokens = self.lex('dir =\ndir = .\n', 'openssl')
        self.assertEqual(tokens[0], (token.Name.Attribute, 'dir'))
        self.assertEqual(tokens[1], (token.Text, ' '))
        self.assertEqual(tokens[2], (token.Operator, '='))
        self.assertEqual(tokens[3], (token.Text, '\n'))
        self.assertEqual(tokens[4], (token.Name.Attribute, 'dir'))
        self.assertEqual(tokens[5], (token.Text, ' '))
        self.assertEqual(tokens[6], (token.Operator, '='))
        self.assertEqual(tokens[7], (token.Text, ' '))
        self.assertEqual(tokens[8], (token.String, '.'))
        self.assertEqual(tokens[9], (token.Text, '\n'))

    def test_lex_incomplete_lhs_string(self):
        from pygments import token

        tokens = self.lex('dir', 'openssl')
        self.assertEqual(tokens[0], (token.Name.Attribute, 'dir'))

    def test_lex_missing_lhs(self):
        from pygments import token

        tokens = self.lex('= foo\ndir = .\n', 'openssl')
        self.assertEqual(tokens[0], (token.Operator, '='))
        self.assertEqual(tokens[1], (token.Text, ' '))
        self.assertEqual(tokens[2], (token.String, 'f'))
        self.assertEqual(tokens[3], (token.String, 'o'))
        self.assertEqual(tokens[4], (token.String, 'o'))
        self.assertEqual(tokens[5], (token.Text, '\n'))
        self.assertEqual(tokens[6], (token.Name.Attribute, 'dir'))
        self.assertEqual(tokens[7], (token.Text, ' '))
        self.assertEqual(tokens[8], (token.Operator, '='))
        self.assertEqual(tokens[9], (token.Text, ' '))
        self.assertEqual(tokens[10], (token.String, '.'))
        self.assertEqual(tokens[11], (token.Text, '\n'))


class DirectiveLexerTests(unittest.TestCase):

    def lex(self, code, lexer_name):
        from pygments import lex, lexers
        return list(lex(code, lexers.get_lexer_by_name(lexer_name)))

    def test_lex_directive(self):
        from pygments import token

        tokens = self.lex('.directive foo\n', 'openssl')
        self.assertEqual(tokens[0], (token.Name.Attribute, '.directive'))
        self.assertEqual(tokens[1], (token.Text, ' '))
        self.assertEqual(tokens[2], (token.String, 'f'))
        self.assertEqual(tokens[3], (token.String, 'o'))
        self.assertEqual(tokens[4], (token.String, 'o'))
        self.assertEqual(tokens[5], (token.Text, '\n'))

    def test_lex_directive_and_operator(self):
        from pygments import token

        tokens = self.lex('.directive = foo\n', 'openssl')
        self.assertEqual(tokens[0], (token.Name.Attribute, '.directive'))
        self.assertEqual(tokens[1], (token.Text, ' '))
        self.assertEqual(tokens[2], (token.Operator, '='))
        self.assertEqual(tokens[3], (token.Text, ' '))
        self.assertEqual(tokens[4], (token.String, 'f'))
        self.assertEqual(tokens[5], (token.String, 'o'))
        self.assertEqual(tokens[6], (token.String, 'o'))
        self.assertEqual(tokens[7], (token.Text, '\n'))

    def test_lex_directive_with_leading_whitespace(self):
        from pygments import token

        tokens = self.lex('  .directive foo\n', 'openssl')
        self.assertEqual(tokens[0], (token.Text, '  '))
        self.assertEqual(tokens[1], (token.Name.Attribute, '.directive'))
        self.assertEqual(tokens[2], (token.Text, ' '))
        self.assertEqual(tokens[3], (token.String, 'f'))
        self.assertEqual(tokens[4], (token.String, 'o'))
        self.assertEqual(tokens[5], (token.String, 'o'))
        self.assertEqual(tokens[6], (token.Text, '\n'))

    def test_lex_incomplete_directive(self):
        from pygments import token

        tokens = self.lex('.directive\n', 'openssl')
        self.assertEqual(tokens[0], (token.Name.Attribute, '.directive'))
        self.assertEqual(tokens[1], (token.Text, '\n'))

        tokens = self.lex('.directive\n.directive foo\n', 'openssl')
        self.assertEqual(tokens[0], (token.Name.Attribute, '.directive'))
        self.assertEqual(tokens[1], (token.Text, '\n'))
        self.assertEqual(tokens[2], (token.Name.Attribute, '.directive'))
        self.assertEqual(tokens[3], (token.Text, ' '))
        self.assertEqual(tokens[4], (token.String, 'f'))
        self.assertEqual(tokens[5], (token.String, 'o'))
        self.assertEqual(tokens[6], (token.String, 'o'))
        self.assertEqual(tokens[7], (token.Text, '\n'))

    def test_lex_incomplete_directive_and_operator(self):
        from pygments import token

        tokens = self.lex('.directive =\n', 'openssl')
        self.assertEqual(tokens[0], (token.Name.Attribute, '.directive'))
        self.assertEqual(tokens[1], (token.Text, ' '))
        self.assertEqual(tokens[2], (token.Operator, '='))
        self.assertEqual(tokens[3], (token.Text, '\n'))

        tokens = self.lex('.directive =\n.directive = foo\n', 'openssl')
        self.assertEqual(tokens[0], (token.Name.Attribute, '.directive'))
        self.assertEqual(tokens[1], (token.Text, ' '))
        self.assertEqual(tokens[2], (token.Operator, '='))
        self.assertEqual(tokens[3], (token.Text, '\n'))
        self.assertEqual(tokens[4], (token.Name.Attribute, '.directive'))
        self.assertEqual(tokens[5], (token.Text, ' '))
        self.assertEqual(tokens[6], (token.Operator, '='))
        self.assertEqual(tokens[7], (token.Text, ' '))
        self.assertEqual(tokens[8], (token.String, 'f'))
        self.assertEqual(tokens[9], (token.String, 'o'))
        self.assertEqual(tokens[10], (token.String, 'o'))
        self.assertEqual(tokens[11], (token.Text, '\n'))

    def test_lex_incomplete_directive_string(self):
        from pygments import token

        tokens = self.lex('.directive', 'openssl')
        self.assertEqual(tokens[0], (token.Name.Attribute, '.directive'))

        tokens = self.lex('.directive\n.directive foo', 'openssl')
        self.assertEqual(tokens[0], (token.Name.Attribute, '.directive'))
        self.assertEqual(tokens[1], (token.Text, '\n'))
        self.assertEqual(tokens[2], (token.Name.Attribute, '.directive'))
        self.assertEqual(tokens[3], (token.Text, ' '))
        self.assertEqual(tokens[4], (token.String, 'f'))
        self.assertEqual(tokens[5], (token.String, 'o'))
        self.assertEqual(tokens[6], (token.String, 'o'))


class PragmaDirectiveLexerTests(unittest.TestCase):

    def lex(self, code, lexer_name):
        from pygments import lex, lexers
        return list(lex(code, lexers.get_lexer_by_name(lexer_name)))

    def test_lex_pragma_directive(self):
        from pygments import token

        tokens = self.lex('.pragma foo\n', 'openssl')
        self.assertEqual(tokens[0], (token.Name.Attribute, '.pragma'))
        self.assertEqual(tokens[1], (token.Text, ' '))
        self.assertEqual(tokens[2], (token.String, 'f'))
        self.assertEqual(tokens[3], (token.String, 'o'))
        self.assertEqual(tokens[4], (token.String, 'o'))
        self.assertEqual(tokens[5], (token.Text, '\n'))

    def test_lex_pragma_directive_and_operator(self):
        from pygments import token

        tokens = self.lex('.pragma = foo\n', 'openssl')
        self.assertEqual(tokens[0], (token.Name.Attribute, '.pragma'))
        self.assertEqual(tokens[1], (token.Text, ' '))
        self.assertEqual(tokens[2], (token.Operator, '='))
        self.assertEqual(tokens[3], (token.Text, ' '))
        self.assertEqual(tokens[4], (token.String, 'f'))
        self.assertEqual(tokens[5], (token.String, 'o'))
        self.assertEqual(tokens[6], (token.String, 'o'))
        self.assertEqual(tokens[7], (token.Text, '\n'))

    def test_lex_pragme_directive_with_leading_whitespace(self):
        from pygments import token

        tokens = self.lex('  .pragma foo\n', 'openssl')
        self.assertEqual(tokens[0], (token.Text, '  '))
        self.assertEqual(tokens[1], (token.Name.Attribute, '.pragma'))
        self.assertEqual(tokens[2], (token.Text, ' '))
        self.assertEqual(tokens[3], (token.String, 'f'))
        self.assertEqual(tokens[4], (token.String, 'o'))
        self.assertEqual(tokens[5], (token.String, 'o'))
        self.assertEqual(tokens[6], (token.Text, '\n'))

    def test_lex_pragma_directive_name(self):
        from pygments import token

        tokens = self.lex('.pragma foo:\n', 'openssl')
        self.assertEqual(tokens[0], (token.Name.Attribute, '.pragma'))
        self.assertEqual(tokens[1], (token.Text, ' '))
        self.assertEqual(tokens[2], (token.Keyword.Pseudo, 'foo'))
        self.assertEqual(tokens[3], (token.Operator, ':'))

    def test_lex_pragma_directive_name_and_operator(self):
        from pygments import token

        tokens = self.lex('.pragma = foo:\n', 'openssl')
        self.assertEqual(tokens[0], (token.Name.Attribute, '.pragma'))
        self.assertEqual(tokens[1], (token.Text, ' '))
        self.assertEqual(tokens[2], (token.Operator, '='))
        self.assertEqual(tokens[3], (token.Text, ' '))
        self.assertEqual(tokens[4], (token.Keyword.Pseudo, 'foo'))
        self.assertEqual(tokens[5], (token.Operator, ':'))

    def test_lex_pragma_directive_name_and_value(self):
        from pygments import token

        tokens = self.lex('.pragma foo:bar\n', 'openssl')
        self.assertEqual(tokens[0], (token.Name.Attribute, '.pragma'))
        self.assertEqual(tokens[1], (token.Text, ' '))
        self.assertEqual(tokens[2], (token.Keyword.Pseudo, 'foo'))
        self.assertEqual(tokens[3], (token.Operator, ':'))
        self.assertEqual(tokens[4], (token.String, 'b'))
        self.assertEqual(tokens[5], (token.String, 'a'))
        self.assertEqual(tokens[6], (token.String, 'r'))
        self.assertEqual(tokens[7], (token.Text, '\n'))

    def test_lex_pragma_directive_name_and_value_with_colon(self):
        from pygments import token

        tokens = self.lex('.pragma foo:bar:baz\n', 'openssl')
        self.assertEqual(tokens[0], (token.Name.Attribute, '.pragma'))
        self.assertEqual(tokens[1], (token.Text, ' '))
        self.assertEqual(tokens[2], (token.Keyword.Pseudo, 'foo'))
        self.assertEqual(tokens[3], (token.Operator, ':'))
        self.assertEqual(tokens[4], (token.String, 'b'))
        self.assertEqual(tokens[5], (token.String, 'a'))
        self.assertEqual(tokens[6], (token.String, 'r'))
        self.assertEqual(tokens[7], (token.String, ':'))
        self.assertEqual(tokens[8], (token.String, 'b'))
        self.assertEqual(tokens[9], (token.String, 'a'))
        self.assertEqual(tokens[10], (token.String, 'z'))
        self.assertEqual(tokens[11], (token.Text, '\n'))

    def test_lex_incomplete_pragma_directive(self):
        from pygments import token

        tokens = self.lex('.pragma\n', 'openssl')
        self.assertEqual(tokens[0], (token.Name.Attribute, '.pragma'))
        self.assertEqual(tokens[1], (token.Text, '\n'))

        tokens = self.lex('.pragma\n.pragma foo\n', 'openssl')
        self.assertEqual(tokens[0], (token.Name.Attribute, '.pragma'))
        self.assertEqual(tokens[1], (token.Text, '\n'))
        self.assertEqual(tokens[2], (token.Name.Attribute, '.pragma'))
        self.assertEqual(tokens[3], (token.Text, ' '))
        self.assertEqual(tokens[4], (token.String, 'f'))
        self.assertEqual(tokens[5], (token.String, 'o'))
        self.assertEqual(tokens[6], (token.String, 'o'))
        self.assertEqual(tokens[7], (token.Text, '\n'))

    def test_lex_incomplete_pragma_directive_and_operator(self):
        from pygments import token

        tokens = self.lex('.pragma =\n', 'openssl')
        self.assertEqual(tokens[0], (token.Name.Attribute, '.pragma'))
        self.assertEqual(tokens[1], (token.Text, ' '))
        self.assertEqual(tokens[2], (token.Operator, '='))
        self.assertEqual(tokens[3], (token.Text, '\n'))

        tokens = self.lex('.pragma =\n.pragma = foo\n', 'openssl')
        self.assertEqual(tokens[0], (token.Name.Attribute, '.pragma'))
        self.assertEqual(tokens[1], (token.Text, ' '))
        self.assertEqual(tokens[2], (token.Operator, '='))
        self.assertEqual(tokens[3], (token.Text, '\n'))
        self.assertEqual(tokens[4], (token.Name.Attribute, '.pragma'))
        self.assertEqual(tokens[5], (token.Text, ' '))
        self.assertEqual(tokens[6], (token.Operator, '='))
        self.assertEqual(tokens[7], (token.Text, ' '))
        self.assertEqual(tokens[8], (token.String, 'f'))
        self.assertEqual(tokens[9], (token.String, 'o'))
        self.assertEqual(tokens[10], (token.String, 'o'))
        self.assertEqual(tokens[11], (token.Text, '\n'))

    def test_lex_incomplete_pragma_directive_string(self):
        from pygments import token

        tokens = self.lex('.pragma', 'openssl')
        self.assertEqual(tokens[0], (token.Name.Attribute, '.pragma'))

        tokens = self.lex('.pragma\n.pragma foo', 'openssl')
        self.assertEqual(tokens[0], (token.Name.Attribute, '.pragma'))
        self.assertEqual(tokens[1], (token.Text, '\n'))
        self.assertEqual(tokens[2], (token.Name.Attribute, '.pragma'))
        self.assertEqual(tokens[3], (token.Text, ' '))
        self.assertEqual(tokens[4], (token.String, 'f'))
        self.assertEqual(tokens[5], (token.String, 'o'))
        self.assertEqual(tokens[6], (token.String, 'o'))

