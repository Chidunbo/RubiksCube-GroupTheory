import pygame
import pygame.freetype  # Import the freetype module.
from rubik.cube import Cube
import random
import math
# Define colors
graph = {}
visited_states = set()
current_cube_state = None
node_positions = {}
node_radius = 10
initial_state = "UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB"

def calculate_forces():
    # Constants for forces
    repulsion_const = 500
    attraction_const = 0.000001

    force_on_nodes = {state: pygame.math.Vector2(0, 0) for state in node_positions}

    # Calculate repulsive forces
    for state1, pos1 in node_positions.items():
        for state2, pos2 in node_positions.items():
            if state1 != state2:
                diff = pygame.math.Vector2(pos1) - pygame.math.Vector2(pos2)
                distance = diff.length()
                if distance > 0:
                    repulsion_force = repulsion_const / distance**2
                    force_on_nodes[state1] += diff.normalize() * repulsion_force

    # Calculate attractive forces
    for state, neighbors in graph.items():
        for neighbor in neighbors:
            diff = pygame.math.Vector2(node_positions[neighbor]) - pygame.math.Vector2(node_positions[state])
            distance = diff.length()
            attraction_force = distance**2 * attraction_const
            force_on_nodes[state] -= diff.normalize() * attraction_force
            force_on_nodes[neighbor] += diff.normalize() * attraction_force

    return force_on_nodes

def update_positions():
    forces = calculate_forces()
    for state, force in forces.items():
        # Update positions based on forces
        new_x = node_positions[state][0] + force.x * 0.1
        new_y = node_positions[state][1] + force.y * 0.1
        
        # Ensure the new position stays within the screen boundaries
        new_x = max(0, min(new_x, 800))
        new_y = max(0, min(new_y, 600))
        
        node_positions[state] = (new_x, new_y)

def expand_graph(cube_state, center_pos):
    moves = ["U", "Ui", "D", "Di", "L", "Li", "R", "Ri", "F", "Fi", "B", "Bi"]
    if cube_state not in graph:
        graph[cube_state] = []
        angle = 0
        for move in moves:
            new_cube = apply_move_and_get_new_state(Cube(cube_state), move)
            new_state = new_cube.flat_str()
            if new_state not in graph[cube_state]:
                graph[cube_state].append(new_state)
                # Calculate and store the position for the new node
                x = int(center_pos[0] + 100 * math.cos(math.radians(angle)))
                y = int(center_pos[1] + 100 * math.sin(math.radians(angle)))
                node_positions[new_state] = (x, y)
                angle += 30
    print("Graph expanded for state:", cube_state)

def draw_graph(screen):
    for state, neighbors in graph.items():
        start_x, start_y = node_positions[state]
        for neighbor in neighbors:
            end_x, end_y = node_positions[neighbor]
            pygame.draw.line(screen, (255, 255, 255), (start_x, start_y), (end_x, end_y), 1)
            pygame.draw.circle(screen, (255, 0, 0), (end_x, end_y), node_radius)

def check_click_on_node(mouse_pos):
    for state, pos in node_positions.items():
        distance = math.sqrt((mouse_pos[0] - pos[0])**2 + (mouse_pos[1] - pos[1])**2)
        if distance <= node_radius:
            return state
    return None


def apply_move_and_get_new_state(cube, move):
    new_cube = Cube(cube.flat_str())

    if move == "U":
        new_cube.U()
    elif move == "Ui":
        new_cube.Ui()
    elif move == "D":
        new_cube.D()
    elif move == "Di":
        new_cube.Di()
    elif move == "L":
        new_cube.L()
    elif move == "Li":
        new_cube.Li()
    elif move == "R":
        new_cube.R()
    elif move == "Ri":
        new_cube.Ri()
    elif move == "F":
        new_cube.F()
    elif move == "Fi":
        new_cube.Fi()
    elif move == "B":
        new_cube.B()
    elif move == "Bi":
        new_cube.Bi()
    return new_cube
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
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption('Rubik\'s Cube Visualizer')
    current_cube_state = initial_state
    center_pos = (400, 300)  # Center of the screen
    node_positions[current_cube_state] = center_pos
    expand_graph(current_cube_state, center_pos)
    scale = 30  # Scale for each sticker
    cube = Cube("UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB")
    clicked_state = "UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB"
    running = True
    while running:
        screen.fill((0, 0, 0))
        update_positions()  # Update positions based on forces

        draw_graph(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                clicked_state = check_click_on_node(pygame.mouse.get_pos())

                if clicked_state:
                    expand_graph(clicked_state, node_positions[clicked_state])
                    #update_positions()
        #draw_cube(current_cube_state, screen, scale)  # Draw the cube
        if clicked_state is not None:
            prev_state = clicked_state
            draw_cube(clicked_state, screen, scale)  # Draw the cube
        else:
            draw_cube(prev_state, screen, scale)
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
