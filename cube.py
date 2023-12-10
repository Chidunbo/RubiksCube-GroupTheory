import pygame
import pygame.freetype  # Import the freetype module.
from rubik.cube import Cube

import math
# Define colors
graph = {}
visited_states = set()


def draw_graph(screen, center_pos, cube_state, radius=100):
    # Define the 12 moves
    moves = ["U", "Ui", "D", "Di", "L", "Li", "R", "Ri", "F", "Fi", "B", "Bi"]
    angle = 0
    node_positions = []
    for move in moves:
        # Calculate position for each neighbor node
        x = int(center_pos[0] + radius * math.cos(math.radians(angle)))
        y = int(center_pos[1] + radius * math.sin(math.radians(angle)))
        node_positions.append((x, y))
        pygame.draw.line(screen, (255, 255, 255), center_pos, (x, y), 1)
        pygame.draw.circle(screen, (255, 255, 255), (x, y), 5)
        angle += 30
    return node_positions

def check_click_on_node(mouse_pos, node_positions):
    for index, position in enumerate(node_positions):
        distance = math.sqrt((mouse_pos[0] - position[0])**2 + (mouse_pos[1] - position[1])**2)
        if distance <= 20:
            return index
    return None

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
    cube = Cube("UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB")
    counter = 0
    running = True
    GAME_FONT = pygame.freetype.Font(None, 10)
    center_pos = (screen.get_width() // 2, screen.get_height() // 2)


    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # Handle mouse click event
            if event.type == pygame.MOUSEBUTTONDOWN:
                node_index = check_click_on_node(pygame.mouse.get_pos(), node_positions)
                if node_index is not None:
                    # Apply the corresponding move to the cube
                    moves = ["U", "Ui", "D", "Di", "L", "Li", "R", "Ri", "F", "Fi", "B", "Bi"]
                    move = moves[node_index]
                    getattr(cube, move)()  # Call the move method on the cube

        screen.fill((0, 0, 0))  # Fill background
        node_positions = draw_graph(screen, center_pos, cube.flat_str())
        draw_cube(cube.flat_str(), screen, scale)  # Draw the cube
        pygame.display.flip()



                
        text_screen.fill((255,255,255))
        # You can use `render` and then blit the text surface ...
       
        screen.fill((0, 0, 0))  # Fill background
 
        #cube.R()
            #cube.U()
        #cube.U_inv()
        current_state_str = cube.flat_str()
        prev_state_str = current_state_str
        draw_graph(screen, center_pos, cube.flat_str())

        draw_cube(cube.flat_str(), screen, scale)  # Draw the cube
        #text_surface, rect = GAME_FONT.render(str(cube.state), (255, 255, 255))
        #screen.blit(text_surface, (100, 600))
        # or just `render_to` the target surface.
        #GAME_FONT.render_to(screen, (40, 350), cube.flat_str(), (255, 255, 255))
        pygame.display.flip()
        pygame.time.wait(10)
   


    pygame.quit()

if __name__ == "__main__":
    main()
