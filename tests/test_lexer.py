import unittest
import pygments

from pygments_openssl.lexer import T_SPACE

pygments_version_info = tuple(map(int, pygments.__version__.split('.')))


class LexerTests(unittest.TestCase):

    def lex(self, code, lexer_name):
        from pygments import lex, lexers
        return list(lex(code, lexers.get_lexer_by_name(lexer_name)))

    def test_lex_comment(self):
        from pygments import token

        tokens = self.lex('# Comment\n', 'openssl')
        self.assertEqual(tokens[0], (token.Comment, '# Comment'))
        self.assertEqual(tokens[1], (T_SPACE, '\n'))

        tokens = self.lex('# Comment\n', 'ini')
        self.assertEqual(tokens[0], (token.Comment.Single, '# Comment'))
        self.assertEqual(tokens[1], (T_SPACE, '\n'))

        tokens = self.lex('# Comment\n', 'bash')
        self.assertEqual(tokens[0], (token.Comment.Single, '# Comment\n'))

    def test_lex_section_header(self):
        from pygments import token

        tokens = self.lex('[ default ]\n', 'openssl')
        self.assertEqual(tokens[0], (token.Keyword, '[ default ]'))
        self.assertEqual(tokens[1], (T_SPACE, '\n'))

        tokens = self.lex('[ default ]\n', 'ini')
        self.assertEqual(tokens[0], (token.Keyword, '[ default ]'))
        self.assertEqual(tokens[1], (T_SPACE, '\n'))

    def test_lex_lhs_and_operator(self):
        from pygments import token

        tokens = self.lex('dir = .\n', 'openssl')
        self.assertEqual(tokens[0], (token.Name.Attribute, 'dir'))
        self.assertEqual(tokens[1], (T_SPACE, ' '))
        self.assertEqual(tokens[2], (token.Operator, '='))
        self.assertEqual(tokens[3], (T_SPACE, ' '))

        tokens = self.lex('dir = .\n', 'ini')
        self.assertEqual(tokens[0], (token.Name.Attribute, 'dir'))
        self.assertEqual(tokens[1], (T_SPACE, ' '))
        self.assertEqual(tokens[2], (token.Operator, '='))
        self.assertEqual(tokens[3], (T_SPACE, ' '))

    def test_lex_lhs_line_continuation(self):
        from pygments import token

        tokens = self.lex('dir \\\n = .\n', 'openssl')
        self.assertEqual(tokens[0], (token.Name.Attribute, 'dir'))
        self.assertEqual(tokens[1], (T_SPACE, ' '))
        self.assertEqual(tokens[2], (token.String.Escape, '\\'))
        self.assertEqual(tokens[3], (T_SPACE, '\n '))
        self.assertEqual(tokens[4], (token.Operator, '='))
        self.assertEqual(tokens[5], (T_SPACE, ' '))

    def test_lex_rhs_line_continuation(self):
        from pygments import token

        tokens = self.lex('dir = \\\n.\n', 'openssl')
        self.assertEqual(tokens[0], (token.Name.Attribute, 'dir'))
        self.assertEqual(tokens[1], (T_SPACE, ' '))
        self.assertEqual(tokens[2], (token.Operator, '='))
        self.assertEqual(tokens[3], (T_SPACE, ' '))
        self.assertEqual(tokens[4], (token.String.Escape, '\\'))
        self.assertEqual(tokens[5], (T_SPACE, '\n'))

    def test_lex_rhs_string(self):
        from pygments import token

        tokens = self.lex('dir = .\n', 'openssl')
        self.assertEqual(tokens[0], (token.Name.Attribute, 'dir'))
        self.assertEqual(tokens[1], (T_SPACE, ' '))
        self.assertEqual(tokens[2], (token.Operator, '='))
        self.assertEqual(tokens[3], (T_SPACE, ' '))
        self.assertEqual(tokens[4], (token.String, '.'))
        self.assertEqual(tokens[5], (T_SPACE, '\n'))

        tokens = self.lex('dir = .\n', 'ini')
        self.assertEqual(tokens[0], (token.Name.Attribute, 'dir'))
        self.assertEqual(tokens[1], (T_SPACE, ' '))
        self.assertEqual(tokens[2], (token.Operator, '='))
        self.assertEqual(tokens[3], (T_SPACE, ' '))
        self.assertEqual(tokens[4], (token.String, '.'))
        self.assertEqual(tokens[5], (T_SPACE, '\n'))

    def test_lex_rhs_comment(self):
        from pygments import token

        tokens = self.lex('dir = . # Comment\n', 'openssl')
        self.assertEqual(tokens[0], (token.Name.Attribute, 'dir'))
        self.assertEqual(tokens[1], (T_SPACE, ' '))
        self.assertEqual(tokens[2], (token.Operator, '='))
        self.assertEqual(tokens[3], (T_SPACE, ' '))
        self.assertEqual(tokens[4], (token.String, '.'))
        self.assertEqual(tokens[5], (T_SPACE, ' '))
        self.assertEqual(tokens[6], (token.Comment, '# Comment'))
        self.assertEqual(tokens[7], (T_SPACE, '\n'))

        tokens = self.lex('dir = . # Comment\n', 'ini')
        self.assertEqual(tokens[0], (token.Name.Attribute, 'dir'))
        self.assertEqual(tokens[1], (T_SPACE, ' '))
        self.assertEqual(tokens[2], (token.Operator, '='))
        self.assertEqual(tokens[3], (T_SPACE, ' '))
        if pygments_version_info >= (2, 14, 0):
            self.assertEqual(tokens[4], (token.String, '.'))
            self.assertEqual(tokens[5], (T_SPACE, ' '))
            self.assertEqual(tokens[6], (token.Comment.Single, '# Comment'))
            self.assertEqual(tokens[7], (T_SPACE, '\n'))
        else:
            self.assertEqual(tokens[4], (token.String, '. # Comment'))
            self.assertEqual(tokens[5], (T_SPACE, '\n'))

    def test_lex_rhs_double_quoted_string(self):
        from pygments import token

        tokens = self.lex('dir = "foo bar"\n', 'openssl')
        self.assertEqual(tokens[0], (token.Name.Attribute, 'dir'))
        self.assertEqual(tokens[1], (T_SPACE, ' '))
        self.assertEqual(tokens[2], (token.Operator, '='))
        self.assertEqual(tokens[3], (T_SPACE, ' '))
        self.assertEqual(tokens[4], (token.String.Double, '"foo bar"'))
        self.assertEqual(tokens[5], (T_SPACE, '\n'))

        tokens = self.lex('dir = "foo bar"\n', 'ini')
        self.assertEqual(tokens[0], (token.Name.Attribute, 'dir'))
        self.assertEqual(tokens[1], (T_SPACE, ' '))
        self.assertEqual(tokens[2], (token.Operator, '='))
        self.assertEqual(tokens[3], (T_SPACE, ' '))
        self.assertEqual(tokens[4], (token.String, '"foo bar"'))
        self.assertEqual(tokens[5], (T_SPACE, '\n'))

    def test_lex_rhs_single_quoted_string(self):
        from pygments import token

        tokens = self.lex("dir = 'foo bar'\n", 'openssl')
        self.assertEqual(tokens[0], (token.Name.Attribute, 'dir'))
        self.assertEqual(tokens[1], (T_SPACE, ' '))
        self.assertEqual(tokens[2], (token.Operator, '='))
        self.assertEqual(tokens[3], (T_SPACE, ' '))
        self.assertEqual(tokens[4], (token.String.Single, "'foo bar'"))
        self.assertEqual(tokens[5], (T_SPACE, '\n'))

        tokens = self.lex("dir = 'foo bar'\n", 'ini')
        self.assertEqual(tokens[0], (token.Name.Attribute, 'dir'))
        self.assertEqual(tokens[1], (T_SPACE, ' '))
        self.assertEqual(tokens[2], (token.Operator, '='))
        self.assertEqual(tokens[3], (T_SPACE, ' '))
        self.assertEqual(tokens[4], (token.String, "'foo bar'"))
        self.assertEqual(tokens[5], (T_SPACE, '\n'))

    def test_lex_rhs_variable_name(self):
        from pygments import token

        tokens = self.lex('foo = $variable\n', 'openssl')
        self.assertEqual(tokens[0], (token.Name.Attribute, 'foo'))
        self.assertEqual(tokens[1], (T_SPACE, ' '))
        self.assertEqual(tokens[2], (token.Operator, '='))
        self.assertEqual(tokens[3], (T_SPACE, ' '))
        self.assertEqual(tokens[4], (token.Name.Variable, '$variable'))
        self.assertEqual(tokens[5], (T_SPACE, '\n'))

    def test_lex_rhs_variable_name_curly_braces(self):
        from pygments import token

        tokens = self.lex('foo = ${ENV::variable}\n', 'openssl')
        self.assertEqual(tokens[0], (token.Name.Attribute, 'foo'))
        self.assertEqual(tokens[1], (T_SPACE, ' '))
        self.assertEqual(tokens[2], (token.Operator, '='))
        self.assertEqual(tokens[3], (T_SPACE, ' '))
        self.assertEqual(tokens[4], (token.Name.Variable, '${ENV::variable}'))
        self.assertEqual(tokens[5], (T_SPACE, '\n'))

    def test_lex_rhs_variable_name_parentheses(self):
        from pygments import token

        tokens = self.lex('foo = $(ENV::variable)\n', 'openssl')
        self.assertEqual(tokens[0], (token.Name.Attribute, 'foo'))
        self.assertEqual(tokens[1], (T_SPACE, ' '))
        self.assertEqual(tokens[2], (token.Operator, '='))
        self.assertEqual(tokens[3], (T_SPACE, ' '))
        self.assertEqual(tokens[4], (token.Name.Variable, '$(ENV::variable)'))
        self.assertEqual(tokens[5], (T_SPACE, '\n'))

    def test_lex_rhs_oid(self):
        from pygments import token

        tokens = self.lex('oid = 1.2.3.4.5\n', 'openssl')
        self.assertEqual(tokens[0], (token.Name.Attribute, 'oid'))
        self.assertEqual(tokens[1], (T_SPACE, ' '))
        self.assertEqual(tokens[2], (token.Operator, '='))
        self.assertEqual(tokens[3], (T_SPACE, ' '))
        self.assertEqual(tokens[4], (token.Name.Function, '1.2.3.4.5'))
        self.assertEqual(tokens[5], (T_SPACE, '\n'))

    def test_lex_rhs_number(self):
        from pygments import token

        tokens = self.lex('num = 12\n', 'openssl')
        self.assertEqual(tokens[0], (token.Name.Attribute, 'num'))
        self.assertEqual(tokens[1], (T_SPACE, ' '))
        self.assertEqual(tokens[2], (token.Operator, '='))
        self.assertEqual(tokens[3], (T_SPACE, ' '))
        self.assertEqual(tokens[4], (token.String, '12'))
        self.assertEqual(tokens[5], (T_SPACE, '\n'))

    def test_lex_rhs_section_reference(self):
        from pygments import token

        tokens = self.lex('foo = @section\n', 'openssl')
        self.assertEqual(tokens[0], (token.Name.Attribute, 'foo'))
        self.assertEqual(tokens[1], (T_SPACE, ' '))
        self.assertEqual(tokens[2], (token.Operator, '='))
        self.assertEqual(tokens[3], (T_SPACE, ' '))
        self.assertEqual(tokens[4], (token.Name.Constant, '@section'))
        self.assertEqual(tokens[5], (T_SPACE, '\n'))

    def test_lex_rhs_critical_keyword(self):
        from pygments import token

        tokens = self.lex('foo = critical,bar\n', 'openssl')
        self.assertEqual(tokens[0], (token.Name.Attribute, 'foo'))
        self.assertEqual(tokens[1], (T_SPACE, ' '))
        self.assertEqual(tokens[2], (token.Operator, '='))
        self.assertEqual(tokens[3], (T_SPACE, ' '))
        self.assertEqual(tokens[4], (token.Keyword.Pseudo, 'critical'))
        self.assertEqual(tokens[5], (token.String, ',bar'))
        self.assertEqual(tokens[6], (T_SPACE, '\n'))

    def test_lex_incomplete_lhs(self):
        from pygments import token

        tokens = self.lex('dir\ndir = .\n', 'openssl')
        self.assertEqual(tokens[0], (token.Name.Attribute, 'dir'))
        self.assertEqual(tokens[1], (T_SPACE, '\n'))
        self.assertEqual(tokens[2], (token.Name.Attribute, 'dir'))
        self.assertEqual(tokens[3], (T_SPACE, ' '))
        self.assertEqual(tokens[4], (token.Operator, '='))
        self.assertEqual(tokens[5], (T_SPACE, ' '))
        self.assertEqual(tokens[6], (token.String, '.'))
        self.assertEqual(tokens[7], (T_SPACE, '\n'))

    def test_lex_incomplete_lhs_and_operator(self):
        from pygments import token

        tokens = self.lex('dir =\ndir = .\n', 'openssl')
        self.assertEqual(tokens[0], (token.Name.Attribute, 'dir'))
        self.assertEqual(tokens[1], (T_SPACE, ' '))
        self.assertEqual(tokens[2], (token.Operator, '='))
        self.assertEqual(tokens[3], (T_SPACE, '\n'))
        self.assertEqual(tokens[4], (token.Name.Attribute, 'dir'))
        self.assertEqual(tokens[5], (T_SPACE, ' '))
        self.assertEqual(tokens[6], (token.Operator, '='))
        self.assertEqual(tokens[7], (T_SPACE, ' '))
        self.assertEqual(tokens[8], (token.String, '.'))
        self.assertEqual(tokens[9], (T_SPACE, '\n'))

    def test_lex_incomplete_lhs_string(self):
        from pygments import token

        tokens = self.lex('dir', 'openssl')
        self.assertEqual(tokens[0], (token.Name.Attribute, 'dir'))

    def test_lex_missing_lhs(self):
        from pygments import token

        tokens = self.lex('= foo\ndir = .\n', 'openssl')
        self.assertEqual(tokens[0], (token.Operator, '='))
        self.assertEqual(tokens[1], (T_SPACE, ' '))
        self.assertEqual(tokens[2], (token.String, 'foo'))
        self.assertEqual(tokens[3], (T_SPACE, '\n'))
        self.assertEqual(tokens[4], (token.Name.Attribute, 'dir'))
        self.assertEqual(tokens[5], (T_SPACE, ' '))
        self.assertEqual(tokens[6], (token.Operator, '='))
        self.assertEqual(tokens[7], (T_SPACE, ' '))
        self.assertEqual(tokens[8], (token.String, '.'))
        self.assertEqual(tokens[9], (T_SPACE, '\n'))


