# !/usr/bin/env python3.4.3
#
# Puzzle Solution

import itertools
import sys


class FileReadError(Exception):
    """Risen on error with reading in of file"""

    def __str__(self):
        return "Error reading in file, " + self.args[0]


class Paint(object):
    """
    Class to handle a paint puzzle
    """

    def __init__(self, text=None):
        """
        :param text: the location of the input file
        """
        self.text = text
        self.cases = {}
        self.test_cases = 0

    def parse(self):
        """
        Read in a file to a dictionary
        :return: a dictionary of cases
        """
        with open(self.text, 'r') as infile:
            # get the number of test cases we have
            try:
                error_message = 'The structure of the data is incorrect'
                self.test_cases = int(infile.readline())
                for case in range(1, self.test_cases + 1):
                    self.cases[case] = {}
                    number_of_colours = infile.readline()
                    if not number_of_colours:
                        raise FileReadError(error_message)
                    self.cases[case]['number_of_colours'] = int(number_of_colours)
                    number_of_customers = infile.readline()
                    if not number_of_customers:
                        raise FileReadError(error_message)
                    number_of_customers = int(number_of_customers)
                    self.cases[case]['number_of_customers'] = number_of_customers
                    total_preferences = 0
                    for line in range(number_of_customers):
                        data = infile.readline()
                        if not data:
                            raise FileReadError(error_message)
                        # remove \n
                        number_of_customer_preferences, customer_preferences = data[:-1].split(' ', 1)
                        number_of_customer_preferences = int(number_of_customer_preferences)
                        total_preferences += number_of_customer_preferences
                        if total_preferences > 3000:
                            raise FileReadError('This test case is too large and will not proceed')
                        # check the number of tuples  matches the number of declared preferences
                        customer_preferences = customer_preferences.split()
                        if len(customer_preferences) / 2 != number_of_customer_preferences:
                            raise FileReadError(error_message)
                        # convert to ints
                        first_element = [int(pref) for pref in customer_preferences[0::2]]
                        second_element = [int(pref) for pref in customer_preferences[1::2]]
                        # create tuples
                        zipped = zip(first_element, second_element)
                        self.cases[case][line] = list(zipped)
            except ValueError as err:
                raise FileReadError(error_message)

    def handle_case(self, case):
        """
        A batch with all colors in glossy variety.
        Then, it switches from glossy to matte one by one and checks if the solution satisfies. If it does, stop
        :param case: the case we are looking at
        :return: the solution or string
        """
        colours = case['number_of_colours']
        solutions = self.build_potential_solutions(colours)

        for solution in solutions:
            if self.check_solution(solution, case):
                return solution
        return 'IMPOSSIBLE'

    def build_potential_solutions(self, colours):
        """
        Change the solution  on one index
        :param colours: the number of colour combinations
        :return: solution
        """
        # all possible combinations of of gloss, matte over the range of colors
        combo = list(itertools.product(range(2), repeat=colours))
        # sort by lowest number of matte
        combo.sort(key=lambda y: sum(y))
        for solution in combo:
            yield solution

    def check_solution(self, solution, case):
        """
        Check the solution meets the needs of our customer
        :param solution:
        :param case:
        :return: Boolean
        """
        colours = case['number_of_colours']
        customers = case['number_of_customers']
        # create tuple for comparison with customer
        solution = list(zip(range(1, colours + 1), solution))
        for customer in range(customers):
            # check each tuple in the solution to see if it is a customers choice
            choice_present = [choice for choice in case[customer] if choice in solution]
            if not choice_present:
                return False
        return True

    def main(self):
        """
        Print the solutions for all cases
        """
        try:
            self.parse()
        except FileReadError as error:
            return error.__str__
        results = []
        for case in range(1, self.test_cases + 1):
            solution = self.handle_case(self.cases[case])
            if solution != 'IMPOSSIBLE':
                solution = ' '.join([str(val) for val in solution])
            reply = 'Case #' + str(case) + ': ' + solution
            results.append(reply)
        for result in results:
            print(result)


if __name__ == '__main__':
    try:
        if len(sys.argv) > 1:
            paint = Paint(sys.argv[1])
            paint.main()
        else:
            print('Please supply a file for input, format is : Python3 solve_paint_puzzle.py FILENAME')
    except IOError as er:
        print(er)


