from piece import Piece
import math


class Cube:
    def __init__(self, lo, hi):
        self.pieces = []
        self.scramble = []
        self.generate_cube(lo, hi)

    # Creates a 3x3 array of piece objects
    def generate_cube(self, lo, hi):
        for x in range(lo, hi):
            for y in range(lo, hi):
                for z in range(lo, hi):
                    self.pieces.append(Piece(x, y, z))

    def get_cube(self):
        return self.pieces

    # Rotates all cubes on the x axis
    def turn_x(self, layer, direction):
        for piece in self.pieces:
            if piece.get_location()[0] == layer:
                piece.rotate_x(direction)

    def turn_y(self, layer, direction):
        for piece in self.pieces:
            if piece.get_location()[1] == layer:
                piece.rotate_y(direction)

    def turn_z(self, layer, direction):
        for piece in self.pieces:
            if piece.get_location()[2] == layer:
                piece.rotate_z(direction)

    # adds array of moves to scramble
    def add_moves(self, moves):
        self.scramble.extend(moves)

    # returns last move in scramble
    def get_scramble(self):
        if len(self.scramble) == 0:
            return None
        return self.scramble.pop()

    # draws each piece in cube
    def show(self):
        for piece in self.pieces:
            piece.draw()

    def round(self):
        for piece in self.pieces:
            piece.round()

