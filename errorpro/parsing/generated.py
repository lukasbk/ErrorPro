#!/usr/bin/env python
# -*- coding: utf-8 -*-

# CAVEAT UTILITOR
#
# This file was automatically generated by Grako.
#
#    https://pypi.python.org/pypi/grako/
#
# Any changes you make to it will be overwritten the next time
# the file is generated.


from __future__ import print_function, division, absolute_import, unicode_literals

from grako.parsing import graken, Parser
from grako.util import re, RE_FLAGS


__version__ = (2016, 5, 2, 11, 39, 9, 0)

__all__ = [
    'DatParser',
    'DatSemantics',
    'main'
]


class DatParser(Parser):
    def __init__(self,
                 whitespace=None,
                 nameguard=None,
                 comments_re=None,
                 eol_comments_re=None,
                 ignorecase=None,
                 left_recursion=True,
                 **kwargs):
        super(DatParser, self).__init__(
            whitespace=whitespace,
            nameguard=nameguard,
            comments_re=comments_re,
            eol_comments_re=eol_comments_re,
            ignorecase=ignorecase,
            left_recursion=left_recursion,
            **kwargs
        )

    @graken()
    def _subformula_without_brackets_(self):
        self._pattern(r"[^=,\(\)\[\]<>\n\r']+")

    @graken()
    def _subformula_(self):
        with self._choice():
            with self._option():
                with self._optional():
                    self._subformula_without_brackets_()
                self._token('(')
                self._subformula_()
                self._token(')')
                with self._optional():
                    self._subformula_()
            with self._option():
                self._subformula_without_brackets_()
            self._error('no available options')

    @graken()
    def _formula_(self):
        with self._choice():
            with self._option():
                self._subformula_()
            with self._option():
                self._token("'")
                self._pattern(r"[^']*")
                self.ast['@'] = self.last_node
                self._token("'")
            self._error("expecting one of: '")

    @graken()
    def _variable_name_(self):
        self._pattern(r'[\w]+')

    @graken()
    def _longname_(self):
        with self._choice():
            with self._option():
                self._token('"')
                self._pattern(r'[^\"]+')
                self.ast['@'] = self.last_node
                self._token('"')
            with self._option():

                def block2():
                    self._pattern(r'[^,\[\]=\(\)\{\}<>\s]+')
                    self._pattern(r'[\t ]+')
                    with self._if():
                        self._pattern(r'[^,\[\]=\(\)\{\}<>\s]+')
                self._positive_closure(block2)

                self.ast['@'] = self.last_node
            self._error('expecting one of: " [^,\\[\\]=\\(\\)\\{\\}<>\\s]+')

    @graken()
    def _error_(self):
        self._token('<')
        self._formula_()
        self.ast['@'] = self.last_node
        self._token('>')

    @graken()
    def _unit_(self):
        self._token('[')
        self._formula_()
        self.ast['@'] = self.last_node
        self._token(']')

    @graken()
    def _assignment_(self):
        with self._optional():
            self._longname_()
            self.ast['longname'] = self.last_node
        self._variable_name_()
        self.ast['name'] = self.last_node
        self._token('=')
        self._formula_()
        self.ast['value'] = self.last_node
        with self._optional():
            self._error_()
            self.ast['error'] = self.last_node
        with self._optional():
            self._unit_()
            self.ast['unit'] = self.last_node

        self.ast._define(
            ['longname', 'name', 'value', 'error', 'unit'],
            []
        )

    @graken()
    def _newline_(self):
        with self._optional():
            with self._choice():
                with self._option():
                    self._token('\r\n')
                with self._option():
                    self._token('\n')
                with self._option():
                    self._token('\r')
                self._error('expecting one of: \n \r \r\n')

    @graken()
    def _whitespace_(self):

        def block0():
            self._newline_()
        self._closure(block0)

    @graken()
    def _multi_assignment_spec_(self):
        with self._optional():
            self._longname_()
            self.ast['longname'] = self.last_node
        self._variable_name_()
        self.ast['name'] = self.last_node
        with self._optional():
            self._error_()
            self.ast['error'] = self.last_node
        with self._optional():
            self._unit_()
            self.ast['unit'] = self.last_node

        self.ast._define(
            ['longname', 'name', 'error', 'unit'],
            []
        )

    @graken()
    def _multi_assignment_header_(self):
        self._multi_assignment_spec_()
        self.ast.setlist('@', self.last_node)

        def block1():
            self._token(',')
            self._multi_assignment_spec_()
            self.ast.setlist('@', self.last_node)
        self._closure(block1)
        self._newline_()

    @graken()
    def _multi_assignment_value_(self):
        self._pattern(r'[-/\w\.\*]+')

    @graken()
    def _multi_assignment_row_(self):

        def block0():
            self._multi_assignment_value_()
            self.ast.setlist('@', self.last_node)
        self._positive_closure(block0)

        self._newline_()

    @graken()
    def _multi_assignment_rows_(self):

        def block0():
            self._multi_assignment_row_()
            self.ast.setlist('@', self.last_node)
            self._whitespace_()
        self._closure(block0)

    @graken()
    def _multi_assignment_(self):
        self._token('{')
        self._whitespace_()
        self._multi_assignment_header_()
        self.ast['header'] = self.last_node
        self._whitespace_()
        self._multi_assignment_rows_()
        self.ast['rows'] = self.last_node
        self._whitespace_()
        self._token('}')

        self.ast._define(
            ['header', 'rows'],
            []
        )

    @graken()
    def _python_line_(self):
        self._token('>')
        self._pattern(r'[^\n\r]*')
        self.ast['@'] = self.last_node

    @graken()
    def _python_code_(self):
        with self._group():
            self._python_line_()
            self.ast.setlist('code', self.last_node)

            def block1():
                self._newline_()
                self._python_line_()
                self.ast.setlist('code', self.last_node)
            self._closure(block1)

        self.ast._define(
            [],
            ['code']
        )

    @graken()
    def _command_(self):
        with self._group():
            with self._choice():
                with self._option():
                    self._assignment_()
                with self._option():
                    self._multi_assignment_()
                with self._option():
                    self._python_code_()
                self._error('no available options')
        self.ast['@'] = self.last_node
        with self._group():
            with self._choice():
                with self._option():
                    self._newline_()
                with self._option():
                    self._check_eof()
                self._error('no available options')

    @graken()
    def _program_(self):
        self._whitespace_()

        def block0():
            self._command_()
            self.ast.setlist('@', self.last_node)
            self._whitespace_()
        self._closure(block0)
        self._check_eof()


