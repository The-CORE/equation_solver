import unittest
import equation_solver


class TestExpression(unittest.TestCase):
    def test_single_value(self):
        value = equation_solver.evaluate('15')
        self.assertEqual(value, 15)

    def test_addition(self):
        value = equation_solver.evaluate('2+3')
        self.assertEqual(value, 5)

    def test_subtraction(self):
        value = equation_solver.evaluate('7-      10')
        self.assertEqual(value, -3)

    def test_multiplication(self):
        value = equation_solver.evaluate('6*9')
        self.assertEqual(value, 54)

    def test_division(self):
        value = equation_solver.evaluate('-8    /4')
        self.assertEqual(value, -2)

    def test_brakets(self):
        value = equation_solver.evaluate('6*(4-2)')
        self.assertEqual(value, 12)
        value = equation_solver.evaluate('(8/(   6  + (-2)))')
        self.assertEqual(value, 2)


class TestEquation(unittest.TestCase):
    def test_assignment(self):
        value = equation_solver.evaluate('   x=14*3')
        self.assertEqual(value, 42)

    def test_rearrangement(self):
        value = equation_solver.evaluate('2=84/   x')
        self.assertEqual(value, 42)


class TestMultipleEquations(unittest.TestCase):
    pass


unittest.main()
