import tokenize
from operator import itemgetter

from nose.tools import assert_equal
import pep8

import fixes


# hack to generate tokens
# TODO: See if there is a better way to do this
def iden(x):
    yield x


class Pep8FixTester(object):
    _oracle = None  # pep8 checker

    def oracle(self, line, *args):
        return getattr(pep8, self._oracle)(line, *args)

    def tokenize(self, line):
        return tokenize.generate_tokens(iden(line).next)

    def fix(self, line, *args):
        for location, msg in self.oracle(line, *args):
            try:
                _, cursor = location
            except TypeError:
                cursor = location
            code, _ = msg.split(None, 1)
            print location, msg

            line = getattr(fixes, code.lower())(line, cursor)

        return line

    def ask(self, line, *args):
        fixed = self.fix(line, *args)

        print '-%s\n+%s' % (line, fixed)
        assert_equal(list(self.oracle(fixed, *args)), [])


class Pep8PhysicalLineFixTester(Pep8FixTester):
    """
    Tester for a physical line oracle (which only returns a single result, rather
    than a generator)
    """
    def oracle(self, line, *args):
        result = super(Pep8PhysicalLineFixTester, self).oracle(line, *args)
        if result is None:
            return []
        else:
            return [result]


class TestExtraneousWhitespace(Pep8FixTester):
    _oracle = 'extraneous_whitespace'

    def test_e201(self):
        yield self.ask, 'spam( ham[1], {eggs: 2})'
        yield self.ask, 'spam(ham[ 1], {eggs: 2})'
        yield self.ask, 'spam(ham[1], { eggs: 2})'

    def test_e202(self):
        yield self.ask, 'spam(ham[1], {eggs: 2} )'
        yield self.ask, 'spam(ham[1 ], {eggs: 2})'
        yield self.ask, 'spam(ham[1], {eggs: 2 })'

    def test_e203(self):
        yield self.ask, 'if x == 4: print x, y; x, y = y , x'
        yield self.ask, 'if x == 4: print x, y ; x, y = y, x'
        yield self.ask, 'if x == 4 : print x, y; x, y = y, x'


class TestMissingWhitespaceAroundOperator(Pep8FixTester):
    _oracle = 'missing_whitespace_around_operator'

    def check_tokenized_expr(self, line, *args):
        compare = itemgetter(0, 1)
        assert_equal(
            [compare(token) for token in self.tokenize(line)],
            [compare(token) for token in self.tokenize(self.fix(line, *args))]
        )

    def test_e225(self):
        for op in pep8.WS_NEEDED_OPERATORS:
            line = "1%s2" % op
            yield self.ask, line, self.tokenize(line)
            yield self.check_tokenized_expr, line, self.tokenize(line)
            line = "1 %s2" % op
            yield self.ask, line, self.tokenize(line)
            yield self.check_tokenized_expr, line, self.tokenize(line)
            line = "1%s 2" % op
            yield self.ask, line, self.tokenize(line)
            yield self.check_tokenized_expr, line, self.tokenize(line)
        lines = [
                'i=i+1',
                'submitted +=1',
                'x = x*2 - 1',
                'hypot2 = x*x + y*y',
                'c = alpha -4',
                'z = x **y',
                'x =foo(bar)',
                'x= foo(bar)',
                ]
        for line in lines:
            yield self.ask, line, self.tokenize(line)
            yield self.check_tokenized_expr, line, self.tokenize(line)


class TestMissingWhitespace(Pep8FixTester):
    _oracle = 'missing_whitespace'

    def test_e231(self):
        yield self.ask, "['a','b']"
        yield self.ask, "foo(bar,baz)"
        yield self.ask, "{foo:bar}"


class TestWhiteSpaceBeforeInlineComment(Pep8FixTester):
    _oracle = 'whitespace_before_inline_comment'

    def test_e261(self):
        lines = [
            "x = x + 1 # Increment x",
            "x = x + 1 #Increment x",
        ]
        for line in lines:
            yield self.ask, line, self.tokenize(line)

    def test_262(self):
        lines = ["x = x + 1  #Increment x", "x = x + 1  #  Increment x"]
        for line in lines:
            yield self.ask, line, self.tokenize(line)


class TestBlankLines(Pep8FixTester):
    _oracle = 'blank_lines'


class TestTabsObsolete(Pep8PhysicalLineFixTester):
    _oracle = 'tabs_obsolete'


class TestTrailingWhitespace(Pep8PhysicalLineFixTester):
    _oracle = 'trailing_whitespace'

    def test_w291(self):
        yield self.ask, "a = 1 \n"

    def test_w293(self):
        yield self.ask, " \n"
