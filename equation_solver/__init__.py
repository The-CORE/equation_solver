import string
from decimal import Decimal


def evaluate(equation_string):
    parser = EquationParser(equation_string)
    equation = parser.parse()
    return equation.evaluate()


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


class EquationNode:
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs

    def _lhs_allows_evaluation(self):
        '''
        The equation can only be validated if the left hand side contains only
        an unknown. This functions checks if that is the case.
        '''
        try:
            if (
                    len(self.lhs.terms) != 1
                    or len(self.lhs.terms[0].items) != 1
                    or not isinstance(self.lhs.terms[0].items[0], UnknownNode)
            ):
                return False
        except AttributeError:
            return False
        return True

    def evaluate(self):
        if not self._lhs_allows_evaluation():
            print(self.lhs.terms)
            raise EquationError('lhs must be a single unknown to be evaluted')
        return self.rhs.evaluate()

class ExpressionNode:
    def __init__(self, terms):
        self.terms = terms

    def evaluate(self):
        value = 0
        modifier = 1
        for term in self.terms:
            if term == '+':
                modifier = 1
            elif term == '-':
                modifier = -1
            else:
                value += modifier * term.evaluate()
        return value


class TermNode:
    def __init__(self, items):
        self.items = items

    def evaluate(self):
        value = 1
        multiply = True
        for item in self.items:
            if item == '*':
                multiply = True
            elif item == '/':
                multiply = False
            else:
                if multiply:
                    value *= item.evaluate()
                else:
                    value /= item.evaluate()
        return value


class NumberNode:
    def __init__(self, value):
        self.value = value

    def evaluate(self):
        return self.value


class UnknownNode:
    def __init__(self, name):
        name = str(name)
        if len(name) != 1:
            raise EquationError(
                'name of unknown cannot be more than one character'
            )
        self.name = name

    def evaluate(self):
        raise EquationError('cannot evaluate unknown')


class EquationError(Exception):
    pass

class EquationFormattingError(EquationError):
    pass
