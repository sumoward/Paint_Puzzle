#!/usr/bin/env python3.4.3
#
# Tests for paint puzzle
#
from unittest import TestCase
from src.solve_paint_puzzle import Paint, FileReadError


class TestValidator(TestCase):
    """
    Unit src for paint puzzle
    """

    def setUp(self):
        """
        Intialize test data
        """
        pass

    def test_parse(self):
        """
        Test the data input from a text file
        """
        text = 'test1'
        paint = Paint(text)
        paint.parse()
        expected = {
            1: {0: [(1, 1)], 1: [(1, 0), (2, 0)], 2: [(5, 0)], 'number_of_colours': 5, 'number_of_customers': 3},
            2: {0: [(1, 0)], 1: [(1, 1)], 'number_of_colours': 1, 'number_of_customers': 2}}

        self.assertEqual(paint.cases, expected)

        text = 'test_empty'
        paint = Paint(text)
        try:
            paint.parse()
        except FileReadError as error:
            self.assertEqual('Error reading in file, The structure of the data is incorrect', error.__str__())

    def test_build_potential_solutions(self):
        """
        Test that we get sorted solutions
        """
        colours = 5
        text = 'test1'
        paint = Paint(text)
        solutions = paint.build_potential_solutions(colours)
        # the best solution is no matte
        expected_first = (0, 0, 0, 0, 0)
        self.assertEqual(next(solutions), expected_first)

        for x in range(colours):
            sol = next(solutions)
            self.assertEqual(sum(sol), 1)

        for x in range(colours * 2):
            sol = next(solutions)
            self.assertEqual(sum(sol), 2)

        for x in range(colours * 2):
            sol = next(solutions)
            self.assertEqual(sum(sol), 3)

        for x in range(colours):
            sol = next(solutions)
            self.assertEqual(sum(sol), 4)

        # the final solution is all matte
        expected_final = (1, 1, 1, 1, 1)
        self.assertEqual(next(solutions), expected_final)

    def test_check_solution(self):
        """
        Test the validation of a solution
        """
        solution = [1, 0, 0, 0, 0]
        text = 'test1'
        paint = Paint(text)

        case = {0: [(1, 1)], 1: [(1, 0), (2, 0)], 2: [(5, 0)], 'number_of_colours': 5, 'number_of_customers': 3}
        result = paint.check_solution(solution, case)
        self.assertTrue(result)

        solution = [0, 0, 0, 0, 0]
        result = paint.check_solution(solution, case)
        self.assertFalse(result)

        # test that an inefficient solution passes
        solution = [1, 0, 1, 1, 0]
        result = paint.check_solution(solution, case)
        self.assertTrue(result)

        case = {0: [(1, 0)], 1: [(1, 1)], 'number_of_colours': 1, 'number_of_customers': 2}
        solution = [1, 0]
        result = paint.check_solution(solution, case)
        self.assertFalse(result)

        solution = [1, 1]
        result = paint.check_solution(solution, case)
        self.assertFalse(result)

    def test_handle_cases(self):
        """
        Test the check for solution
        """
        case = {0: [(1, 1)], 1: [(1, 0), (2, 0)], 2: [(5, 0)], 'number_of_colours': 5, 'number_of_customers': 3}
        text = 'test1'
        paint = Paint(text)
        result = paint.handle_case(case)
        expected = (1, 0, 0, 0, 0)
        self.assertEqual(result, expected)

        case = {0: [(1, 0)], 1: [(1, 1)], 'number_of_colours': 1, 'number_of_customers': 2}
        result = paint.handle_case(case)
        expected = 'IMPOSSIBLE'
        self.assertEqual(result, expected)
