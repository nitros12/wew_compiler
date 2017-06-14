#!/usr/bin/env python
# -*- coding: utf-8 -*-

# CAVEAT UTILITOR
#
# This file was automatically generated by TatSu.
#
#    https://pypi.python.org/pypi/tatsu/
#
# Any changes you make to it will be overwritten the next time
# the file is generated.


from __future__ import print_function, division, absolute_import, unicode_literals

from tatsu.buffering import Buffer
from tatsu.parsing import Parser
from tatsu.parsing import tatsumasu
from tatsu.util import re, generic_main  # noqa


KEYWORDS = {}


class testBuffer(Buffer):
    def __init__(
        self,
        text,
        whitespace=None,
        nameguard=None,
        comments_re=None,
        eol_comments_re=None,
        ignorecase=None,
        namechars='',
        **kwargs
    ):
        super(testBuffer, self).__init__(
            text,
            whitespace=whitespace,
            nameguard=nameguard,
            comments_re=comments_re,
            eol_comments_re=eol_comments_re,
            ignorecase=ignorecase,
            namechars=namechars,
            **kwargs
        )


class testParser(Parser):
    def __init__(
        self,
        whitespace=None,
        nameguard=None,
        comments_re=None,
        eol_comments_re=None,
        ignorecase=None,
        left_recursion=True,
        parseinfo=False,
        keywords=None,
        namechars='',
        buffer_class=testBuffer,
        **kwargs
    ):
        if keywords is None:
            keywords = KEYWORDS
        super(testParser, self).__init__(
            whitespace=whitespace,
            nameguard=nameguard,
            comments_re=comments_re,
            eol_comments_re=eol_comments_re,
            ignorecase=ignorecase,
            left_recursion=left_recursion,
            parseinfo=parseinfo,
            keywords=keywords,
            namechars=namechars,
            buffer_class=buffer_class,
            **kwargs
        )

    @tatsumasu()
    def _start_(self):  # noqa
        self._expression_()
        self._check_eof()

    @tatsumasu()
    def _expression_(self):  # noqa
        self._assign_expression_()

    @tatsumasu()
    def _assign_expression_(self):  # noqa
        with self._choice():
            with self._option():

                def sep0():
                    self._token(':=')

                def block0():
                    self._lor_expression_()
                self._right_join(block0, sep0)
            with self._option():
                self._lor_expression_()
            self._error('no available options')

    @tatsumasu()
    def _lor_expression_(self):  # noqa
        with self._choice():
            with self._option():

                def sep0():
                    self._token('||')

                def block0():
                    self._land_expression_()
                self._right_join(block0, sep0)
            with self._option():
                self._land_expression_()
            self._error('no available options')

    @tatsumasu()
    def _land_expression_(self):  # noqa
        with self._choice():
            with self._option():

                def sep0():
                    self._token('&&')

                def block0():
                    self._or_expression_()
                self._right_join(block0, sep0)
            with self._option():
                self._or_expression_()
            self._error('no available options')

    @tatsumasu()
    def _or_expression_(self):  # noqa
        with self._choice():
            with self._option():

                def sep0():
                    self._token('|')

                def block0():
                    self._xor_expression_()
                self._right_join(block0, sep0)
            with self._option():
                self._xor_expression_()
            self._error('no available options')

    @tatsumasu()
    def _xor_expression_(self):  # noqa
        with self._choice():
            with self._option():

                def sep0():
                    self._token('^')

                def block0():
                    self._and_expression_()
                self._right_join(block0, sep0)
            with self._option():
                self._and_expression_()
            self._error('no available options')

    @tatsumasu()
    def _and_expression_(self):  # noqa
        with self._choice():
            with self._option():

                def sep0():
                    self._token('&')

                def block0():
                    self._equality_expression_()
                self._right_join(block0, sep0)
            with self._option():
                self._equality_expression_()
            self._error('no available options')

    @tatsumasu()
    def _equality_expression_(self):  # noqa
        with self._choice():
            with self._option():

                def sep0():
                    with self._group():
                        with self._choice():
                            with self._option():
                                self._token('==')
                            with self._option():
                                self._token('!=')
                            self._error('expecting one of: != ==')

                def block0():
                    self._relative_expression_()
                self._right_join(block0, sep0)
            with self._option():
                self._relative_expression_()
            self._error('no available options')

    @tatsumasu()
    def _relative_expression_(self):  # noqa
        with self._choice():
            with self._option():

                def sep0():
                    with self._group():
                        with self._choice():
                            with self._option():
                                self._token('>')
                            with self._option():
                                self._token('<')
                            with self._option():
                                self._token('>=')
                            with self._option():
                                self._token('<=')
                            self._error('expecting one of: < <= > >=')

                def block0():
                    self._shift_expression_()
                self._right_join(block0, sep0)
            with self._option():
                self._shift_expression_()
            self._error('no available options')

    @tatsumasu()
    def _shift_expression_(self):  # noqa
        with self._choice():
            with self._option():

                def sep0():
                    with self._group():
                        with self._choice():
                            with self._option():
                                self._token('<<')
                            with self._option():
                                self._token('>>')
                            self._error('expecting one of: << >>')

                def block0():
                    self._add_expression_()
                self._right_join(block0, sep0)
            with self._option():
                self._add_expression_()
            self._error('no available options')

    @tatsumasu()
    def _add_expression_(self):  # noqa
        with self._choice():
            with self._option():

                def sep0():
                    with self._group():
                        with self._choice():
                            with self._option():
                                self._token('+')
                            with self._option():
                                self._token('-')
                            self._error('expecting one of: + -')

                def block0():
                    self._mult_expression_()
                self._right_join(block0, sep0)
            with self._option():
                self._mult_expression_()
            self._error('no available options')

    @tatsumasu()
    def _mult_expression_(self):  # noqa
        with self._choice():
            with self._option():

                def sep0():
                    with self._group():
                        with self._choice():
                            with self._option():
                                self._token('/')
                            with self._option():
                                self._token('*')
                            self._error('expecting one of: * /')

                def block0():
                    self._unary_expression_()
                self._right_join(block0, sep0)
            with self._option():
                self._unary_expression_()
            self._error('no available options')

    @tatsumasu()
    def _unary_expression_(self):  # noqa
        with self._choice():
            with self._option():
                with self._group():
                    with self._choice():
                        with self._option():
                            self._token('*')
                        with self._option():
                            self._token('-')
                        with self._option():
                            self._token('+')
                        with self._option():
                            self._token('~')
                        with self._option():
                            self._token('!')
                        with self._option():
                            self._token('--')
                        with self._option():
                            self._token('++')
                        self._error('expecting one of: ! * + ++ - -- ~')
                self._unary_expression_()
            with self._option():
                self._postfix_expression_()
            self._error('no available options')

    @tatsumasu()
    def _postfix_expression_(self):  # noqa
        with self._choice():
            with self._option():
                self._postfix_expression_()
                self._token('[')
                self._expression_()
                self._token(']')
            with self._option():
                self._postfix_expression_()
                self._token('++')
            with self._option():
                self._postfix_expression_()
                self._token('--')
            with self._option():
                self._function_expression_()
            self._error('no available options')

    @tatsumasu()
    def _function_expression_(self):  # noqa
        with self._choice():
            with self._option():
                self._function_expression_()
                self._token('(')

                def sep0():
                    self._token(',')

                def block0():
                    self._expression_()
                self._gather(block0, sep0)
                self._token(')')
            with self._option():
                self._primary_expression_()
            self._error('no available options')

    @tatsumasu()
    def _primary_expression_(self):  # noqa
        with self._choice():
            with self._option():
                self._identifier_()
            with self._option():
                self._literal_()
            with self._option():
                self._token('(')
                self._cut()
                self._expression_()
                self.name_last_node('@')
                self._token(')')
            self._error('no available options')

    @tatsumasu()
    def _integer_(self):  # noqa
        self._pattern(r'\d+')

    @tatsumasu()
    def _string_(self):  # noqa
        self._pattern(r'".+"')

    @tatsumasu()
    def _char_(self):  # noqa
        self._pattern(r"'.'")

    @tatsumasu()
    def _literal_(self):  # noqa
        with self._choice():
            with self._option():
                self._integer_()
            with self._option():
                self._string_()
            with self._option():
                self._char_()
            self._error('no available options')

    @tatsumasu()
    def _identifier_(self):  # noqa
        self._pattern(r'[A-Za-z]\w+')


