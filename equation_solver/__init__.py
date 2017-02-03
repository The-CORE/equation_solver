from .equation_parser import EquationParser
from .exceptions import EquationError
from .nodes import UnknownNode, ExpressionNode, TermNode, NumberNode


DEBUG = False
USE_STEPS_LIMIT = True
STEPS_LIMIT = 100


def evaluate(equation_string):
    parser = EquationParser(equation_string)
    equation = parser.parse()
    equation = solve(equation)
    return equation.evaluate()


def solve(equation):
    '''
    Solves the equation.
    For now, this function and all functions called within it assume exactly
    one unknown.
    '''
    steps = 0
    if DEBUG: print(equation)
    while not equation.lhs_allows_evaluation():
        _one_step_of_cleaning(equation)
        if DEBUG: input()
        if DEBUG: print(equation)
        steps += 1
        if USE_STEPS_LIMIT and steps >= STEPS_LIMIT:
            break
    return equation


def _one_step_of_cleaning(equation):
    if _node_contains_unknown(equation.rhs):
        old_rhs = equation.rhs
        equation.rhs = equation.lhs
        equation.lhs = old_rhs
    elif len(equation.lhs.terms) == 2:
        if equation.lhs.terms.pop(0) == '-':
            equation.rhs = ExpressionNode(
                [
                    TermNode(
                        [
                            ExpressionNode([TermNode([NumberNode(-1)])]),
                            '*',
                            equation.rhs
                        ]
                    )
                ]
            )
    elif len(equation.lhs.terms) != 1:
        for term in equation.lhs.terms:
            if not _node_contains_unknown(term) and term not in ['+', '-']:
                index = equation.lhs.terms.index(term)
                equation.lhs.terms.remove(term)
                if index == 0 or equation.lhs.terms[index-1] == '+':
                    equation.rhs.terms.append('-')
                else:
                    equation.rhs.terms.append('+')
                equation.rhs.terms.append(term)
                if index != 0:
                    equation.lhs.terms.pop(index-1)
    # else:
    #     rhs_term = TermNode([equation.rhs])
    #     for item in equation.lhs.terms[0].items:
    #         if not _node_contains_unknown(item) and item not in ['*', '/']:
    #             index = equation.lhs.terms[0].items.index(term)
    #             equation.lhs.terms.remove(term)
    #             if index == 0 or equation.lhs.terms[0].items[index-1] == '+':
    #                 equation.


def _node_contains_unknown(node):
    if isinstance(node, UnknownNode):
        return True
    if hasattr(node, 'lhs'):
        if _node_contains_unknown(node.lhs) or _node_contains_unknown(node.rhs):
            return True
    if hasattr(node, 'terms'):
        for term in node.terms:
            if _node_contains_unknown(term):
                return True
    if hasattr(node, 'items'):
        for item in node.items:
            if _node_contains_unknown(item):
                return True
    return False
