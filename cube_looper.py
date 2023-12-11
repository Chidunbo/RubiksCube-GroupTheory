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
current_neighbors = {}

node_radius = 5
initial_state = "UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB"
HIGHLIGHT_COLOR = (0, 255, 0)  # Green for clicked node
NEIGHBOR_COLOR = (0, 0, 255)   # Blue for neighbors
NODE_COLOR = (255, 0, 0)       # Red for other nodes
LINE_COLOR = (255, 255, 255)
max_x = 1600
max_y = 900
def add_node(Cube, move, center_pos):
    """
    Add a new node to the graph corresponding to the given move from the current cube state.
    cube_state: Current state of the cube.
    move: The move to apply to the cube state.
    center_pos: The position around which the new node should be placed.
    """
    cube_state = Cube.flat_str()
    new_cube = apply_move_and_get_new_state(Cube, move)
    new_state = new_cube.flat_str()

    # Ensure the current cube state is in the graph
    if cube_state not in graph:
        graph[cube_state] = []

    # Add or update node
    if new_state not in node_positions:
        # Generate a random angle for positioning the new node
        angle = random.uniform(0, 2 * math.pi)
        offset_distance = 100  # Distance from the center_pos

        # Calculate and store the position for the new node
        x = int(center_pos[0] + offset_distance * math.cos(angle))
        y = int(center_pos[1] + offset_distance * math.sin(angle))
        new_x = max(10, min(x, max_x)-10)
        new_y = max(10, min(y, max_y)-10)
        node_positions[new_state] = (new_x, new_y)
    else:
        # If the node already exists, update its neighbors
        for neighbor in graph[new_state]:
            if neighbor != cube_state:
                # Ensure the neighbor is initialized in the graph
                if neighbor not in graph:
                    graph[neighbor] = []
                graph[neighbor].append(cube_state)
                if cube_state not in graph:
                    graph[cube_state] = []
                graph[cube_state].append(neighbor)

    # Connect the current state with the new state
    if new_state not in graph[cube_state]:
        graph[cube_state].append(new_state)

    print("Node added/updated for move:", move, "State:", new_state)
    return new_cube


def calculate_forces():
    # Constants for forces
    repulsion_const = 0.000001
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
            diff = pygame.math.Vector2(node_positions[neighbor]) - pygame.math.Vector2(node_positions[state]) + pygame.math.Vector2(.00001,.00001)
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
        new_x = max(10, min(new_x, max_x)-10)
        new_y = max(10, min(new_y, max_y)-10)
        
        node_positions[state] = (new_x, new_y)

def expand_graph(cube_state, center_pos):
    global current_cube_state, graph, node_positions, current_neighbors

    moves = ["U", "Ui", "D", "Di", "L", "Li", "R", "Ri", "F", "Fi", "B", "Bi"]

    # Initialize the graph for the current cube state if not present
    if cube_state not in graph:
        graph[cube_state] = []

    # Retain the current path and clear other nodes
    new_graph = {}
    for state in graph:
        if state == current_cube_state:
            new_graph[state] = [cube_state]
        else:
            new_graph[state] = graph[state]

    # Clear node_positions of nodes not in new_graph
    for state in list(node_positions.keys()):
        if state not in new_graph and state != cube_state:
            del node_positions[state]

    graph = new_graph
    current_cube_state = cube_state  # Update the current cube state

    # Clear current neighbors
    current_neighbors.clear()

    angle = 0
    for move in moves:
        new_cube = apply_move_and_get_new_state(Cube(cube_state), move)
        new_state = new_cube.flat_str()
        if new_state not in graph[cube_state]:
            graph[cube_state].append(new_state)
            if new_state not in node_positions:
                x = int(center_pos[0] + 50 * math.cos(math.radians(angle)))
                y = int(center_pos[1] + 50 * math.sin(math.radians(angle)))
                node_positions[new_state] = (x, y)
                # Store new neighbors
                current_neighbors[new_state] = (x, y)
            angle += 30

    print("Graph expanded for state:", cube_state)



def draw_graph(screen, clicked_state=None):
    for state, neighbors in graph.items():
        start_x, start_y = node_positions[state]
        for neighbor in neighbors:
            end_x, end_y = node_positions[neighbor]
            if state == clicked_state or neighbor == clicked_state:
                line_color = NEIGHBOR_COLOR
            else:
                line_color = LINE_COLOR
            pygame.draw.line(screen, line_color, (start_x, start_y), (end_x, end_y), 1)

        node_color = HIGHLIGHT_COLOR if state == clicked_state else NODE_COLOR
        pygame.draw.circle(screen, node_color, (start_x, start_y), node_radius)

    # Draw the new neighbor nodes
    for state, pos in current_neighbors.items():
        pygame.draw.circle(screen, NEIGHBOR_COLOR, pos, node_radius)

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
    global current_cube_state, graph, node_positions  # Declare as global to modify them

    pygame.init()
    screen = pygame.display.set_mode((max_x, max_y))
    pygame.display.set_caption('Rubik\'s Cube Visualizer')

    # Set initial state
    current_cube_state = initial_state
    center_pos = (max_x // 2, max_y // 2)  # Center of the screen

    # Initialize graph and node_positions with the initial state
    graph[current_cube_state] = []
    node_positions[current_cube_state] = center_pos

    scale = 30  # Scale for each sticker
    clicked_state = None
    running = True
    moves = ["U", "Ui", "D", "Di", "L", "Li", "R", "Ri", "F", "Fi", "B", "Bi"]

    for move1 in moves:
        for move2 in moves:
            cube = Cube(initial_state)
            current_cube_state = cube.flat_str()
            cube = add_node(cube, move1, node_positions[current_cube_state])
            cube = add_node(cube, move2, node_positions[current_cube_state])

            while cube.flat_str() != initial_state: # Apply first move
                cube = add_node(cube, move1, node_positions[current_cube_state])
                current_cube_state = cube.flat_str()

            # Apply second move
                cube = add_node(cube, move2, node_positions[current_cube_state])
                current_cube_state = cube.flat_str()

            # Check if solved state is reached
            if cube.flat_str() == initial_state:
                draw_graph(screen, clicked_state)
                #update_positions()
                #draw_cube(cube.flat_str(), screen, scale)  # Draw the current cube
                pygame.display.flip()
                pygame.time.wait(5)  # Delay for visual effect  # Skip the rest and go to the next pair if solved

            # Visual update for the current move pair
            screen.fill((0, 0, 0))
           

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            if not running:
                break

        if not running:
            break

    pygame.quit()

if __name__ == "__main__":
    main()


if __name__ == "__main__":
    main()