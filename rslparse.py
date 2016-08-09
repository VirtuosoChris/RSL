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

from grako.buffering import Buffer
from grako.parsing import graken, Parser
from grako.util import re, RE_FLAGS, generic_main  # noqa


__version__ = (2016, 8, 9, 11, 34, 22, 1)

__all__ = [
    'RSLParser',
    'RSLSemantics',
    'main'
]

KEYWORDS = set([
    'alias',
    'byte',
    'char',
    'class',
    'const',
    'double',
    'dword',
    'else',
    'elseif',
    'export',
    'float',
    'for',
    'func',
    'half',
    'if',
    'int',
    'long',
    'module',
    'oword',
    'persistent',
    'qword',
    'rasterize',
    'sequential',
    'short',
    'struct',
    'uchar',
    'uint',
    'ulong',
    'ushort',
    'word',
])


class RSLBuffer(Buffer):
    def __init__(self,
                 text,
                 whitespace=None,
                 nameguard=None,
                 comments_re='/\\*.*?\\*/',
                 eol_comments_re='//.*?$',
                 ignorecase=None,
                 namechars='',
                 **kwargs):
        super(RSLBuffer, self).__init__(
            text,
            whitespace=whitespace,
            nameguard=nameguard,
            comments_re=comments_re,
            eol_comments_re=eol_comments_re,
            ignorecase=ignorecase,
            namechars=namechars,
            **kwargs
        )


