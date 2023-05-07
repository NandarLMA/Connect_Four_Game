"""
Author : Nandar Lamin Aye
Solution to : Exercise Performance Task_1 (Four Connect Problem)

Description :

This code file includes the implementation of a board class that is specifically designed to be used in the Connect Four game.

The board class provides a framework for representing the game board, and includes functions for displaying and querying
the state of the board.

"""


class Board:
    def __init__(self, row_count, col_count):
        self._row_count = row_count
        self._column_count = col_count

    def print_row_seperator(self):
        for count in range(self._column_count):
            print(f'*------', end='*')
        print()

    def show_board(self, data_matrix, symbols):
        print()
        for count in range(self._column_count):
            print(f'    {count + 1}', end='\t')

        print()
        self.print_row_seperator()

        for i_row in reversed(range(self._row_count)):
            for j_col in range(self._column_count):
                print(f'|   {symbols[data_matrix[i_row][j_col]]}', end="  |")
            print()
            self.print_row_seperator()

        print()

    def is_valid_spot(self, data_matrix, col_position):
        if 0 <= col_position < self._column_count:
            if data_matrix[self._row_count - 1][col_position] != 0:
                return False
            return True

        return False

    def get_column_count(self):
        return self._column_count

    def get_row_count(self):
        return self._row_count
