"""
Author : Nandar Lamin Aye (Credit to KeithGalli)
Solution to : Exercise Performance Task_1 (Four Connect Problem)

Description : 

This file is all credit to connect4_with_ai.py from Connect 4 Python repository by KeithGalli which is available on Github
Link : https://github.com/KeithGalli/Connect4-Python/tree/503c0b4807001e7ea43a039cb234a4e55c4b226c

Minimax Algorithm is used for the AI play, which is a well-known recursion algorithm used in decision-making programs. 
The scoring function has been adjusted along with the recursive depth to improve the AI's play.

The main function of this file is minimax(), and the other functions are helper functions
that assist with the implementation of the minimax() function. Calling minimax() is sufficient to get the AI's move.

The original implementation of this file uses the 'numpy' library, however, for this assignment, 
it has been modified to use only 2D arrays without the use of numpy.

"""

import math
import random

EMPTY = 0
ROW_COUNT = None
COL_COUNT = None
PLAYER_PIECE = 1
AI_PIECE = 2
WINDOW_LENGTH = 4
HIGHEST_SCORE = 100000000000000
LOWEST_SCORE = -10000000000000


def winning_move(board, piece):
    # Check horizontal locations for win
    for c in range(COL_COUNT - 3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c + 1] == piece and board[r][c + 2] == piece and \
                    board[r][c + 3] == piece:
                return True

    # Check vertical locations for win
    for c in range(COL_COUNT):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r + 1][c] == piece and board[r + 2][c] == piece and \
                    board[r + 3][c] == piece:
                return True

    # Check positively sloped diagonals
    for c in range(COL_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r + 1][c + 1] == piece and board[r + 2][c + 2] == piece and \
                    board[r + 3][c + 3] == piece:
                return True

    # Check negatively sloped diagonals
    for c in range(COL_COUNT - 3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == piece and board[r - 1][c + 1] == piece and board[r - 2][c + 2] == piece and \
                    board[r - 3][c + 3] == piece:
                return True


def is_valid_location(board, col):
    return board[ROW_COUNT - 1][col] == 0


def get_valid_locations(board):
    valid_locations = []
    for col in range(COL_COUNT):
        if is_valid_location(board, col):
            valid_locations.append(col)
    return valid_locations


def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r


def is_terminal_node(board):
    return winning_move(board, PLAYER_PIECE) or winning_move(board, AI_PIECE) or len(get_valid_locations(board)) == 0


def score_position(board, piece):
    score = 0
    center_array = [int(i) for i in [board[i][COL_COUNT // 2] for i in range(ROW_COUNT)]]

    center_count = sum([i == piece for i in center_array])
    score += center_count * 3

    for r in range(ROW_COUNT):
        row_array = [int(i) for i in board[r]]

        for c in range(COL_COUNT - 3):
            window = row_array[c:c + WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    for c in range(COL_COUNT):
        col_array = [int(i) for i in [board[i][c] for i in range(ROW_COUNT)]]

        for r in range(ROW_COUNT - 3):
            window = col_array[r:r + WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    for r in range(ROW_COUNT - 3):
        for c in range(COL_COUNT - 3):
            window = [board[r + i][c + i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    for r in range(ROW_COUNT - 3):
        for c in range(COL_COUNT - 3):
            window = [board[r + 3 - i][c + i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    return score


def evaluate_window(window, piece):
    score = 0
    opp_piece = PLAYER_PIECE
    if piece == PLAYER_PIECE:
        opp_piece = AI_PIECE

    if sum([i == piece for i in window]) == 4:
        score += 100
    elif sum([i == piece for i in window]) == 3 and sum([i == EMPTY for i in window]) == 1:
        score += 5
    elif sum([i == piece for i in window]) == 2 and sum([i == EMPTY for i in window]) == 2:
        score += 2
    if sum([i == opp_piece for i in window]) == 3 and sum([i == EMPTY for i in window]) == 1:
        score -= 50

    return score


def drop_piece(board, row, col, piece):
    board[row][col] = piece


def copy_data_matrix(board):
    board_copy = [[0 for i in range(len(board[0]))] for j in range(len(board))]
    for i_row in range(len(board)):
        for j_col in range(len(board[0])):
            board_copy[i_row][j_col] = board[i_row][j_col]

    return board_copy


def minimax(board, row_count, col_count, depth, alpha, beta, maximizingPlayer):

    global ROW_COUNT
    global COL_COUNT
    ROW_COUNT = row_count
    COL_COUNT = col_count

    valid_locations = get_valid_locations(board)
    is_terminal = is_terminal_node(board)
    if depth == 0 or is_terminal:
        if is_terminal:
            if winning_move(board, AI_PIECE):
                return None, HIGHEST_SCORE
            elif winning_move(board, PLAYER_PIECE):
                return None, HIGHEST_SCORE
            else:  # Game is over, no more valid moves
                return None, 0
        else:  # Depth is zero
            return None, score_position(board, AI_PIECE)

    if maximizingPlayer:
        value = -math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = copy_data_matrix(board)
            drop_piece(b_copy, row, col, AI_PIECE)
            new_score = minimax(b_copy, row_count, col_count, depth - 1, alpha, beta, False)[1]
            if new_score > value:
                value = new_score
                column = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return column, value
    else:  # Minimizing player
        value = math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = copy_data_matrix(board)
            drop_piece(b_copy, row, col, PLAYER_PIECE)
            new_score = minimax(b_copy, row_count, col_count, depth - 1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                column = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return column, value