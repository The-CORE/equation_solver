from .equation_parser import EquationParser
from .exceptions import EquationError
from .nodes import UnknownNode


def evaluate(equation_string):
    parser = EquationParser(equation_string)
    equation = parser.parse()
    equation = solve(equation)
    return equation.evaluate()


def solve(equation):
    """
    # Will not work.
    print(equation)
    found_unknown = False
    unknown_is_on_lhs = False
    for side in (equation.lhs, equation.rhs):
        for term in side.terms:
            if term in ['+', '-']:
                break
            for item in term.items:
                if isinstance(item, UnknownNode):
                    if found_unknown:
                        raise EquationError(
                            '''
                            equation cannot be solved if there is more than one
                            instance of an unknown
                            '''
                        )
                    found_unknown = True
                    if side == equation.lhs:
                        unknown_is_on_lhs = True
    if not unknown_is_on_lhs:
        old_rhs = equation.rhs
        equation.rhs = equation.lhs
        equation.lhs = old_rhs
    print(equation)
    """
    return equation
