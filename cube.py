import pygame
import pygame.freetype  # Import the freetype module.
from rubik.cube import Cube
import random
import math
# Define colors
move_colors = {
    "U": (255, 0, 0), "Ui": (255, 100, 100),
    "D": (0, 255, 0), "Di": (100, 255, 100),
    "L": (0, 0, 255), "Li": (100, 100, 255),
    "R": (255, 255, 0), "Ri": (255, 255, 100),
    "F": (255, 0, 255), "Fi": (255, 100, 255),
    "B": (0, 255, 255), "Bi": (100, 255, 255)
}
graph = {}
visited_states = set()
current_cube_state = None
node_positions = {}
current_neighbors = {}

node_radius = 10
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

    if new_state not in node_positions:
        # Generate a random angle for positioning the new node
        angle = random.uniform(0, 2 * math.pi)
        offset_distance = 100  # Distance from the center_pos

        # Calculate and store the position for the new node
        x = int(center_pos[0] + offset_distance * math.cos(angle))
        y = int(center_pos[1] + offset_distance * math.sin(angle))
        new_x = max(0, min(x, max_x))
        new_y = max(0, min(y, max_y))
        node_positions[new_state] = (new_x, new_y)

        # Update the graph with the new state
        if cube_state not in graph:
            graph[cube_state] = []
        graph[cube_state].append(new_state)

        print("Node added for move:", move, "New state:", new_state)
    return new_cube
def calculate_forces():
    # Constants for forces
    repulsion_const = 0.00001
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
            diff = pygame.math.Vector2(node_positions[neighbor]) - pygame.math.Vector2(node_positions[state]) + pygame.math.Vector2(.00000001,.00000001)
            distance = diff.length()
            attraction_force = distance**2 * attraction_const
            force_on_nodes[state] -= diff.normalize() * attraction_force
            force_on_nodes[neighbor] += diff.normalize() * attraction_force

    return force_on_nodes

def update_positions():
    forces = calculate_forces()
    for state, force in forces.items():
        # Update positions based on forces
        new_x = node_positions[state][0] + force.x * 0.01
        new_y = node_positions[state][1] + force.y * 0.01
        
        # Ensure the new position stays within the screen boundaries
        new_x = max(0, min(new_x, max_x))
        new_y = max(0, min(new_y, max_y))
        
        node_positions[state] = (new_x, new_y)

def expand_graph(cube_state, center_pos):
    global current_cube_state, graph, node_positions, current_neighbors

    moves = ["U", "Ui", "D", "Di", "L", "Li", "R", "Ri", "F", "Fi", "B", "Bi"]

    # Initialize the graph for the current cube state if not present
    if cube_state not in graph:
        graph[cube_state] = []

    # Retain the current path and clear other nodes
    new_graph = {}
    last_node_in_path = None
    for state in graph:
        if state == current_cube_state:
            new_graph[state] = [cube_state]
            last_node_in_path = state
        else:
            new_graph[state] = graph[state]

    # Adjust the position of the last node in the path to create a longer edge
    if last_node_in_path and last_node_in_path in node_positions:
        adjust_last_node_position(last_node_in_path, cube_state, 1.5)  # 1.5 is the lengthening factor

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
                x = int(center_pos[0] + 100 * math.cos(math.radians(angle)))
                y = int(center_pos[1] + 100 * math.sin(math.radians(angle)))
                node_positions[new_state] = (x, y)
                current_neighbors[new_state] = (x, y)
            angle += 30

    print("Graph expanded for state:", cube_state)

    return last_node_in_path

def adjust_last_node_position(last_node, current_node, factor):
    last_x, last_y = node_positions[last_node]
    current_x, current_y = node_positions[current_node]

    direction_x = current_x - last_x
    direction_y = current_y - last_y
    length = math.sqrt(direction_x**2 + direction_y**2)

    # Check to prevent division by zero
    if length == 0:
        return

    # Normalize the direction vector
    direction_x /= length
    direction_y /= length

    # Extend the last node position
    extended_x = last_x - direction_x * length * (factor - 1)
    extended_y = last_y - direction_y * length * (factor - 1)

    node_positions[last_node] = (int(extended_x), int(extended_y))

