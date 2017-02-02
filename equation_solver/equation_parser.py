import string
from decimal import Decimal
from .nodes import (
    EquationNode,
    ExpressionNode,
    TermNode,
    NumberNode,
    UnknownNode
)
from .exceptions import EquationError, EquationFormattingError

class EquationParser:
    def __init__(self, equation):
        self.equation = str(equation)
        for item in string.whitespace:
            self.equation = self.equation.replace(item, '')
        self.length_of_equation = len(equation)
        self.position_in_equation = 0

    def _peek(self):
        if self.position_in_equation < len(self.equation):
            return self.equation[self.position_in_equation]
        return None

    def _next(self):
        self.position_in_equation += 1

    def parse(self):
        '''
        Creates the node tree that can be evaluated into the answer.
        '''
        return self._parse_equation()

    def _parse_equation(self):
        side1 = self._parse_expression()
        side2 = None
        if self._peek() is not None:
            # parse_expression will only end if it errors, hits an equals sign
            # or hits the end of the file, so, this if statement will only
            # execute if it hit an equals sign.
            self._next()
            side2 = self._parse_expression()
        if side2 is None:
            # If there is no equals sign, put it in an equation anyway, for
            # consistency, but, give it an unknown on the lhs so it will
            # evaluate.
            return EquationNode(
                ExpressionNode([TermNode([UnknownNode('x')])]),
                side1
            )
        return EquationNode(side1, side2)

    def _parse_expression(self):
        terms = [self._parse_term()]
        while self._peek() is not None and self._peek() not in ['=', ')']:
            if self._peek() not in ['+', '-']:
                raise EquationFormattingError(
                    '''
                    terms within the same expression may only be seperated by
                    "+" and "-"
                    '''
                )
            terms.append(self._peek())
            self._next()
            terms.append(self._parse_term())
        return ExpressionNode(terms)

    def _parse_term(self):
        items = [self._parse_item()]
        while (
                self._peek() is not None
                and self._peek() not in ['+', '-', '=', ')']
        ):
            if self._peek() not in ['*', '/']:
                raise EquationFormattingError(
                    'expected "*" or "/", got {}'.format(self._peek())
                )
            items.append(self._peek())
            self._next()
            items.append(self._parse_item())
        return TermNode(items)

    def _parse_item(self):
        if (
                self._peek() is not None
                and self._peek() in string.digits
                or self._peek() in ['+', '-']
        ):
            return self._parse_number()
        elif self._peek() is not None and self._peek() in string.ascii_letters:
            return self._parse_unknown()
        elif self._peek() == '(':
            self._next()
            expression = self._parse_expression()
            if self._peek() != ')':
                raise EquationFormattingError(
                    'reached end of string, expected ")"'
                )
            self._next()
            return expression

    def _parse_number(self):
        number_string = ""
        valid = False
        if self._peek() is not None and self._peek() in ['+', '-']:
            number_string += self._peek()
            self._next()
        while self._peek() is not None and self._peek() in string.digits:
            valid = True
            number_string += self._peek()
            self._next()
        if self._peek() == '.':
            valid = False
            number_string += '.'
            self._next()
        while self._peek() is not None and self._peek() in string.digits:
            valid = True
            number_string += self._peek()
            self._next()
        if not valid:
            raise EquationFormattingError(
                'expected number, got {}'.format(number_string)
            )
        return NumberNode(Decimal(number_string))

    def _parse_unknown(self):
        node = UnknownNode(self._peek())
        self._next()
        return node
