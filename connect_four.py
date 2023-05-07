"""
Author : Nandar Lamin Aye
Solution to : Exercise Performance Task_1 (Four Connect Problem)

Description :

This code file is designed to provide a procedural approach to playing the game Connect Four.
The file includes all the necessary functions required for both a two-player mode and an AI mode.

The file can be considered as the main function, as it provides the overall structure and organization for the Connect Four game.
The functions included within the file allow for players to make moves and for the game to respond accordingly.

"""


from connect_four_2players import ask_game_mode, show_board, ask_player_move, is_terminate_state, show_game_over_message,\
    is_valid_spot, get_row
from connect_four_AI import minimax
import math

DEFAULT_ROW = 6
DEFAULT_COL = 7
DEFAULT_DEPTH = 2
symbols = {0: ' ', 1: 'O', 2: 'X'}
data_matrix = [[0 for i in range(DEFAULT_COL)] for j in range(DEFAULT_ROW)]
current_player = 1

while True:
    is_playing_with_AI = ask_game_mode()
    show_board(data_matrix, DEFAULT_ROW, DEFAULT_COL, symbols)

    is_over = False
    if not is_playing_with_AI:
        while not is_over:
            print(f"Player {current_player}'s turn! ")
            col_position, data_matrix = ask_player_move(data_matrix, DEFAULT_ROW, DEFAULT_COL, current_player)
            if type(col_position) is not int:
                if col_position == 'R':
                    current_player = 1
                    data_matrix = [[0 for i in range(DEFAULT_COL)] for j in range(DEFAULT_ROW)]
                    continue
                else:
                    quit()

            show_board(data_matrix, DEFAULT_ROW, DEFAULT_COL, symbols)
            game_over = is_terminate_state(data_matrix, DEFAULT_ROW, DEFAULT_COL, current_player, col_position)
            is_over = game_over[0]
            if not is_over:
                current_player = {1: 2, 2: 1}[current_player]

        show_game_over_message(game_over[1], current_player)

        decision = input("Want to play again (P) | Quit (Q) : ")
        while decision.upper() != 'P' and decision.upper() != 'Q':
            print("Sorry! Not a valid Choice")
            decision = input("Want to play again (P) | Quit (Q) : ")

        if decision.upper() == 'Q':
            quit()
        elif decision.upper() == 'P':
            data_matrix = [[0 for i in range(DEFAULT_COL)] for j in range(DEFAULT_ROW)]
            current_player = 1

    else:
        while not is_over:
            if current_player == 1:
                print("Your Turn!!")
                col_position, data_matrix = ask_player_move(data_matrix, DEFAULT_ROW, DEFAULT_COL, current_player)
                if type(col_position) is not int:
                    if col_position == 'R':
                        current_player = 1
                        data_matrix = [[0 for i in range(DEFAULT_COL)] for j in range(DEFAULT_ROW)]
                        continue
                    else:
                        quit()
            else:
                print("AI turn!")
                col_position, _ = minimax(data_matrix, DEFAULT_ROW, DEFAULT_COL, DEFAULT_DEPTH, -math.inf, math.inf, True)
                if is_valid_spot(data_matrix, DEFAULT_ROW, DEFAULT_COL, col_position):
                    row = get_row(data_matrix, DEFAULT_ROW, col_position)
                    data_matrix[row][col_position] = current_player

            show_board(data_matrix, DEFAULT_ROW, DEFAULT_COL, symbols)
            game_over = is_terminate_state(data_matrix, DEFAULT_ROW, DEFAULT_COL, current_player, col_position)
            is_over = game_over[0]
            if not is_over:
                current_player = {1: 2, 2: 1}[current_player]

        show_game_over_message(game_over[1], current_player, is_playing_with_AI)

        decision = input("Want to play again (P) | Quit (Q) : ")
        while decision.upper() != 'P' and decision.upper() != 'Q':
            print("Sorry! Not a valid Choice")
            decision = input("Want to play again (P) | Quit (Q) : ")

        if decision.upper() == 'P':
            data_matrix = [[0 for i in range(DEFAULT_COL)] for j in range(DEFAULT_ROW)]
            current_player = 1
        else:
            quit()
