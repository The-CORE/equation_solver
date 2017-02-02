from .exceptions import EquationError, EquationFormattingError


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

    def __str__(self):
        return str(self.lhs) + ' = ' + str(self.rhs)

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

    def __str__(self):
        return '(' + ' '.join([str(term) for term in self.terms]).strip() + ')'


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

    def __str__(self):
        return ' '.join([str(item) for item in self.items]).strip()


class NumberNode:
    def __init__(self, value):
        self.value = value

    def evaluate(self):
        return self.value

    def __str__(self):
        return str(self.value)

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

    def __str__(self):
        return self.name
