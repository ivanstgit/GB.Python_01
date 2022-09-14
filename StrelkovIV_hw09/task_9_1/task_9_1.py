# Создайте программу для игры в "Крестики-нолики"
import random

import emoji as emoji

EMPTY_SYMBOL = " "
HUMAN_SYMBOL = "O"
BOT_SYMBOL = "X"
FIELD_SIZE = 3
PRINT_SYMBOLS = {
    EMPTY_SYMBOL: ' ',
    HUMAN_SYMBOL: ':o:',
    BOT_SYMBOL: ':x:'
    }


def print_field(field: list):
    print("_"*5)
    for line in field:
        print_str = [PRINT_SYMBOLS[cell] for cell in line]

        print(emoji.emojize(" ".join(print_str)))


def check_field_is_full(field: list):
    for line in field:
        for col in line:
            if col == " ":
                return False
    return True


def check_is_win(field: list, player_symbol: str):
    """ Победа? """

    for j in range(FIELD_SIZE):
        result = sum([1 if field[i][j] == player_symbol else 0
                     for i in range(FIELD_SIZE)])
        if result == FIELD_SIZE:
            return True
        result = sum([1 if field[j][i] == player_symbol else 0
                     for i in range(FIELD_SIZE)])
        if result == FIELD_SIZE:
            return True
    result = sum([1 if field[i][i] == player_symbol else 0
                 for i in range(FIELD_SIZE)])
    if result == FIELD_SIZE:
        return True
    result = sum([1 if field[FIELD_SIZE - 1 - i][i] == player_symbol else 0
                 for i in range(FIELD_SIZE)])
    if result == FIELD_SIZE:
        return True

    return False


def get_score_for_line(line: list, player_symbol: str):
    """ Оцениваем линию: чем больше наших и меньше чужих, тем оценка выше"""
    score_increment = 0
    my_cells_cnt = 0
    enemy_cells_cnt = 0

    for cellValue in line:
        if cellValue == player_symbol:
            my_cells_cnt += 1
        else:
            if cellValue != EMPTY_SYMBOL:
                enemy_cells_cnt += 1

    if my_cells_cnt == FIELD_SIZE - 1 and enemy_cells_cnt == 0: # last, max score
        score_increment = 1000
        return score_increment

    if enemy_cells_cnt == FIELD_SIZE - 1 and my_cells_cnt == 0: # big defence score
        score_increment = 900
        return score_increment

    if enemy_cells_cnt == 0: # //mine(*5) or empty (*1)
        score_increment = my_cells_cnt * 5 + (FIELD_SIZE - my_cells_cnt)

    return score_increment


def get_score_for_lines(row, col, player_symbol, field: list):
    """ Оцениваем ячейку по всем линиям, в которые она входит"""
    result = 0

    # о линии  row
    result += get_score_for_line([field[row][i] for i in range(FIELD_SIZE)], player_symbol)

    # по линии col
    result += get_score_for_line([field[i][col] for i in range(FIELD_SIZE)], player_symbol)

     # по диагонали \
    if row == col:
        result += get_score_for_line([field[i][i] for i in range(FIELD_SIZE)], player_symbol)

    # по диагонали /
    if row == (FIELD_SIZE - col - 1):
        result += get_score_for_line([field[FIELD_SIZE - 1 - i][i] for i in range(FIELD_SIZE)], player_symbol)

    return result


game_field = [[EMPTY_SYMBOL, EMPTY_SYMBOL, EMPTY_SYMBOL],
              [EMPTY_SYMBOL, EMPTY_SYMBOL, EMPTY_SYMBOL],
              [EMPTY_SYMBOL, EMPTY_SYMBOL, EMPTY_SYMBOL]]

current_player = random.randint(1, 2)
while not check_field_is_full(game_field):
    print_field(game_field)
    current_symbol = [BOT_SYMBOL, HUMAN_SYMBOL][current_player - 1]

    # игрок - ввод с клавиатуры
    if current_symbol == HUMAN_SYMBOL:
        in_str = input(f"Ход игрока({current_symbol}). Введите через пробел координаты по горизонтали и вертикали:")
        y, x = map(int, in_str.split())
        if game_field[x - 1][y - 1] == EMPTY_SYMBOL:
            game_field[x - 1][y - 1] = current_symbol
            current_player = 3 - current_player
    # ПК - логика вычисления хода
    else:
        max_score = 0
        x, y = -1, -1
        for i in range(FIELD_SIZE):
            for j in range(FIELD_SIZE):
                if game_field[i][j] == EMPTY_SYMBOL:
                    cell_score = get_score_for_lines(i, j, current_symbol, game_field)
                    if cell_score > max_score:
                        max_score = cell_score
                        x, y = i, j
        if 0 <= x < FIELD_SIZE and 0 <= y < FIELD_SIZE:
            game_field[x][y] = current_symbol
            current_player = 3 - current_player
        else:
            print("ups")
            exit(0)

    if check_is_win(game_field, current_symbol):
        print(f"Победа {current_symbol}")
        exit(0)

print(f"Ничья")