class RSLParser(Parser):
    def __init__(self,
                 whitespace=None,
                 nameguard=None,
                 comments_re='/\\*.*?\\*/',
                 eol_comments_re='//.*?$',
                 ignorecase=None,
                 left_recursion=True,
                 keywords=KEYWORDS,
                 namechars='',
                 **kwargs):
        super(RSLParser, self).__init__(
            whitespace=whitespace,
            nameguard=nameguard,
            comments_re=comments_re,
            eol_comments_re=eol_comments_re,
            ignorecase=ignorecase,
            left_recursion=left_recursion,
            keywords=keywords,
            namechars=namechars,
            **kwargs
        )

    def parse(self, text, *args, **kwargs):
        if not isinstance(text, Buffer):
            text = RSLBuffer(text, **kwargs)
        return super(RSLParser, self).parse(text, *args, **kwargs)

    @graken()
    def _identifier_(self):
        self._pattern(r'(?!\d)\w+')
        self._check_name()

    @graken()
    def _split_identifier_(self):

        def sep0():
            self._token('.')

        def block0():
            self._identifier_()
        self._positive_closure(block0, sep=sep0)

    @graken()
    def _call_parameter_(self):
        with self._optional():
            self._identifier_()
            self._token('=')
        self._expression_()

    @graken()
    def _call_parameters_(self):
        self._token('(')

        def sep0():
            self._token(',')

        def block0():
            self._call_parameter_()
        self._closure(block0, sep=sep0)
        self._token(')')

    @graken()
    def _define_parameters_(self):
        self._token('(')

        def sep0():
            self._token(',')

        def block0():
            self._variable_declaration_initialization_()
            self.add_last_node_to_name('@')
        self._closure(block0, sep=sep0)
        self._token(')')

    @graken()
    def _array_index_(self):
        self._token('[')
        self._expression_()
        self._token(']')

    @graken()
    def _template_call_parameter_(self):
        with self._optional():
            self._identifier_()
            self._token('=')
        with self._group():
            with self._choice():
                with self._option():
                    self._type_()
                with self._option():
                    self._expression_()
                self._error('no available options')

    @graken()
    def _template_call_parameters_(self):
        self._token('<')

        def sep0():
            self._token(',')

        def block0():
            self._template_call_parameter_()
            self.add_last_node_to_name('@')
        self._closure(block0, sep=sep0)
        self._token('>')

    @graken()
    def _template_define_parameters_(self):
        self._token('<')

        def sep0():
            self._token(',')

        def block0():
            self._variable_declaration_initialization_()
            self.add_last_node_to_name('@')
        self._closure(block0, sep=sep0)
        self._token('>')

    @graken()
    def _type_(self):
        self._split_identifier_()
        with self._optional():
            self._template_call_parameters_()
        with self._optional():
            self._array_index_()

    @graken()
    def _variable_attribute_(self):
        with self._choice():
            with self._option():
                self._token('persistent')
            with self._option():
                self._token('export')
            self._error('expecting one of: export persistent')

    @graken()
    def _variable_declaration_(self):

        def block0():
            self._variable_attribute_()
        self._closure(block0)
        self._type_()
        self._identifier_()

    @graken()
    def _variable_declaration_initialization_(self):
        self._variable_declaration_()
        with self._optional():
            self._token('=')
            self._expression_()

    @graken()
    def _variable_declaration_construction_(self):
        self._variable_declaration_()
        self._call_parameters_()

    @graken()
    def _variable_declaration_statement_(self):
        with self._group():
            with self._choice():
                with self._option():
                    self._variable_declaration_initialization_()
                with self._option():
                    self._variable_declaration_construction_()
                self._error('no available options')
        self._token(';')

    @graken()
    def _file_(self):

        def block0():
            self._file_statement_()
        self._closure(block0)

    @graken()
    def _file_statement_(self):
        with self._choice():
            with self._option():
                self._import_statement_()
            with self._option():

                def block0():
                    self._module_statement_()
                self._closure(block0)
            self._error('no available options')

    @graken()
    def _import_statement_(self):
        self._token('import')
        self._split_identifier_()

    @graken()
    def _module_attribute_(self):
        self._token('export')

    @graken()
    def _module_(self):

        def block0():
            self._module_attribute_()
        self._closure(block0)
        self._token('module')
        self._identifier_()
        self._token('{')

        def block1():
            self._module_statement_()
        self._closure(block1)
        self._token('}')

    @graken()
    def _module_statement_(self):
        with self._choice():
            with self._option():
                self._module_()
            with self._option():

                def block0():
                    self._inner_statement_()
                self._closure(block0)
            self._error('no available options')

    @graken()
    def _class_attribute_(self):
        self._token('export')

    @graken()
    def _identifier_declaration_(self):
        self._identifier_()
        with self._optional():
            self._template_define_parameters_()

    @graken()
    def _class_(self):

        def block0():
            self._class_attribute_()
        self._closure(block0)
        self._token('class')
        self._identifier_declaration_()
        self._token('{')

        def block1():
            self._inner_statement_()
        self._closure(block1)
        self._token('}')

    @graken()
    def _struct_(self):

        def block0():
            self._class_attribute_()
        self._closure(block0)
        self._token('struct')
        self._identifier_declaration_()
        self._token('{')

        def block1():
            self._inner_statement_()
        self._closure(block1)
        self._token('}')

    @graken()
    def _inner_statement_(self):
        with self._choice():
            with self._option():
                self._class_()
            with self._option():
                self._struct_()
            with self._option():
                self._export_()
            with self._option():
                self._alias_()
            with self._option():
                self._variable_declaration_statement_()
            with self._option():
                self._func_()
            self._error('no available options')

    @graken()
    def _export_(self):
        self._token('export')
        self._type_()
        self._token(';')

    @graken()
    def _alias_(self):
        self._token('alias')
        self._type_()
        self._token('=')
        self._type_()
        self._token(';')

    @graken()
    def _func_attribute_(self):
        self._token('export')

    @graken()
    def _func_(self):

        def block0():
            self._func_attribute_()
        self._closure(block0)
        self._token('func')
        self._identifier_declaration_()
        self._define_parameters_()
        with self._optional():
            self._token('->')
            self._define_parameters_()
        self._token('{')

        def block1():
            self._func_statement_()
        self._closure(block1)
        self._token('}')

    @graken()
    def _func_call_(self):
        self._split_identifier_()
        with self._optional():
            self._template_call_parameters_()
        with self._optional():
            self._call_parameters_()

    @graken()
    def _variable_lvalue_(self):
        self._split_identifier_()
        with self._optional():
            self._array_index_()

    @graken()
    def _lvalue_(self):
        self._variable_lvalue_()

    @graken()
    def _func_statement_(self):
        with self._choice():
            with self._option():
                self._control_statement_()
            with self._option():
                self._inner_statement_()
            self._error('no available options')

    @graken()
    def _func_call_statement_(self):
        self._func_call_()
        self._token('->')
        self._call_parameters_()

    @graken()
    def _control_statement_(self):
        with self._choice():
            with self._option():
                self._for_()
            with self._option():
                self._while_()
            with self._option():
                self._if_()
            with self._option():
                self._expression_statement_()
            with self._option():
                self._func_call_statement_()
            self._error('no available options')

    @graken()
    def _for_attribute_(self):
        self._token('sequential')

    @graken()
    def _for_(self):

        def block0():
            self._for_attribute_()
        self._closure(block0)
        self._token('for')
        self._for_args_()
        self._token('{')

        def block1():
            self._control_statement_()
        self._closure(block1)
        self._token('}')

    @graken()
    def _for_arg_(self):
        self._identifier_()
        self._token(':')
        self._expression_()

    @graken()
    def _for_args_(self):
        self._token('(')

        def sep0():
            self._token(',')

        def block0():
            self._for_arg_()
        self._positive_closure(block0, sep=sep0)
        self._token(')')

    @graken()
    def _while_(self):
        self._token('while')
        self._token('(')
        self._expression_()
        self._token(')')
        self._token('{')

        def block0():
            self._control_statement_()
        self._closure(block0)
        self._token('}')

    @graken()
    def _if_(self):
        self._token('if')
        self._token('(')
        self._expression_()
        self._token(')')
        self._token('{')

        def block0():
            self._control_statement_()
        self._closure(block0)
        self._token('}')

        def block1():
            self._elseif_()
        self._closure(block1)
        with self._optional():
            self._else_()

    @graken()
    def _elseif_(self):
        self._token('elseif')
        self._token('(')
        self._expression_()
        self._token(')')
        self._token('{')

        def block0():
            self._control_statement_()
        self._closure(block0)
        self._token('}')

    @graken()
    def _else_(self):
        self._token('elseif')
        self._token('(')
        self._expression_()
        self._token(')')
        self._token('{')

        def block0():
            self._control_statement_()
        self._closure(block0)
        self._token('}')

    @graken()
    def _expression_statement_(self):
        self._binary_lvalue_op_()
        self._token(';')

    @graken()
    def _binary_lvalue_op_(self):
        self._lvalue_()
        with self._group():
            with self._choice():
                with self._option():
                    self._token('=')
                with self._option():
                    self._token('+=')
                with self._option():
                    self._token('-=')
                with self._option():
                    self._token('*=')
                with self._option():
                    self._token('%=')
                with self._option():
                    self._token('/=')
                with self._option():
                    self._token('<<=')
                with self._option():
                    self._token('>>=')
                with self._option():
                    self._token('|=')
                with self._option():
                    self._token('&=')
                with self._option():
                    self._token('^=')
                self._error('expecting one of: %= &= *= += -= /= <<= = >>= ^= |=')
        self._expression_()

    @graken()
    def _unary_lvalue_op_(self):
        with self._choice():
            with self._option():
                self._left_u_lvalue_op_()
            with self._option():
                self._right_u_lvalue_op_()
            self._error('no available options')

    @graken()
    def _left_u_lvalue_op_(self):
        with self._group():
            with self._choice():
                with self._option():
                    self._token('++')
                with self._option():
                    self._token('--')
                self._error('expecting one of: ++ --')
        self._lvalue_()

    @graken()
    def _right_u_lvalue_op_(self):
        self._lvalue_()
        with self._group():
            with self._choice():
                with self._option():
                    self._token('++')
                with self._option():
                    self._token('--')
                self._error('expecting one of: ++ --')

    @graken()
    def _binary_arith_op_(self):
        self._expression_()
        with self._group():
            with self._choice():
                with self._option():
                    self._token('+')
                with self._option():
                    self._token('-')
                with self._option():
                    self._token('%')
                with self._option():
                    self._token('^')
                with self._option():
                    self._token('*')
                with self._option():
                    self._token('/')
                with self._option():
                    self._token('&')
                with self._option():
                    self._token('^')
                with self._option():
                    self._token('|')
                with self._option():
                    self._token('>>')
                with self._option():
                    self._token('<<')
                self._error('expecting one of: % & * + - / << >> ^ |')
        self._expression_()

    @graken()
    def _unary_arith_op_(self):
        with self._group():
            with self._choice():
                with self._option():
                    self._token('!')
                with self._option():
                    self._token('~')
                with self._option():
                    self._token('-')
                with self._option():
                    self._token('+')
                self._error('expecting one of: ! + - ~')
        self._expression_()

    @graken()
    def _binary_comparison_op_(self):
        self._expression_()
        with self._group():
            with self._choice():
                with self._option():
                    self._token('==')
                with self._option():
                    self._token('!=')
                with self._option():
                    self._token('<')
                with self._option():
                    self._token('<=')
                with self._option():
                    self._token('>')
                with self._option():
                    self._token('>=')
                with self._option():
                    self._token('&&')
                with self._option():
                    self._token('||')
                with self._option():
                    self._token('^^')
                self._error('expecting one of: != && < <= == > >= ^^ ||')
        self._expression_()

    @graken()
    def _ternary_op_(self):
        self._expression_()
        self._token('?')
        self._expression_()
        self._token(':')
        self._expression_()

    @graken()
    def _brace_initializer_(self):
        self._token('{')

        def sep0():
            self._token(',')

        def block0():
            self._expression_()
            self.add_last_node_to_name('@')
        self._closure(block0, sep=sep0)
        self._token('}')

    @graken()
    def _expression_(self):
        with self._choice():
            with self._option():
                with self._group():
                    self._token('(')
                    self._expression_()
                    self._token(')')
            with self._option():
                self._binary_arith_op_()
            with self._option():
                self._unary_arith_op_()
            with self._option():
                self._binary_comparison_op_()
            with self._option():
                self._unary_lvalue_op_()
            with self._option():
                self._left_u_lvalue_op_()
            with self._option():
                self._right_u_lvalue_op_()
            with self._option():
                self._binary_lvalue_op_()
            with self._option():
                self._ternary_op_()
            with self._option():
                self._func_call_()
            with self._option():
                self._brace_initializer_()
            with self._option():
                self._numeric_constant_()
            with self._option():
                self._variable_lvalue_()
            self._error('no available options')

    @graken()
    def _numeric_constant_(self):
        with self._choice():
            with self._option():
                self._float_constant_()
            with self._option():
                self._integer_constant_()
            self._error('no available options')

    @graken()
    def _integer_constant_(self):
        with self._choice():
            with self._option():
                self._hex_constant_()
            with self._option():
                self._binary_constant_()
            with self._option():
                self._octal_constant_()
            with self._option():
                self._decimal_constant_()
            self._error('no available options')

    @graken()
    def _hex_constant_(self):
        self._pattern(r'0x[0-9A-Fa-f]+')

    @graken()
    def _decimal_constant_(self):
        self._pattern(r'[1-9][0-9]*')

    @graken()
    def _binary_constant_(self):
        self._pattern(r'0b[01]+')

    @graken()
    def _octal_constant_(self):
        self._pattern(r'0[0-9]*')

    @graken()
    def _float_constant_(self):
        self._decimal_constant_()
        self._token('.')
        with self._optional():
            self._decimal_constant_()

    @graken()
    def _start_(self):
        self._file_()


