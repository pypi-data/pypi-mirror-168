import numpy as np

class sudoku_solver:

    def __init__(self, grid):
        self.grid = grid

    def possible(self, row, column, number):

        """

        :param row: the row we are checking for
        :param column: the column we are checking for
        :param number: the number we are checking
        :return: True or False
        """

        # availability in row check
        for i in range(0, 9):
            if self.grid[row][i] == number:
                return False

        # availability in column check
        for i in range(0, 9):
            if self.grid[i][column] == number:
                return False

        # availability in square check
        x0 = (column // 3) * 3
        y0 = (row // 3) * 3
        for i in range(0, 3):
            for j in range(0, 3):
                if self.grid[y0 + i][x0 + j] == number:
                    return False
        return True

    def solve(self):
        """Description : This method takes one arguement, which in format of list of lists.The 9X9 sudoku should be given in a form of list of lists where there will be zeros (0) in place of null values.
            Sample : input for the method should be in the bellow format--
                    A = [[5,3,0,0,7,0,0,0,0],
                         [6,0,0,1,9,5,0,0,0],
                         [0,9,8,0,0,0,0,6,0],
                         [8,0,0,0,6,0,0,0,3],
                         [4,0,0,8,0,3,0,0,1],
                         [7,0,0,0,2,0,0,0,6],
                         [0,6,0,0,0,0,2,8,0],
                         [0,0,0,0,1,9,0,0,5],
                         [0,0,0,0,0,0,0,0,0]]"""

        for row in range(0, 9):
            for column in range(0, 9):
                if self.grid[row][column] == 0:
                    for number in range(1, 10):
                        if self.possible(row, column, number):
                            self.grid[row][column] = number
                            self.solve()
                            self.grid[row][column] = 0

                    return
        print(np.matrix(self.grid))
        input('for more possible solutions : Press Enter')