def extend_line(start_x, start_y, end_x, end_y, factor):
    # Calculate the direction of the line
    direction_x = end_x - start_x
    direction_y = end_y - start_y

    # Normalize the direction
    length = math.sqrt(direction_x**2 + direction_y**2)
    direction_x /= length
    direction_y /= length

    # Extend the line
    extended_x = end_x + direction_x * length * (factor - 1)
    extended_y = end_y + direction_y * length * (factor - 1)

    return extended_x, extended_y
def draw_graph(screen, font, clicked_state=None, last_node_in_path=None):
    edge_extension_factor = 1  # Factor to extend the edge length

    for state, neighbors in graph.items():
        start_x, start_y = node_positions[state]
        for neighbor in neighbors:
            end_x, end_y = node_positions[neighbor]

            # Check if this edge is between the clicked node and the last node in the path
            if (state == clicked_state and neighbor == last_node_in_path) or (state == last_node_in_path and neighbor == clicked_state):
                # Calculate the extended points for the edge
                extended_x, extended_y = extend_line(start_x, start_y, end_x, end_y, edge_extension_factor)
                pygame.draw.line(screen, LINE_COLOR, (start_x, start_y), (extended_x, extended_y), 1)
            else:
                pygame.draw.line(screen, LINE_COLOR, (start_x, start_y), (end_x, end_y), 1)

            node_color = HIGHLIGHT_COLOR if state == clicked_state else NODE_COLOR
            pygame.draw.circle(screen, node_color, (start_x, start_y), node_radius)
    # Draw and label new neighbor nodes 
    #push test
    if clicked_state:
        for move in ["U", "Ui", "D", "Di", "L", "Li", "R", "Ri", "F", "Fi", "B", "Bi"]:
            new_cube = apply_move_and_get_new_state(Cube(clicked_state), move)
            new_state = new_cube.flat_str()
            if new_state in current_neighbors:
                x, y = current_neighbors[new_state]

                pygame.draw.circle(screen, move_colors[move], (x, y), node_radius-2)
                font.render_to(screen, (x + 15, y), move, move_colors[move])
            elif new_state in node_positions and new_state in graph[clicked_state]:
                # If the node is an existing neighbor, label it with the move color
                x, y = node_positions[new_state]
                font.render_to(screen, (x + 15, y), move, move_colors[move])
                #node_color = HIGHLIGHT_COLOR if state == clicked_state else NODE_COLOR
                pygame.draw.circle(screen, move_colors[move], (x, y), node_radius)


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
def determine_move(state1, state2):
    """
    Determine the move made between two states.
    """
    moves = ["U", "Ui", "D", "Di", "L", "Li", "R", "Ri", "F", "Fi", "B", "Bi"]
    cube1 = Cube(state1)
    
    for move in moves:
        # Apply each move to the first state
        temp_cube = Cube(cube1.flat_str())  # Create a copy to avoid modifying the original
        apply_move_and_get_new_state(temp_cube, move)
        if temp_cube.flat_str() == state2:
            return move  # Found the move that transforms state1 into state2

    return None  # No single move found

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

    # Expand graph from the initial state
    expand_graph(current_cube_state, center_pos)

    scale = 30  # Scale for each sticker
    cube = Cube(initial_state)
    
    # Set clicked state to the initial state at the start
    clicked_state = initial_state
    last_node_in_path = None

    running = True
    font = pygame.freetype.Font(None, 20)

    while running:
        screen.fill((0, 0, 0))

        draw_graph(screen, font, clicked_state)
        update_positions()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Check if a node was clicked
                new_clicked_state = check_click_on_node(pygame.mouse.get_pos())
                if new_clicked_state:
                    clicked_state = new_clicked_state
                    last_node_in_path = expand_graph(clicked_state, node_positions[clicked_state])
                draw_graph(screen, font, clicked_state, last_node_in_path)

        if clicked_state is not None:
            draw_cube(clicked_state, screen, scale)  # Draw the cube for the clicked state
        else:
            draw_cube(cube.flat_str(), screen, scale)  # Draw the initial cube

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