class testSemantics(object):
    def start(self, ast):  # noqa
        return ast

    def expression(self, ast):  # noqa
        return ast

    def assign_expression(self, ast):  # noqa
        return ast

    def lor_expression(self, ast):  # noqa
        return ast

    def land_expression(self, ast):  # noqa
        return ast

    def or_expression(self, ast):  # noqa
        return ast

    def xor_expression(self, ast):  # noqa
        return ast

    def and_expression(self, ast):  # noqa
        return ast

    def equality_expression(self, ast):  # noqa
        return ast

    def relative_expression(self, ast):  # noqa
        return ast

    def shift_expression(self, ast):  # noqa
        return ast

    def add_expression(self, ast):  # noqa
        return ast

    def mult_expression(self, ast):  # noqa
        return ast

    def unary_expression(self, ast):  # noqa
        return ast

    def postfix_expression(self, ast):  # noqa
        return ast

    def function_expression(self, ast):  # noqa
        return ast

    def primary_expression(self, ast):  # noqa
        return ast

    def integer(self, ast):  # noqa
        return ast

    def string(self, ast):  # noqa
        return ast

    def char(self, ast):  # noqa
        return ast

    def literal(self, ast):  # noqa
        return ast

    def identifier(self, ast):  # noqa
        return ast


def main(filename, startrule, **kwargs):
    with open(filename) as f:
        text = f.read()
    parser = testParser()
    return parser.parse(text, startrule, filename=filename, **kwargs)


if __name__ == '__main__':
    import json
    from tatsu.util import asjson

    ast = generic_main(main, testParser, name='test')
    print('AST:')
    print(ast)
    print()
    print('JSON:')
    print(json.dumps(asjson(ast), indent=2))
    print()