class RSLSemantics(object):
    def identifier(self, ast):
        return ast

    def split_identifier(self, ast):
        return ast

    def call_parameter(self, ast):
        return ast

    def call_parameters(self, ast):
        return ast

    def define_parameters(self, ast):
        return ast

    def array_index(self, ast):
        return ast

    def template_call_parameter(self, ast):
        return ast

    def template_call_parameters(self, ast):
        return ast

    def template_define_parameters(self, ast):
        return ast

    def type(self, ast):
        return ast

    def variable_attribute(self, ast):
        return ast

    def variable_declaration(self, ast):
        return ast

    def variable_declaration_initialization(self, ast):
        return ast

    def variable_declaration_construction(self, ast):
        return ast

    def variable_declaration_statement(self, ast):
        return ast

    def file(self, ast):
        return ast

    def file_statement(self, ast):
        return ast

    def import_statement(self, ast):
        return ast

    def module_attribute(self, ast):
        return ast

    def module(self, ast):
        return ast

    def module_statement(self, ast):
        return ast

    def class_attribute(self, ast):
        return ast

    def identifier_declaration(self, ast):
        return ast

    def class_(self, ast):
        return ast

    def struct(self, ast):
        return ast

    def inner_statement(self, ast):
        return ast

    def export(self, ast):
        return ast

    def alias(self, ast):
        return ast

    def func_attribute(self, ast):
        return ast

    def func(self, ast):
        return ast

    def func_call(self, ast):
        return ast

    def variable_lvalue(self, ast):
        return ast

    def lvalue(self, ast):
        return ast

    def func_statement(self, ast):
        return ast

    def func_call_statement(self, ast):
        return ast

    def control_statement(self, ast):
        return ast

    def for_attribute(self, ast):
        return ast

    def for_(self, ast):
        return ast

    def for_arg(self, ast):
        return ast

    def for_args(self, ast):
        return ast

    def while_(self, ast):
        return ast

    def if_(self, ast):
        return ast

    def elseif(self, ast):
        return ast

    def else_(self, ast):
        return ast

    def expression_statement(self, ast):
        return ast

    def binary_lvalue_op(self, ast):
        return ast

    def unary_lvalue_op(self, ast):
        return ast

    def left_u_lvalue_op(self, ast):
        return ast

    def right_u_lvalue_op(self, ast):
        return ast

    def binary_arith_op(self, ast):
        return ast

    def unary_arith_op(self, ast):
        return ast

    def binary_comparison_op(self, ast):
        return ast

    def ternary_op(self, ast):
        return ast

    def brace_initializer(self, ast):
        return ast

    def expression(self, ast):
        return ast

    def numeric_constant(self, ast):
        return ast

    def integer_constant(self, ast):
        return ast

    def hex_constant(self, ast):
        return ast

    def decimal_constant(self, ast):
        return ast

    def binary_constant(self, ast):
        return ast

    def octal_constant(self, ast):
        return ast

    def float_constant(self, ast):
        return ast

    def start(self, ast):
        return ast


def main(
        filename,
        startrule,
        trace=False,
        whitespace=None,
        nameguard=None,
        comments_re='/\\*.*?\\*/',
        eol_comments_re='//.*?$',
        ignorecase=None,
        left_recursion=True,
        **kwargs):

    with open(filename) as f:
        text = f.read()
    whitespace = whitespace or None
    parser = RSLParser(parseinfo=False)
    ast = parser.parse(
        text,
        startrule,
        filename=filename,
        trace=trace,
        whitespace=whitespace,
        nameguard=nameguard,
        ignorecase=ignorecase,
        **kwargs)
    return ast

if __name__ == '__main__':
    import json
    ast = generic_main(main, RSLParser, name='RSL')
    print('AST:')
    print(ast)
    print()
    print('JSON:')
    print(json.dumps(ast, indent=2))
    print()
