import time
import math
import random

import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from cube import Cube

display_width = 1200
display_height = 1000
# allowable moves user can enter
MOVES = ['R', 'R\'', 'L', 'L\'', 'U', 'U\'', 'D', 'D\'', 'F', 'F\'', 'B', 'B\'']


class Visualizer:
    def __init__(self):
        self.cube = Cube(-1, 2)
        self.angle_x = 0
        self.angle_y = 0
        self.clock = pygame.time.Clock()
        self.gameDisplay = pygame.display.set_mode \
            ((display_width, display_height), DOUBLEBUF | OPENGL)
        open('output.txt', 'w').close()

    # starting screen that displays rotating rubik's cube
    def start(self):
        pygame.init()

        gluPerspective(45, (display_width / display_height), 0.1, 50)
        glClearColor(0.6, 0.6, 0.6, 0)
        glTranslatef(0.0, 0.0, -20)
        glRotatef(45, 1, 1, 0)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                if event.type == pygame.KEYDOWN or \
                        event.type == pygame.MOUSEBUTTONDOWN:
                    self.visualize_cube()

            glRotatef(5, 3, 3, 0)
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            self.cube.show()
            pygame.display.flip()
            pygame.time.wait(10)

    # renders and visualizes the cube
    def visualize_cube(self):
        self.read_input()
        pygame.init()

        glMatrixMode(GL_PROJECTION)
        gluPerspective(45, (display_width / display_height), 0.1, 50)

        while True:
            # if cube is currently being scrambled, curr move returns the next move
            curr_move = self.cube.get_scramble()
            if curr_move is not None:
                self.turn_cube(curr_move, True)
            else:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()

                    # takes user input and turns the cube
                    if event.type == pygame.KEYDOWN:
                        keys = pygame.key.get_pressed()
                        shift = keys[pygame.K_RSHIFT] or keys[pygame.K_LSHIFT]
                        if shift:
                            if event.key == pygame.K_r:
                                self.turn_cube('R\'', True)
                            elif event.key == pygame.K_l:
                                self.turn_cube('L\'', True)
                            elif event.key == pygame.K_u:
                                self.turn_cube('U\'', True)
                            elif event.key == pygame.K_d:
                                self.turn_cube('D\'', True)
                            elif event.key == pygame.K_f:
                                self.turn_cube('F\'', True)
                            elif event.key == pygame.K_b:
                                self.turn_cube('B\'', True)
                        else:
                            if event.key == pygame.K_r:
                                self.turn_cube('R', True)
                            elif event.key == pygame.K_l:
                                self.turn_cube('L', True)
                            elif event.key == pygame.K_u:
                                self.turn_cube('U', True)
                            elif event.key == pygame.K_d:
                                self.turn_cube('D', True)
                            elif event.key == pygame.K_f:
                                self.turn_cube('F', True)
                            elif event.key == pygame.K_b:
                                self.turn_cube('B', True)
                        if event.key == pygame.K_SPACE:
                            self.scramble()

            # manages rotation of entire cube
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP]:
                self.angle_y -= 5
            if keys[pygame.K_DOWN]:
                self.angle_y += 5
            if keys[pygame.K_RIGHT]:
                self.angle_x -= 5
            if keys[pygame.K_LEFT]:
                self.angle_x += 5

            self.draw_cube()

    def draw_cube(self):
        glClearColor(0.6, 0.6, 0.6, 0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glTranslatef(0.0, 0.0, -15)
        glRotatef(45, 1, 1, 0)

        glRotatef(self.angle_y, -1, 0, 0)
        glRotatef(self.angle_x, 0, 1, 0)

        self.cube.show()

        pygame.display.flip()
        pygame.time.wait(10)

    def animate(self, dir, face, angle):
        animate_times = 6
        for i in range(animate_times):
            time.sleep(0.001)
            if dir == 'x':
                self.cube.turn_x(face, angle/animate_times)
            elif dir == 'y':
                self.cube.turn_y(face, angle/animate_times)
            elif dir == 'z':
                self.cube.turn_z(face, angle/animate_times)
            self.draw_cube()
        self.cube.round()
        self.draw_cube()

    # receives text input and turns cube and records it to output.txt
    def turn_cube(self, direction, w):
        write = w
        if direction == 'R\'':
            self.animate('x', 1, -math.pi/2)
        elif direction == 'R':
            self.animate('x', 1, math.pi/2)
        elif direction == 'L':
            self.animate('x', -1, -math.pi/2)
        elif direction == 'L\'':
            self.animate('x', -1, math.pi/2)
        elif direction == 'U\'':
            self.animate('y', 1, -math.pi/2)
        elif direction == 'U':
            self.animate('y', 1, math.pi/2)
        elif direction == 'D\'':
            self.animate('y', -1, math.pi/2)
        elif direction == 'D':
            self.animate('y', -1, -math.pi/2)
        elif direction == 'F\'':
            self.animate('z', 1, -math.pi/2)
        elif direction == 'F':
            self.animate('z', 1, math.pi/2)
        elif direction == 'B\'':
            self.animate('z', -1, math.pi/2)
        elif direction == 'B':
            self.animate('z', -1, -math.pi/2)
        else:
            print('Not a recognized character!')
            write = False
        if write:
            writer = open('output.txt', 'a')
            writer.write(direction + ' ')
            writer.close()

    # randomly scrambles cube
    def scramble(self):
        scrambled = []
        for i in range(25):
            move = random.randint(0, 11)
            scrambled.append(MOVES[move])
        self.cube.add_moves(scrambled)

    # loads input from input.txt and reads allowed moves
    def read_input(self):
        try:
            reader = open('input.txt', 'r')
            moves = reader.read()
            moves = moves.replace(' ', '')
            moves = moves.upper()
            for i in range(len(moves)):
                if moves[i] in MOVES:
                    if i + 1 < len(moves):
                        # handles prime and double move notation
                        if moves[i+1] == '\'':
                            self.turn_cube(moves[i:i+2], False)
                            i += 1
                            continue
                        elif moves[i+1] == '2':
                            self.turn_cube(moves[i], False)
                            self.turn_cube(moves[i], False)
                            i += 1
                            continue
                    self.turn_cube(moves[i], False)
        except FileNotFoundError:
            print('No input.txt file!')


if __name__ == '__main__':
    rubiks_cube = Visualizer()
    rubiks_cube.start()
