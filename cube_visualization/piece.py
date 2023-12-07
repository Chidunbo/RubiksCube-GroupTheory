import numpy as np
from OpenGL.GL import *
import math

vertices = [(-1, -1, -1), (1, -1, -1), (1, 1, -1), (-1, 1, -1),
            (-1, -1, 1), (1, -1, 1), (1, 1, 1), (-1, 1, 1)]
edges = [(0, 1), (1, 2), (2, 3), (3, 0), (4, 5), (5, 6),
         (6, 7), (7, 4), (0, 4), (1, 5), (2, 6), (3, 7)]
surfaces = [(0, 1, 2, 3), (5, 4, 7, 6), (4, 0, 3, 7), (1, 5, 6, 2),
            (4, 5, 1, 0), (3, 2, 6, 7)]
colors = [
    (0, 0, 1),  # blue
    (0, 1, 0),  # green
    (1, 0.5, 0.1),  # orange
    (1, 0, 0),  # red
    (1, 1, 0),  # yellow
    (1, 1, 1)]  # white


class Piece:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.len = 0.5
        self.position = np.identity(3, int)

    # multiplies current position by a rotation matrix to move and rotate the
    # piece
    def rotate_x(self, direction):
        rotation = np.matrix([[1, 0, 0],
                              [0, math.cos(direction), -math.sin(direction)],
                              [0, math.sin(direction), math.cos(direction)]])
        self.position = self.position * rotation

    def rotate_y(self, direction):
        rotation = np.matrix([[math.cos(direction), 0, math.sin(direction)],
                              [0, 1, 0],
                              [-math.sin(direction), 0, math.cos(direction)]])
        self.position = self.position * rotation

    def rotate_z(self, direction):
        rotation = np.matrix([[math.cos(direction), -math.sin(direction), 0],
                              [math.sin(direction), math.cos(direction), 0],
                              [0, 0, 1]])
        self.position = self.position * rotation

    def round(self):
        self.position = self.position.round()

    def get_location(self):
        curr = np.matrix([self.x, self.y, self.z]) * self.position
        return curr.item(0), curr.item(1), curr.item(2)

    # returns a 4x4 matrix of current rotation that can be passed into
    # glMultMatrixf
    def get_matrix(self):
        dim = np.size(self.position, 1)
        matrix_array = np.array(self.position)
        matrix_array = matrix_array.flatten()
        gl_matrix = []
        for i in range(np.size(matrix_array)):
            gl_matrix.append(matrix_array[i])
            if i % dim == 2:
                gl_matrix.append(0)
        gl_matrix.extend([0, 0, 0, 1])
        return gl_matrix

    # draws each individual piece
    def draw(self):
        glEnable(GL_DEPTH_TEST)

        glEnable(GL_POLYGON_OFFSET_FILL)
        glPolygonOffset(1.0, 1.0)

        # rotates the piece accordingly
        glPushMatrix()
        glMultMatrixf(self.get_matrix())

        glTranslatef(self.x, self.y, self.z)
        glScalef(self.len, self.len, self.len)

        # draws edges
        glLineWidth(5)
        glColor3fv((0, 0, 0))
        glBegin(GL_LINES)
        for e in edges:
            glVertex3fv(vertices[e[0]])
            glVertex3fv(vertices[e[1]])
        glEnd()

        # draws surfaces
        glBegin(GL_QUADS)
        for i in range(len(surfaces)):
            glColor3fv(colors[i])
            for j in surfaces[i]:
                glVertex3fv(vertices[j])
        glEnd()

        glPopMatrix()
