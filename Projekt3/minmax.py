from const import *
from main import find_all_moves, find_all_captures, move2
from copy import deepcopy


def evaluate_board(pieces):
    red_pieces = count_points(pieces, True)
    blue_pieces = count_points(pieces, False)
    return red_pieces - blue_pieces


def count_points(pieces, red):
    points = 0
    for i in range(8):
        for j in range(8):
            if pieces[i][j] is not None and pieces[i][j].is_red == red:
                points += 1
                if 0 < j < 7:
                    points += 1
                if pieces[i][j].king:
                    points += 4
                elif 2 < i < 5:
                    points += 1
                elif i == 2 and red:
                    points += 2
                elif i == 5 and not red:
                    points += 2
                elif i == 1 and red:
                    points += 3
                elif i == 6 and not red:
                    points += 3

    return points


def minmax(pieces):
    depth = Const.MAX_DEPTH
    best_move = None
    while best_move is None and depth > 0:
        best_move = min_move(pieces, depth, None)[0]
        depth -= 1
    return best_move

def max_move(pieces, depth, best_move):
    return max_min_board(pieces, depth - 1, float('inf'), best_move)


def min_move(pieces, depth, best_move):
    return max_min_board(pieces, depth - 1, float('-inf'), best_move)


def max_min_board(pieces_original, depth, best_value, best_move):
    if depth <= 0:
        return best_move, evaluate_board(pieces_original)
    if best_value == float('-inf'):
        moves = []
        captures = find_all_captures(False, pieces_original)
        if len(captures) == 0:
            moves = find_all_moves(False, pieces_original)
        if len(moves):
            for key in moves.keys():
                for the_move in moves[key]:

                    pieces = deepcopy(pieces_original)
                    pieces = move2(key, pieces, the_move, moves, captures)
                    value = min_move(pieces, depth, best_move)[1]
                    if value > best_value:
                        best_value = value
                        best_move = {key: the_move}
        else:
            for key in captures.keys():
                for the_move in captures[key]:
                    pieces = deepcopy(pieces_original)
                    pieces = move2(key, pieces, the_move, moves, captures)
                    value = min_move(pieces, depth, best_move)[1]
                    if value > best_value:
                        best_value = value
                        best_move = {key: the_move}
        return best_move, evaluate_board(pieces_original)

    elif best_value == float('inf'):
        moves = []
        captures = find_all_captures(True, pieces_original)
        if len(captures) == 0:
            moves = find_all_moves(True, pieces_original)
        if len(moves):
            for key in moves.keys():
                for the_move in moves[key]:
                    pieces = deepcopy(pieces_original)
                    pieces = move2(key, pieces, the_move, moves, captures)
                    value = min_move(pieces, depth, {key: the_move})[1]
                    if value < best_value:
                        best_value = value
                        best_move = {key: the_move}
        else:
            for key in captures.keys():
                for the_move in captures[key]:
                    pieces = deepcopy(pieces_original)
                    pieces = move2(key, pieces, the_move, moves, captures)
                    value = min_move(pieces, depth, {key: the_move})[1]
                    if value < best_value:
                        best_value = value
                        best_move = {key: the_move}