class DirectiveLexerTests(unittest.TestCase):

    def lex(self, code, lexer_name):
        from pygments import lex, lexers
        return list(lex(code, lexers.get_lexer_by_name(lexer_name)))

    def test_lex_directive(self):
        from pygments import token

        tokens = self.lex('.directive foo\n', 'openssl')
        self.assertEqual(tokens[0], (token.Name.Attribute, '.directive'))
        self.assertEqual(tokens[1], (T_SPACE, ' '))
        self.assertEqual(tokens[2], (token.String, 'foo'))
        self.assertEqual(tokens[3], (T_SPACE, '\n'))

    def test_lex_directive_and_operator(self):
        from pygments import token

        tokens = self.lex('.directive = foo\n', 'openssl')
        self.assertEqual(tokens[0], (token.Name.Attribute, '.directive'))
        self.assertEqual(tokens[1], (T_SPACE, ' '))
        self.assertEqual(tokens[2], (token.Operator, '='))
        self.assertEqual(tokens[3], (T_SPACE, ' '))
        self.assertEqual(tokens[4], (token.String, 'foo'))
        self.assertEqual(tokens[5], (T_SPACE, '\n'))

    def test_lex_directive_with_leading_whitespace(self):
        from pygments import token

        tokens = self.lex('  .directive foo\n', 'openssl')
        self.assertEqual(tokens[0], (T_SPACE, '  '))
        self.assertEqual(tokens[1], (token.Name.Attribute, '.directive'))
        self.assertEqual(tokens[2], (T_SPACE, ' '))
        self.assertEqual(tokens[3], (token.String, 'foo'))
        self.assertEqual(tokens[4], (T_SPACE, '\n'))

    def test_lex_incomplete_directive(self):
        from pygments import token

        tokens = self.lex('.directive\n', 'openssl')
        self.assertEqual(tokens[0], (token.Name.Attribute, '.directive'))
        self.assertEqual(tokens[1], (T_SPACE, '\n'))

        tokens = self.lex('.directive\n.directive foo\n', 'openssl')
        self.assertEqual(tokens[0], (token.Name.Attribute, '.directive'))
        self.assertEqual(tokens[1], (T_SPACE, '\n'))
        self.assertEqual(tokens[2], (token.Name.Attribute, '.directive'))
        self.assertEqual(tokens[3], (T_SPACE, ' '))
        self.assertEqual(tokens[4], (token.String, 'foo'))
        self.assertEqual(tokens[5], (T_SPACE, '\n'))

    def test_lex_incomplete_directive_and_operator(self):
        from pygments import token

        tokens = self.lex('.directive =\n', 'openssl')
        self.assertEqual(tokens[0], (token.Name.Attribute, '.directive'))
        self.assertEqual(tokens[1], (T_SPACE, ' '))
        self.assertEqual(tokens[2], (token.Operator, '='))
        self.assertEqual(tokens[3], (T_SPACE, '\n'))

        tokens = self.lex('.directive =\n.directive = foo\n', 'openssl')
        self.assertEqual(tokens[0], (token.Name.Attribute, '.directive'))
        self.assertEqual(tokens[1], (T_SPACE, ' '))
        self.assertEqual(tokens[2], (token.Operator, '='))
        self.assertEqual(tokens[3], (T_SPACE, '\n'))
        self.assertEqual(tokens[4], (token.Name.Attribute, '.directive'))
        self.assertEqual(tokens[5], (T_SPACE, ' '))
        self.assertEqual(tokens[6], (token.Operator, '='))
        self.assertEqual(tokens[7], (T_SPACE, ' '))
        self.assertEqual(tokens[8], (token.String, 'foo'))
        self.assertEqual(tokens[9], (T_SPACE, '\n'))

    def test_lex_incomplete_directive_string(self):
        from pygments import token

        tokens = self.lex('.directive', 'openssl')
        self.assertEqual(tokens[0], (token.Name.Attribute, '.directive'))

        tokens = self.lex('.directive\n.directive foo', 'openssl')
        self.assertEqual(tokens[0], (token.Name.Attribute, '.directive'))
        self.assertEqual(tokens[1], (T_SPACE, '\n'))
        self.assertEqual(tokens[2], (token.Name.Attribute, '.directive'))
        self.assertEqual(tokens[3], (T_SPACE, ' '))
        self.assertEqual(tokens[4], (token.String, 'foo'))