class DatSemantics(object):
    def subformula_without_brackets(self, ast):
        return ast

    def subformula(self, ast):
        return ast

    def formula(self, ast):
        return ast

    def variable_name(self, ast):
        return ast

    def longname(self, ast):
        return ast

    def error(self, ast):
        return ast

    def unit(self, ast):
        return ast

    def assignment(self, ast):
        return ast

    def newline(self, ast):
        return ast

    def whitespace(self, ast):
        return ast

    def multi_assignment_spec(self, ast):
        return ast

    def multi_assignment_header(self, ast):
        return ast

    def multi_assignment_value(self, ast):
        return ast

    def multi_assignment_row(self, ast):
        return ast

    def multi_assignment_rows(self, ast):
        return ast

    def multi_assignment(self, ast):
        return ast

    def python_line(self, ast):
        return ast

    def python_code(self, ast):
        return ast

    def command(self, ast):
        return ast

    def program(self, ast):
        return ast


def main(filename, startrule, trace=False, whitespace=None, nameguard=None):
    import json
    with open(filename) as f:
        text = f.read()
    parser = DatParser(parseinfo=False)
    ast = parser.parse(
        text,
        startrule,
        filename=filename,
        trace=trace,
        whitespace=whitespace,
        nameguard=nameguard)
    print('AST:')
    print(ast)
    print()
    print('JSON:')
    print(json.dumps(ast, indent=2))
    print()

if __name__ == '__main__':
    import argparse
    import string
    import sys

    class ListRules(argparse.Action):
        def __call__(self, parser, namespace, values, option_string):
            print('Rules:')
            for r in DatParser.rule_list():
                print(r)
            print()
            sys.exit(0)

    parser = argparse.ArgumentParser(description="Simple parser for Dat.")
    parser.add_argument('-l', '--list', action=ListRules, nargs=0,
                        help="list all rules and exit")
    parser.add_argument('-n', '--no-nameguard', action='store_true',
                        dest='no_nameguard',
                        help="disable the 'nameguard' feature")
    parser.add_argument('-t', '--trace', action='store_true',
                        help="output trace information")
    parser.add_argument('-w', '--whitespace', type=str, default=string.whitespace,
                        help="whitespace specification")
    parser.add_argument('file', metavar="FILE", help="the input file to parse")
    parser.add_argument('startrule', metavar="STARTRULE",
                        help="the start rule for parsing")
    args = parser.parse_args()

    main(
        args.file,
        args.startrule,
        trace=args.trace,
        whitespace=args.whitespace,
        nameguard=not args.no_nameguard
    )
