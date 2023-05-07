"""
Author : Nandar Lamin Aye
Solution to : Exercise Performance Task_1 (Four Connect Problem)

Description :

All necessary functions to play a game in 2 players mode are mentioned in this file. UI part such as displaying
welcome message and board status is also included.

All the functions in this code file have been implemented by me.

"""


def print_row_seperator(col_count):
    for count in range(col_count):
        print(f'*------', end='*')
    print()


def show_board(data_matrix, row_count, col_count, symbols):
    for count in range(col_count):
        print(f'    {count + 1}', end='\t')

    print()
    print_row_seperator(col_count)

    for i_row in reversed(range(row_count)):
        for j_col in range(col_count):
            print(f'|   {symbols[data_matrix[i_row][j_col]]}', end="  |")
        print()
        print_row_seperator(col_count)
    print()


def ask_game_mode():
    print()
    print(f'*-----------------------------------*')
    print("|    Welcome to Connect Four        |")
    print("|-----------------------------------|")
    print("|    Keys Bindings :-               |")
    print("|                                   |")
    print("|    1       : 2 players game       |")
    print("|    2       : Against AI           |")
    print("|    R or r  : Restart              |")
    print("|    Q or q  : Quit                 |")
    print(f'*-----------------------------------*')

    partner = int(input("Choose one of the Numbers (1,2) : "))
    while partner <= 0 or partner > 2:
        partner = int(input("Choose one of the Numbers (1,2) : "))

    if partner == 2:
        return True

    return False


def show_game_over_message(result, winner, is_playing_with_AI=False):
    if result == 'Win':
        if is_playing_with_AI and winner == 2:
            print("AI won the game !!!")
        elif is_playing_with_AI and winner == 1:
            print("You won the game !!!")
        else:
            print(f'Player {winner} Won the Game!')
    else:
        print(f'The game is Tie')


def get_row(data_matrix, row_count, chosen_column):
    for i_row in range(row_count):
        if data_matrix[i_row][chosen_column] == 0:
            return i_row

    return row_count


def is_valid_spot(data_matrix, row_count, col_count, col_position):
    if 0 <= col_position < col_count:
        if data_matrix[row_count - 1][col_position] != 0:
            return False
        return True
    else:
        return False


def ask_player_move(data_matrix, row_count, col_count, current_player):
    user_choice = input("Select the colum(1-7) | Restart (R) | Quit (Q): ")
    if user_choice.isnumeric():
        col_position = int(user_choice) - 1
        if is_valid_spot(data_matrix, row_count, col_count, col_position):
            row = get_row(data_matrix, row_count, col_position)
            data_matrix[row][col_position] = current_player
            return col_position, data_matrix
        else:
            print("Sorry! Not a valid Column")
            return ask_player_move(data_matrix, row_count, col_count, current_player)
    else:
        if user_choice.upper() == 'R' or user_choice.upper() == 'Q':
            return user_choice, data_matrix
        else:
            print("Sorry! Not a valid Choice")
            return ask_player_move(data_matrix, row_count, col_count, current_player)


def is_horizontal_win(data_matrix, row_count, col_count, current_player, col_position):
    related_row = get_row(data_matrix, row_count, col_position) - 1
    for i_col in range(col_count - 3):
        if data_matrix[related_row][i_col] == current_player and \
                data_matrix[related_row][i_col + 1] == current_player and \
                data_matrix[related_row][i_col + 2] == current_player and \
                data_matrix[related_row][i_col + 3] == current_player:
            return True

    return False


def is_vertical_win(data_matrix, row_count, current_player, col_position):
    for i_row in reversed(range(row_count - 3)):
        if data_matrix[i_row][col_position] == current_player and \
                data_matrix[i_row + 1][col_position] == current_player and \
                data_matrix[i_row + 2][col_position] == current_player and \
                data_matrix[i_row + 3][col_position] == current_player:
            return True
    return False


def is_positive_slope_win(data_matrix, row_count, col_count, current_player, col_position):
    row_position = get_row(data_matrix, row_count, col_position) - 1
    diff = col_position - row_position
    continuous_spot = 0
    for i_col in range(col_count):
        related_row = i_col - diff
        if 0 <= related_row < row_count:
            if data_matrix[related_row][i_col] == current_player:
                continuous_spot += 1
                if continuous_spot >= 4:
                    return True
            else:
                continuous_spot = 0
    return False


def is_negative_slope_win(data_matrix, row_count, col_count, current_player, col_position):
    row_position = get_row(data_matrix, row_count, col_position) - 1
    diagonal_sum = col_position + row_position
    continuous_spot = 0

    for i_col in range(col_count):
        related_row = diagonal_sum - i_col
        if 0 <= related_row < row_count:
            if data_matrix[related_row][i_col] == current_player:
                continuous_spot += 1
                if continuous_spot >= 4:
                    return True
            else:
                continuous_spot = 0

    return False


def is_tie(data_matrix, col_count, row_count):
    for i_col in range(col_count):
        if data_matrix[row_count - 1][i_col] == 0:
            return False
    return True


def is_terminate_state(data_matrix, row_count, col_count, current_player, col_position):
    if is_horizontal_win(data_matrix, row_count, col_count, current_player, col_position) or \
            is_vertical_win(data_matrix, row_count, current_player, col_position) or \
            is_positive_slope_win(data_matrix, row_count, col_count, current_player, col_position) or \
            is_negative_slope_win(data_matrix, row_count, col_count, current_player, col_position):
        return [True, 'Win']

    if is_tie(data_matrix, col_count, row_count):
        return [True, 'Tie']

    return [False]