class PragmaDirectiveLexerTests(unittest.TestCase):

    def lex(self, code, lexer_name):
        from pygments import lex, lexers
        return list(lex(code, lexers.get_lexer_by_name(lexer_name)))

    def test_lex_pragma_directive(self):
        from pygments import token

        tokens = self.lex('.pragma foo\n', 'openssl')
        self.assertEqual(tokens[0], (token.Name.Builtin, '.pragma'))
        self.assertEqual(tokens[1], (T_SPACE, ' '))
        self.assertEqual(tokens[2], (token.String, 'foo'))
        self.assertEqual(tokens[3], (T_SPACE, '\n'))

    def test_lex_pragma_directive_and_operator(self):
        from pygments import token

        tokens = self.lex('.pragma = foo\n', 'openssl')
        self.assertEqual(tokens[0], (token.Name.Builtin, '.pragma'))
        self.assertEqual(tokens[1], (T_SPACE, ' '))
        self.assertEqual(tokens[2], (token.Operator, '='))
        self.assertEqual(tokens[3], (T_SPACE, ' '))
        self.assertEqual(tokens[4], (token.String, 'foo'))
        self.assertEqual(tokens[5], (T_SPACE, '\n'))

    def test_lex_pragme_directive_with_leading_whitespace(self):
        from pygments import token

        tokens = self.lex('  .pragma foo\n', 'openssl')
        self.assertEqual(tokens[0], (T_SPACE, '  '))
        self.assertEqual(tokens[1], (token.Name.Builtin, '.pragma'))
        self.assertEqual(tokens[2], (T_SPACE, ' '))
        self.assertEqual(tokens[3], (token.String, 'foo'))
        self.assertEqual(tokens[4], (T_SPACE, '\n'))

    def test_lex_pragma_directive_name(self):
        from pygments import token

        tokens = self.lex('.pragma abspath:\n', 'openssl')
        self.assertEqual(tokens[0], (token.Name.Builtin, '.pragma'))
        self.assertEqual(tokens[1], (T_SPACE, ' '))
        self.assertEqual(tokens[2], (token.Keyword.Pseudo, 'abspath'))
        self.assertEqual(tokens[3], (token.Operator, ':'))

    def test_lex_pragma_directive_name_and_operator(self):
        from pygments import token

        tokens = self.lex('.pragma = abspath:\n', 'openssl')
        self.assertEqual(tokens[0], (token.Name.Builtin, '.pragma'))
        self.assertEqual(tokens[1], (T_SPACE, ' '))
        self.assertEqual(tokens[2], (token.Operator, '='))
        self.assertEqual(tokens[3], (T_SPACE, ' '))
        self.assertEqual(tokens[4], (token.Keyword.Pseudo, 'abspath'))
        self.assertEqual(tokens[5], (token.Operator, ':'))

    def test_lex_pragma_directive_name_and_value(self):
        from pygments import token

        tokens = self.lex('.pragma abspath:bar\n', 'openssl')
        self.assertEqual(tokens[0], (token.Name.Builtin, '.pragma'))
        self.assertEqual(tokens[1], (T_SPACE, ' '))
        self.assertEqual(tokens[2], (token.Keyword.Pseudo, 'abspath'))
        self.assertEqual(tokens[3], (token.Operator, ':'))
        self.assertEqual(tokens[4], (token.String, 'bar'))
        self.assertEqual(tokens[5], (T_SPACE, '\n'))

    def test_lex_pragma_directive_name_and_value_with_colon(self):
        from pygments import token

        tokens = self.lex('.pragma abspath:bar:baz\n', 'openssl')
        self.assertEqual(tokens[0], (token.Name.Builtin, '.pragma'))
        self.assertEqual(tokens[1], (T_SPACE, ' '))
        self.assertEqual(tokens[2], (token.Keyword.Pseudo, 'abspath'))
        self.assertEqual(tokens[3], (token.Operator, ':'))
        self.assertEqual(tokens[4], (token.String, 'bar:baz'))
        self.assertEqual(tokens[5], (T_SPACE, '\n'))

    def test_lex_incomplete_pragma_directive(self):
        from pygments import token

        tokens = self.lex('.pragma\n', 'openssl')
        self.assertEqual(tokens[0], (token.Name.Builtin, '.pragma'))
        self.assertEqual(tokens[1], (T_SPACE, '\n'))

        tokens = self.lex('.pragma\n.pragma foo\n', 'openssl')
        self.assertEqual(tokens[0], (token.Name.Builtin, '.pragma'))
        self.assertEqual(tokens[1], (T_SPACE, '\n'))
        self.assertEqual(tokens[2], (token.Name.Builtin, '.pragma'))
        self.assertEqual(tokens[3], (T_SPACE, ' '))
        self.assertEqual(tokens[4], (token.String, 'foo'))
        self.assertEqual(tokens[5], (T_SPACE, '\n'))

    def test_lex_incomplete_pragma_directive_and_operator(self):
        from pygments import token

        tokens = self.lex('.pragma =\n', 'openssl')
        self.assertEqual(tokens[0], (token.Name.Builtin, '.pragma'))
        self.assertEqual(tokens[1], (T_SPACE, ' '))
        self.assertEqual(tokens[2], (token.Operator, '='))
        self.assertEqual(tokens[3], (T_SPACE, '\n'))

        tokens = self.lex('.pragma =\n.pragma = foo\n', 'openssl')
        self.assertEqual(tokens[0], (token.Name.Builtin, '.pragma'))
        self.assertEqual(tokens[1], (T_SPACE, ' '))
        self.assertEqual(tokens[2], (token.Operator, '='))
        self.assertEqual(tokens[3], (T_SPACE, '\n'))
        self.assertEqual(tokens[4], (token.Name.Builtin, '.pragma'))
        self.assertEqual(tokens[5], (T_SPACE, ' '))
        self.assertEqual(tokens[6], (token.Operator, '='))
        self.assertEqual(tokens[7], (T_SPACE, ' '))
        self.assertEqual(tokens[8], (token.String, 'foo'))
        self.assertEqual(tokens[9], (T_SPACE, '\n'))

    def test_lex_incomplete_pragma_directive_string(self):
        from pygments import token

        tokens = self.lex('.pragma', 'openssl')
        self.assertEqual(tokens[0], (token.Name.Builtin, '.pragma'))

        tokens = self.lex('.pragma\n.pragma foo', 'openssl')
        self.assertEqual(tokens[0], (token.Name.Builtin, '.pragma'))
        self.assertEqual(tokens[1], (T_SPACE, '\n'))
        self.assertEqual(tokens[2], (token.Name.Builtin, '.pragma'))
        self.assertEqual(tokens[3], (T_SPACE, ' '))
        self.assertEqual(tokens[4], (token.String, 'foo'))


