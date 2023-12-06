import pygame
import pygame.freetype  # Import the freetype module.

class RubiksCube:
    def __init__(self, state):
        if len(state) != 54:
            raise ValueError("State must be a 54-element vector.")
        self.state = list(state)

    def _rotate_face(self, indices):
        temp = [self.state[i] for i in indices]
        for i in range(9):
            self.state[indices[i]] = temp[(i - 6) % 9]

    def _rotate_side(self, indices, inverse=False):
        temp = [self.state[i] for i in indices]
        if inverse:
            temp = temp[-3:] + temp[:-3]
        else:
            temp = temp[3:] + temp[:3]
        for i, index in enumerate(indices):
            self.state[index] = temp[i]

    def R(self):
        self._rotate_face([9, 10, 11, 12, 13, 14, 15, 16, 17])
        self._rotate_side([2, 5, 8, 18, 21, 24, 27, 30, 33, 45, 48, 51], inverse=True)

    def R_inv(self):
        self.R()
        self.R()
        self.R()

    def L(self):
        self._rotate_face([36, 37, 38, 39, 40, 41, 42, 43, 44])
        self._rotate_side([0, 3, 6, 20, 23, 26, 29, 32, 35, 47, 50, 53])

    def L_inv(self):
        self.L()
        self.L()
        self.L()

    def U(self):
        self._rotate_face([0, 1, 2, 3, 4, 5, 6, 7, 8])
        self._rotate_side([9, 10, 11, 18, 19, 20, 27, 28, 29, 36, 37, 38])

    def U_inv(self):
        self.U()
        self.U()
        self.U()

    def D(self):
        self._rotate_face([27, 28, 29, 30, 31, 32, 33, 34, 35])
        self._rotate_side([15, 16, 17, 24, 25, 26, 33, 34, 35, 42, 43, 44], inverse=True)

    def D_inv(self):
        self.D()
        self.D()
        self.D()

    def F(self):
        self._rotate_face([18, 19, 20, 21, 22, 23, 24, 25, 26])
        self._rotate_side([6, 7, 8, 9, 12, 15, 27, 28, 29, 36, 39, 42])

    def F_inv(self):
        self.F()
        self.F()
        self.F()

    def B(self):
        self._rotate_face([45, 46, 47, 48, 49, 50, 51, 52, 53])
        self._rotate_side([0, 1, 2, 11, 14, 17, 24, 25, 26, 33, 40, 43], inverse=True)

    def B_inv(self):
        self.B()
        self.B()
        self.B()

# Define colors
color = {
    "U": (255, 255, 255),  # white
    "D": (255, 255, 0),    # yellow
    "L": (255, 165, 0),    # orange
    "R": (255, 0, 0),      # red
    "F": (0, 170, 0),      # green
    "B": (0, 0, 255)       # blue
}

def draw_cube(cube_state, screen, scale):
    for face in range(6):
        for i in range(3):
            for j in range(3):
                idx = face * 9 + i * 3 + j
                color_key = cube_state[idx]
                pygame.draw.rect(screen, color[color_key],
                                 (j * scale + face % 3 * 3 * scale, i * scale + face // 3 * 3 * scale, scale, scale))
                pygame.draw.rect(screen, (0, 0, 0),
                                 (j * scale + face % 3 * 3 * scale, i * scale + face // 3 * 3 * scale, scale, scale), 1)

def main():
    pygame.init()
    scale = 30  # Scale for each sticker
    screen = pygame.display.set_mode((9 * scale, 12 * scale))
    pygame.display.set_caption('Rubik\'s Cube Visualizer')
    text_screen =  pygame.display.set_mode((800, 600))
    cube = RubiksCube("UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB")
    counter = 0
    running = True
    GAME_FONT = pygame.freetype.Font("your_font.ttf", 24)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        text_screen.fill((255,255,255))
        # You can use `render` and then blit the text surface ...
       
        screen.fill((0, 0, 0))  # Fill background
        if counter == 0:
            cube.R()
            #cube.U_inv()
            counter += 1
        if  cube.state == "UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB":
            pygame.time.wait(10000000)
            print(counter)
            running = False

        counter +=1 
        cube.R()
        #cube.U_inv()
        draw_cube(cube.state, screen, scale)
        text_surface, rect = GAME_FONT.render("Hello World!", (0, 0, 0))
        screen.blit(text_surface, (40, 250))
        # or just `render_to` the target surface.
        GAME_FONT.render_to(screen, (40, 350), "Hello World!", (0, 0, 0))
        pygame.display.flip()
        pygame.time.wait(10)
   


    pygame.quit()

if __name__ == "__main__":
    main()
