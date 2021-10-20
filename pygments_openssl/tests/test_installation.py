import unittest


class InstallationTests(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_has_lexer(self):
        from pygments.lexers import get_lexer_by_name
        get_lexer_by_name('openssl')

    def test_unknown_lexer_raises(self):
        from pygments.lexers import get_lexer_by_name
        from pygments.util import ClassNotFound
        try:
            get_lexer_by_name('does-not-exist')
        except ClassNotFound:
            pass # success
        else:
            self.fail('ClassNotFound not raised')