class IncludeDirectiveLexerTests(unittest.TestCase):

    def lex(self, code, lexer_name):
        from pygments import lex, lexers
        return list(lex(code, lexers.get_lexer_by_name(lexer_name)))

    def test_lex_include_directive(self):
        from pygments import token

        tokens = self.lex('.include foo\n', 'openssl')
        self.assertEqual(tokens[0], (token.Name.Builtin, '.include'))
        self.assertEqual(tokens[1], (T_SPACE, ' '))
        self.assertEqual(tokens[2], (token.String, 'foo'))
        self.assertEqual(tokens[3], (T_SPACE, '\n'))

    def test_lex_include_directive_and_operator(self):
        from pygments import token

        tokens = self.lex('.include = foo\n', 'openssl')
        self.assertEqual(tokens[0], (token.Name.Builtin, '.include'))
        self.assertEqual(tokens[1], (T_SPACE, ' '))
        self.assertEqual(tokens[2], (token.Operator, '='))
        self.assertEqual(tokens[3], (T_SPACE, ' '))
        self.assertEqual(tokens[4], (token.String, 'foo'))
        self.assertEqual(tokens[5], (T_SPACE, '\n'))

    def test_lex_pragme_directive_with_leading_whitespace(self):
        from pygments import token

        tokens = self.lex('  .include foo\n', 'openssl')
        self.assertEqual(tokens[0], (T_SPACE, '  '))
        self.assertEqual(tokens[1], (token.Name.Builtin, '.include'))
        self.assertEqual(tokens[2], (T_SPACE, ' '))
        self.assertEqual(tokens[3], (token.String, 'foo'))
        self.assertEqual(tokens[4], (T_SPACE, '\n'))

    def test_lex_incomplete_include_directive(self):
        from pygments import token

        tokens = self.lex('.include\n', 'openssl')
        self.assertEqual(tokens[0], (token.Name.Builtin, '.include'))
        self.assertEqual(tokens[1], (T_SPACE, '\n'))

        tokens = self.lex('.include\n.include foo\n', 'openssl')
        self.assertEqual(tokens[0], (token.Name.Builtin, '.include'))
        self.assertEqual(tokens[1], (T_SPACE, '\n'))
        self.assertEqual(tokens[2], (token.Name.Builtin, '.include'))
        self.assertEqual(tokens[3], (T_SPACE, ' '))
        self.assertEqual(tokens[4], (token.String, 'foo'))
        self.assertEqual(tokens[5], (T_SPACE, '\n'))

    def test_lex_incomplete_include_directive_and_operator(self):
        from pygments import token

        tokens = self.lex('.include =\n', 'openssl')
        self.assertEqual(tokens[0], (token.Name.Builtin, '.include'))
        self.assertEqual(tokens[1], (T_SPACE, ' '))
        self.assertEqual(tokens[2], (token.Operator, '='))
        self.assertEqual(tokens[3], (T_SPACE, '\n'))

        tokens = self.lex('.include =\n.include = foo\n', 'openssl')
        self.assertEqual(tokens[0], (token.Name.Builtin, '.include'))
        self.assertEqual(tokens[1], (T_SPACE, ' '))
        self.assertEqual(tokens[2], (token.Operator, '='))
        self.assertEqual(tokens[3], (T_SPACE, '\n'))
        self.assertEqual(tokens[4], (token.Name.Builtin, '.include'))
        self.assertEqual(tokens[5], (T_SPACE, ' '))
        self.assertEqual(tokens[6], (token.Operator, '='))
        self.assertEqual(tokens[7], (T_SPACE, ' '))
        self.assertEqual(tokens[8], (token.String, 'foo'))
        self.assertEqual(tokens[9], (T_SPACE, '\n'))

    def test_lex_incomplete_include_directive_string(self):
        from pygments import token

        tokens = self.lex('.include', 'openssl')
        self.assertEqual(tokens[0], (token.Name.Builtin, '.include'))

        tokens = self.lex('.include\n.include foo', 'openssl')
        self.assertEqual(tokens[0], (token.Name.Builtin, '.include'))
        self.assertEqual(tokens[1], (T_SPACE, '\n'))
        self.assertEqual(tokens[2], (token.Name.Builtin, '.include'))
        self.assertEqual(tokens[3], (T_SPACE, ' '))
        self.assertEqual(tokens[4], (token.String, 'foo'))

