import tkinter as tk
from minmax import *
from const import *


class Board(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.canvas = tk.Canvas(self, bg="black", height=Const.HEIGHT, width=Const.WIDTH)
        self.canvas.pack()
        self.coord_arr = [[(Const.WIDTH / 8 * i, Const.HEIGHT / 8 * j) for i in range(8)] for j in range(8)]
        self.pieces = [[None] * 8 for i in range(8)]
        self.dots = []
        self.is_red_turn = True
        self.chosen_piece = None

        for i in range(3):
            for j in range(8):
                if (i + j) % 2:
                    self.pieces[i][j] = Piece(False)
        for i in range(5, 8):
            for j in range(8):
                if (i + j) % 2:
                    self.pieces[i][j] = Piece(True)
        self.on_every_move()

    def on_every_move(self):
        if self.chosen_piece is None:
            self.canvas.delete("All")
            self.draw_board()
        all_captures = find_all_captures(self.is_red_turn, self.pieces)
        all_moves = find_all_moves(self.is_red_turn, self.pieces)
        if len(all_captures):
            all_moves = dict()

        if self.is_red_turn:
            self.bind("<Button-1>", self.choose_piece)
            if self.chosen_piece not in all_moves.keys() and self.chosen_piece not in all_captures.keys():
                self.chosen_piece = None
            if self.chosen_piece is not None and self.pieces[self.chosen_piece[0]][self.chosen_piece[1]] is not None:
                if len(all_captures) == 0:
                    if len(all_moves):
                        self.draw_dots(self.chosen_piece[0], self.chosen_piece[1], all_moves)
                else:
                    self.draw_dots(self.chosen_piece[0], self.chosen_piece[1], all_captures)
                if self.pieces[self.chosen_piece[0]][self.chosen_piece[1]] is not None:
                    self.bind("<Button-1>",
                              lambda x: self.move(self.click_coords(x), all_moves, all_captures))
        else:
            self.unbind("<Button-1>")
            best_move = minmax(self.pieces)
            self.chosen_piece = []
            for key in best_move.keys():
                self.chosen_piece += key
                destination = best_move[key]
            if len(all_captures):
                all_moves = []
            print(all_captures, all_moves)
            self.move(destination, all_moves, all_captures)
            self.is_red_turn = True
            self.on_every_move()

    def clear_dots(self):
        for dot in self.dots:
            self.canvas.delete(dot)
        self.dots = []

    def click_coords(self, event):
        for i in range(8):
            for j in range(8):
                if self.coord_arr[i][j][0] <= event.x <= self.coord_arr[i][j][0] + Const.SQUARE_SIZE \
                        and self.coord_arr[i][j][1] <= event.y <= self.coord_arr[i][j][1] + Const.SQUARE_SIZE:
                    return i, j
        return None

    def draw_dots(self, x, y, moves):
        empty_space = 0.4
        coords_left_up = self.coord_arr[x][y][0] + empty_space * Const.SQUARE_SIZE, \
                         self.coord_arr[x][y][1] + empty_space * Const.SQUARE_SIZE
        coords_right_down = self.coord_arr[x][y][0] + (1 - empty_space) * Const.SQUARE_SIZE, \
                            self.coord_arr[x][y][1] + (1 - empty_space) * Const.SQUARE_SIZE
        dot = self.canvas.create_oval(coords_left_up, coords_right_down, fill="black")
        self.dots.append(dot)
        for i in moves[x, y]:
            coords_left_up = self.coord_arr[i[0]][i[1]][0] + empty_space * Const.SQUARE_SIZE, \
                             self.coord_arr[i[0]][i[1]][1] + empty_space * Const.SQUARE_SIZE
            coords_right_down = self.coord_arr[i[0]][i[1]][0] + (1 - empty_space) * Const.SQUARE_SIZE, \
                                self.coord_arr[i[0]][i[1]][1] + (1 - empty_space) * Const.SQUARE_SIZE
            dot = self.canvas.create_oval(coords_left_up, coords_right_down, fill="yellow")
        self.dots.append(dot)

    def draw_board(self):
        empty_space = 0.1
        for i in range(8):
            for j in range(8):

                if (i + j) % 2:
                    color = "brown"
                else:
                    color = "white"
                coords_left_up = self.coord_arr[i][j][0], self.coord_arr[i][j][1]
                coords_right_down = self.coord_arr[i][j][0] + Const.SQUARE_SIZE, self.coord_arr[i][j][
                    1] + Const.SQUARE_SIZE
                self.canvas.create_rectangle(coords_left_up, coords_right_down, fill=color)

                if self.pieces[i][j] is not None:
                    coords_left_up = self.coord_arr[i][j][0] + empty_space * Const.SQUARE_SIZE, \
                                     self.coord_arr[i][j][1] + empty_space * Const.SQUARE_SIZE
                    coords_right_down = self.coord_arr[i][j][0] + (1 - empty_space) * Const.SQUARE_SIZE, \
                                        self.coord_arr[i][j][1] + (1 - empty_space) * Const.SQUARE_SIZE
                    if self.pieces[i][j].is_red:
                        color = "red"
                    else:
                        color = "blue"

                    self.canvas.create_oval(coords_left_up, coords_right_down, fill=color)

    def choose_piece(self, event):
        i, j = self.click_coords(event)
        self.chosen_piece = (i, j)
        self.on_every_move()
        # if self.pieces[i][j] is not None:
        #    moves, captures = self.find_moves(i, j), self.find_captures(i, j)
        #    self.bind("<Button-1>", lambda x: self.move(self.click_coords(x), moves, captures, [i, j]))

    def move(self, destination, moves, captures):
        x, y = destination
        moved = 0
        print(" MOVES ", moves)
        if len(moves):
            if (x, y) in moves[(self.chosen_piece[0], self.chosen_piece[1])]:
                self.pieces[x][y] = self.pieces[self.chosen_piece[0]][self.chosen_piece[1]]
                self.pieces[self.chosen_piece[0]][self.chosen_piece[1]] = None
                moved = 1
        if len(captures):
            if (x, y) in captures[(self.chosen_piece[0], self.chosen_piece[1])]:
                self.pieces[x][y] = self.pieces[self.chosen_piece[0]][self.chosen_piece[1]]
                self.pieces[self.chosen_piece[0]][self.chosen_piece[1]] = None
                self.pieces[(self.chosen_piece[0] + x) // 2][(self.chosen_piece[1] + y) // 2] = None
                moved = 1
        if moved:
            self.is_red_turn = not self.is_red_turn
            if x == 0 and self.pieces[x][y].is_red == True:
                self.pieces[x][y].king = True
            if x == 7 and self.pieces[x][y].is_red == False:
                self.pieces[x][y].king = True
        else:
            self.bind("<Button-1>", self.choose_piece)
        self.chosen_piece = None
        self.on_every_move()


def move2(chosen_piece, pieces, destination, moves, captures):
    x, y = destination
    moved = 0
    if len(moves):
        if (x, y) in moves[(chosen_piece[0], chosen_piece[1])]:
            pieces[x][y] = pieces[chosen_piece[0]][chosen_piece[1]]
            pieces[chosen_piece[0]][chosen_piece[1]] = None
            moved = 1
    if len(captures):
        if (x, y) in captures[(chosen_piece[0], chosen_piece[1])]:
            pieces[x][y] = pieces[chosen_piece[0]][chosen_piece[1]]
            pieces[chosen_piece[0]][chosen_piece[1]] = None
            pieces[(chosen_piece[0] + x) // 2][(chosen_piece[1] + y) // 2] = None
            moved = 1
    if moved:
        # is_red_turn = not is_red_turn
        if x == 0 and pieces[x][y].is_red == True:
            pieces[x][y].king = True
        if x == 7 and pieces[x][y].is_red == False:
            pieces[x][y].king = True
    return pieces


def find_all_captures(is_red_color, pieces):
    all_captures = dict()
    for i in range(8):
        for j in range(8):
            if pieces[i][j] is not None and is_red_color == pieces[i][j].is_red:
                possible_captures = find_captures(i, j, pieces)
                if len(possible_captures):
                    all_captures[(i, j)] = possible_captures
    return all_captures


def find_all_moves(is_red_color, pieces):
    all_moves = dict()
    for i in range(8):
        for j in range(8):
            if pieces[i][j] is not None and is_red_color == pieces[i][j].is_red:
                possible_moves = find_moves(i, j, pieces)
                if len(possible_moves):
                    all_moves[(i, j)] = possible_moves
    return all_moves


def find_captures(x, y, pieces):
    if pieces[x][y] is not None:
        a = find_captures_in_direction(x, y, 1, 1, pieces)
        b = find_captures_in_direction(x, y, -1, 1, pieces)
        c = find_captures_in_direction(x, y, 1, -1, pieces)
        d = find_captures_in_direction(x, y, -1, -1, pieces)
        captures = a + b + c + d
        return captures
    else:
        return None


def find_captures_in_direction(x, y, dir_x, dir_y, pieces):
    range_of_piece = 1
    if pieces[x][y].king:
        range_of_piece = 6
    for i in range(1, range_of_piece + 1):
        if not (0 < x + dir_x * i < 7) or not (0 < y + dir_y * i < 7):
            return []
        if pieces[x + dir_x * i][y + dir_y * i] is not None and pieces[x + dir_x * i][y + dir_y * i].is_red != \
                pieces[x][y].is_red:
            if pieces[x + dir_x * i + dir_x][y + dir_y * i + dir_y] is None:
                return [(x + dir_x * i + dir_x, y + dir_y * i + dir_y)]
            else:
                return []
    return []
    ## napisać sprawdzanie bicia


def find_moves(x, y, pieces):
    if pieces[x][y] is not None:
        dir_x = 1 if not pieces[x][y].is_red else -1
        a = find_moves_in_direction(x, y, dir_x, 1, pieces)
        b = find_moves_in_direction(x, y, dir_x, -1, pieces)
        moves = a + b
        return moves
    else:
        return None


def find_moves_in_direction(x, y, dir_x, dir_y, pieces):
    range_of_piece = 1
    moves = []
    if pieces[x][y].king:
        range_of_piece = 6
    for i in range(1, range_of_piece + 1):
        if not (0 <= x + dir_x * i <= 7) or not (0 <= y + dir_y * i <= 7):
            return []
        if pieces[x + dir_x * i][y + dir_y * i] is None:
            moves.append((x + dir_x * i, y + dir_y * i))
        else:
            return moves
    return moves


class Piece:
    def __init__(self, is_red, king=False):
        self.is_red = is_red
        self.king = king


def main():
    pass


if __name__ == '__main__':
    main()
    app = Board()
    app.mainloop()
