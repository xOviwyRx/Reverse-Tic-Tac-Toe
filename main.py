"""
Tic-Tac-Toe game.
"""
import random
import numpy as np

PLAYERS_MARKS = ('X', 'O')


def new_play_board():
    play_board = [['_' for j in range(0, 10)] for i in range(0, 10)]
    return play_board


def display_board(board_list):
    """Prints the game board."""
    s = ''
    for j in range(1, 11):
        s += str(j) + ' '
    print('{:>25}'.format(s))
    i = 1
    for row in board_list:
        s = '|'
        for el in row:
            delimiter = '|'
            s += el + delimiter
        print(f'{i:<3}{s}')
        i += 1


def player_input():
    """Gets player's input string to choose the game mark to play."""
    user_mark = ''
    while user_mark not in ('X', 'O'):
        user_mark = input('Please, choose your marker: X or O: ').upper()

    if user_mark == 'X':
        pc_mark = 'O'
    else:
        pc_mark = 'X'
    dic = {'user_mark': user_mark, 'pc_mark': pc_mark}
    return dic


def place_marker(board, marker, position):
    """Puts a player mark to appropriate position."""
    board[position[0]][position[1]] = marker


def vertical_horizontal_loss(board, mark, horizontal=False):
    i = 0
    while i < 10:
        count = 0
        j = 0
        while j < 10:
            if horizontal:
                cell = board[i][j]
            else:
                cell = board[j][i]
            if cell == mark:
                count += 1
                if count == 5:
                    return True
            else:
                count = 0
            j += 1
        i += 1
    return False


def diagonal_loss(board, mark):
    for i in range(-5, 5):
        ar = np.diagonal(board, i)
        count = 0
        for el in ar:
            if el == mark:
                count += 1
                if count == 5:
                    return True
            else:
                count = 0
    return False


def loss_check(board, mark):
    """Returns boolean value whether the player loose the game."""

    if vertical_horizontal_loss(board, mark) or vertical_horizontal_loss(board, mark, True) or \
            diagonal_loss(board, mark) or diagonal_loss(np.fliplr(board), mark):
        return True
    return False


def get_position_tuple(position):
    """Convert position from '0-99' to [0-9][0-9]"""
    i = position // 10
    j = position % 10
    position_tuple = (i, j)
    return position_tuple


def choose_first(players):
    """Randomly returns the player's mark that goes first."""
    rand = random.choice((0, 1))
    if rand == 0:
        return players['user_mark']
    else:
        return players['pc_mark']


def space_check(board, position):
    """Returns boolean value whether the cell is free or not."""
    return board[position[0]][position[1]] not in PLAYERS_MARKS


def get_marks_count_around(x, y, board, mark, dir_x, dir_y):
    """Gets count of marks on selected direction around position(x,y)"""
    x = x + dir_x
    y = y + dir_y
    count = 0
    while (x < 10) and (y < 10) and (x >= 0) and (y >= 0) and (board[x][y] == mark):
        count += 1
        x = x + dir_x
        y = y + dir_y
    return count


def get_max_marks_count_around(position_tuple, board, mark):
    """Gets maximum count of marks around position_tuple"""
    x = position_tuple[0]
    y = position_tuple[1]
    counts = [get_marks_count_around(x, y, board, mark, 1, 0) + get_marks_count_around(x, y, board, mark, -1, 0),
              get_marks_count_around(x, y, board, mark, 0, -1) + get_marks_count_around(x, y, board, mark, 0, 1),
              get_marks_count_around(x, y, board, mark, 1, 1) + get_marks_count_around(x, y, board, mark, -1, -1),
              get_marks_count_around(x, y, board, mark, 1, -1) + get_marks_count_around(x, y, board, mark, -1, 1)]
    return max(counts)


def get_unchecked_position(checked_positions, board):
    """Gets random unchecked position"""
    while True:
        position = (random.randint(0, 9), random.randint(0, 9))
        if (position not in checked_positions) and (space_check(board, position)):
            return position


def pc_choice(board, mark, len_free_positions, current_min_count_around):
    """Do PC choice based on minimum count of PC marks around possible position"""
    checked_positions = []

    count = 5
    while count != current_min_count_around and len(checked_positions) != len_free_positions:
        position_tuple = get_unchecked_position(checked_positions, board)
        checked_positions.append(position_tuple)
        max_count_around = get_max_marks_count_around(position_tuple, board, mark)
        if max_count_around <= count:
            choice = {'position_tuple': position_tuple, 'max_count_around': max_count_around}
            count = max_count_around
    return choice


def player_choice(board):
    """Gets player's next position and check if it's appropriate to play."""
    position = (-1, -1)

    while True:
        position_list = \
            list(input(f'Choose your next position (2 numbers with space) from 1 to 10: ').split())
        if len(position_list) < 2:
            print("Incorrect input. Input 2 numbers with space from 1 to 10.")
            continue
        try:
            position = (int(position_list[0]) - 1, int(position_list[1]) - 1)
        except ValueError as exc:
            print(f'Incorrect input. Numbers should be integer')
            continue
        if position[0] not in [num for num in range(0, 10)] or \
                position[1] not in [num for num in range(0, 10)]:
            print("Incorrect input. Numbers should be from 1 to 10.")
        elif space_check(board, position):
            return position
        else:
            print("Position is busy.")


def replay():
    """Asks the players to play again."""
    decision = ''
    while decision not in ('y', 'n'):
        decision = input('Would you like to play again? Type "y" or "n"').lower()

    return decision == 'y'


def clear_screen():
    """Clears the game screen via adding new rows."""
    print('\n' * 100)


def switch_player(mark):
    """Switches player's marks to play next turn."""
    return 'O' if mark == 'X' else 'X'


def check_game_finish(board, mark, player_marks, amount_free_positions):
    """Return boolean value is the game finished or not."""
    if loss_check(board, mark):
        if player_marks['user_mark'] == mark:
            print('PC is WIN!')
        else:
            print('You WIN! Congratulations!!!')
        return True

    if amount_free_positions == 0:
        print('The game ended in a draw.')
        return True

    return False


def init_new_game():
    """Initialize new game"""
    global play_board, player_marks, current_player_mark, amount_free_positions, min_pc_around
    play_board = new_play_board()
    player_marks = player_input()
    current_player_mark = choose_first(player_marks)
    amount_free_positions = 100
    min_pc_around = 0
    if current_player_mark == player_marks['user_mark']:
        print(f'You are go first!')
    else:
        print(f'PC goes first.')


play_board = []
player_marks = {}
current_player_mark = ''
amount_free_positions = min_pc_around = 0

print('Welcome to Tic Tac Toe!')
init_new_game()

while True:
    if current_player_mark == player_marks['user_mark']:
        display_board(play_board)
        player_position = False
        while not player_position:
            player_position = player_choice(play_board)
    else:
        dic_pc_position = pc_choice(play_board, current_player_mark, amount_free_positions, min_pc_around)
        if dic_pc_position['max_count_around'] > min_pc_around:
            min_pc_around = dic_pc_position['max_count_around']
        player_position = dic_pc_position['position_tuple']
    place_marker(play_board, current_player_mark, player_position)
    amount_free_positions -= 1
    if check_game_finish(play_board, current_player_mark, player_marks, amount_free_positions):
        display_board(play_board)
        if not replay():
            break
        else:
            init_new_game()
    else:
        current_player_mark = switch_player(current_player_mark)
