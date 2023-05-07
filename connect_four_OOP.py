"""
Author : Nandar Lamin Aye
Solution to : Exercise Performance Task_1 (Four Connect Problem)

Description :

This code file is designed to provide an object-oriented programming (OOP) approach to play the game Connect Four.

The file includes a ConnectFour class which is the main class of the game, and is responsible for managing
the overall game state, including the players, the game board, and the game logic.

At the end of this code file, an instance of the ConnectFour class is created and used to start the game.
"""

import math
from connect_four_AI import minimax
from board import Board


def show_welcome_message():
    print()
    print(f'*-----------------------------------*')
    print("|    Welcome to Connect Four        |")
    print("|-----------------------------------|")
    print("|    Keys Bindings :-               |")
    print("|                                   |")
    print("|    1       : 2 players game       |")
    print("|    2       : Play against AI      |")
    print("|    R or r  : Restart              |")
    print("|    Q or q  : Quit                 |")
    print(f'*-----------------------------------*')


class ConnectFour:

    def __init__(self, row_count=6, column_count=7):
        self._board = Board(row_count, column_count)
        self._current_player = 1
        self._is_playing_with_AI = False
        self._symbols = {0: ' ', 1: 'O', 2: 'X'}
        self._data_matrix = self.__initialize_data_matrix()

    def __initialize_data_matrix(self):
        return [[0 for i in range(self._board.get_column_count())] for j in range(self._board.get_row_count())]

    def ask_game_mode(self):
        mode = int(input("Choose one of the Numbers (1,2) : "))
        while mode <= 0 or mode > 2:
            mode = int(input("Choose one of the Numbers (1,2) : "))

        if mode == 2:
            self._is_playing_with_AI = True
        else:
            self._is_playing_with_AI = False

    def ask_player_move(self):
        action = input("Select the colum(1-7) | Restart (R) | Quit (Q): ")
        if action.isnumeric():
            position = int(action) - 1
            if self._board.is_valid_spot(self._data_matrix, position):
                row = self.get_row(position)
                self._data_matrix[row][position] = self._current_player
                return position
            else:
                print("Sorry! Not a valid Column")
                return self.ask_player_move()
        else:
            if action.upper() == 'R':
                self._current_player = 1
                self._data_matrix = self.__initialize_data_matrix()
                self.start_game()
            elif action.upper() == 'Q':
                quit()
            else:
                print("Sorry! Not a valid Choice")
                return self.ask_player_move()

    def get_row(self, chosen_column):
        for i_row in range(self._board.get_row_count()):
            if self._data_matrix[i_row][chosen_column] == 0:
                return i_row

        return self._board.get_row_count()

    def is_horizontal_win(self, position):
        related_row = self.get_row(position) - 1
        for i_col in range(self._board.get_column_count() - 3):
            if self._data_matrix[related_row][i_col] == self._current_player and \
                    self._data_matrix[related_row][i_col + 1] == self._current_player and \
                    self._data_matrix[related_row][i_col + 2] == self._current_player and \
                    self._data_matrix[related_row][i_col + 3] == self._current_player:
                return True

        return False

    def is_vertical_win(self, position):
        for i_row in reversed(range(self._board.get_row_count() - 3)):
            if self._data_matrix[i_row][position] == self._current_player and \
                    self._data_matrix[i_row + 1][position] == self._current_player and \
                    self._data_matrix[i_row + 2][position] == self._current_player and \
                    self._data_matrix[i_row + 3][position] == self._current_player:
                return True
        return False

    def is_positive_slope_win(self, col_position):
        row_position = self.get_row(col_position) - 1
        diff = col_position - row_position
        continuous_spot = 0

        for i_col in range(self._board.get_column_count()):
            related_row = i_col - diff
            if 0 <= related_row < self._board.get_row_count():
                if self._data_matrix[related_row][i_col] == self._current_player:
                    continuous_spot += 1
                    if continuous_spot >= 4:
                        return True
                else:
                    continuous_spot = 0
        return False

    def is_negative_slope_win(self, col_position):
        row_position = self.get_row(col_position) - 1
        diagonal_sum = col_position + row_position
        continuous_spot = 0

        for i_col in range(self._board.get_column_count()):
            related_row = diagonal_sum - i_col
            if 0 <= related_row < self._board.get_row_count():
                if self._data_matrix[related_row][i_col] == self._current_player:
                    continuous_spot += 1
                    if continuous_spot >= 4:
                        return True
                else:
                    continuous_spot = 0

        return False

    def is_tie(self):
        for i_col in range(self._board.get_column_count()):
            if self._data_matrix[self._board.get_row_count() - 1][i_col] == 0:
                return False
        return True

    def is_wining_state(self, position):
        if self.is_horizontal_win(position) or self.is_vertical_win(position) or self.is_positive_slope_win(
                position) or self.is_negative_slope_win(position):
            return True
        else:
            return False

    def is_terminate_state(self, position):
        if self.is_wining_state(position):
            return [True, 'Win']

        if self.is_tie():
            return [True, 'Tie']

        return [False]

    def ask_for_next_game(self):
        decision = input("Want to play again (P) | Quit (Q) : ")
        if decision.upper() == 'Q':
            quit()
        elif decision.upper() == 'P':
            self._data_matrix = self.__initialize_data_matrix()
            self._current_player = 1
            self.start_game()
        else:
            print("Sorry! Not a valid Input Choose 'P' or 'Q' : ")
            self.ask_for_next_game()

    def show_game_over_message(self, result):
        if result == 'Win':
            if self._is_playing_with_AI and self._current_player == 2:
                print("AI won the game !!!")
            elif self._is_playing_with_AI and self._current_player == 1:
                print("You won the game !!!")
            else:
                print(f'Player {self._current_player} Won the Game!')
        else:
            print(f'The game is Tie')
        self.ask_for_next_game()

    def start_game(self):
        show_welcome_message()
        self.ask_game_mode()
        self._board.show_board(self._data_matrix, self._symbols)
        is_over = False
        if not self._is_playing_with_AI:
            while not is_over:
                print(f"Player {self._current_player}'s turn! ")
                position = self.ask_player_move()
                self._board.show_board(self._data_matrix, self._symbols)
                game_over = self.is_terminate_state(position)
                is_over = game_over[0]
                if not is_over:
                    self._current_player = {1: 2, 2: 1}[self._current_player]

            self.show_game_over_message(game_over[1])
        else:
            while not is_over:
                if self._current_player == 1:
                    print("Your Turn!!")
                    position = self.ask_player_move()
                else:
                    print("AI turn!")
                    position, _ = minimax(self._data_matrix, self._board.get_row_count(),
                                          self._board.get_column_count(),
                                          2, -math.inf, math.inf, True)
                    if self._board.is_valid_spot(self._data_matrix, position):
                        row = self.get_row(position)
                        self._data_matrix[row][position] = self._current_player
                    else:
                        print(f"AI position ({row},{position})")

                self._board.show_board(self._data_matrix, self._symbols)
                game_over = self.is_terminate_state(position)
                is_over = game_over[0]
                if not is_over:
                    self._current_player = {1: 2, 2: 1}[self._current_player]

            self.show_game_over_message(game_over[1])


if __name__ == '__main__':
    connect_four = ConnectFour(6, 7)
    connect_four.start_game()
