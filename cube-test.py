import pygame
import pygame.freetype
from rubik.cube import Cube
import math
import multiprocessing
import os

# Define constants and colors
node_radius = 30
initial_state = "UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB"
HIGHLIGHT_COLOR = (0, 255, 0)
NEIGHBOR_COLOR = (0, 0, 255)
NODE_COLOR = (255, 0, 0)
LINE_COLOR = (255, 255, 255)
max_x = 1600
max_y = 900
scren_scale = 15
current_neighbors = {}

move_colors = {
    "U": (255, 255, 255), "Ui": (255, 100, 100),
    "D": (0, 255, 0), "Di": (100, 255, 100),
    "L": (0, 0, 255), "Li": (100, 100, 255),
    "R": (255, 255, 0), "Ri": (255, 255, 100),
    "F": (255, 0, 255), "Fi": (255, 100, 255),
    "B": (0, 255, 255), "Bi": (100, 255, 255)
}
node_labels = {}  # A new dictionary to store move labels for nodes
move_angles = {
    "U": 0, "Ui": 30, "D": 60, "Di": 90,
    "L": 120, "Li": 150, "R": 180, "Ri": 210,
    "F": 240, "Fi": 270, "B": 300, "Bi": 330
}
def explore_moves(subset_of_moves, initial_state, results_queue):
    local_graph = {}
    local_node_positions = {}
    center_pos = (max_x * scren_scale // 2, max_y * scren_scale // 2)

    for move1 in subset_of_moves:
        for move2 in subset_of_moves:
            cube = Cube(initial_state)
            current_cube_state = cube.flat_str()
            local_node_positions[current_cube_state] = center_pos

            # Use updated center_pos for each new node
            cube, center_pos = add_node(cube, move1, center_pos, local_graph, local_node_positions)
            current_cube_state = cube.flat_str()
            cube, center_pos = add_node(cube, move2, center_pos, local_graph, local_node_positions)
            current_cube_state = cube.flat_str()

            while cube.flat_str() != initial_state:
                # Continue using updated center_pos
                cube, center_pos = add_node(cube, move1, center_pos, local_graph, local_node_positions)
                current_cube_state = cube.flat_str()
                cube, center_pos = add_node(cube, move2, center_pos, local_graph, local_node_positions)
                current_cube_state = cube.flat_str()

    results_queue.put((local_graph, local_node_positions))

def add_node(Cube, move, center_pos, local_graph, local_node_positions):
    cube_state = Cube.flat_str()
    new_cube = apply_move_and_get_new_state(Cube, move)
    new_state = new_cube.flat_str()

    # Ensure the current cube state is in the local graph
    if cube_state not in local_graph:
        local_graph[cube_state] = []

    if new_state not in local_graph:
        local_graph[new_state] = []

    # Calculate new position for node only if it doesn't exist
    if new_state not in local_node_positions:
        angle = move_angles[move]
        angle = math.radians(angle)
        offset_distance = 30
        x, y = center_pos
        new_x = int(x + offset_distance * math.cos(angle))
        new_y = int(y + offset_distance * math.sin(angle))
        local_node_positions[new_state] = (new_x, new_y)
    else:
        # If position exists, use the existing position
        new_x, new_y = local_node_positions[new_state]
         # If the node already exists, update its neighbors
        for neighbor in local_graph[new_state]:
            if neighbor != cube_state:
                # Ensure the neighbor is initialized in the graph
                if neighbor not in local_graph:
                    local_graph[neighbor] = []
                local_graph[neighbor].append(cube_state)
                if cube_state not in local_graph:
                    local_graph[cube_state] = []
                local_graph[cube_state].append(neighbor)

    node_labels[new_state] = move
    if new_state not in local_graph[cube_state]:
        local_graph[cube_state].append(new_state)
    return new_cube, (new_x, new_y)




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
        new_x = new_x#max(10, min(new_x, max_x)-10)
        new_y = new_y#max(10, min(new_y, max_y)-10)
        
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



def draw_graph(surface, font, graph, node_positions, node_labels, clicked_state=None):
    for state, neighbors in graph.items():
        start_x, start_y = node_positions[state]
        for neighbor in neighbors:
            end_x, end_y = node_positions[neighbor]
            if state == clicked_state or neighbor == clicked_state:
                line_color = NEIGHBOR_COLOR
            else:
                line_color = LINE_COLOR
            pygame.draw.line(surface, line_color, (start_x, start_y), (end_x, end_y), 5)

        node_color = move_colors[node_labels[state]] if state in node_labels else NODE_COLOR
        pygame.draw.circle(surface, node_color, (start_x, start_y), node_radius)

    # Draw the new neighbor nodes
    for state, pos in current_neighbors.items():
        pygame.draw.circle(surface, NEIGHBOR_COLOR, pos, node_radius)
    if state in node_labels:
        move_label = node_labels[state]
        move_color = move_colors[move_label]
        #font.render_to(surface, (start_x + 15, start_y), move_label, move_color)

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
    global current_cube_state

   

    moves = ["U", "Ui", "D", "Di", "L", "Li", "R", "Ri", "F", "Fi", "B", "Bi"]
    move_subsets = []
    #for move1 in moves:
    #    for move2 in moves:
    #        move_subsets.append([move1, move2])
               # Example subsets  # Example subsets
    move_subsets = [moves]  # Example subsets  # Example subsets
    results_queue = multiprocessing.Queue()
    print("Number of subsets:", len(move_subsets))
    print("subsets:", move_subsets)
    processes = []
    current_index = 0
    step_size = 500  # Number of nodes to process at each iteration
    for subset in move_subsets:
        p = multiprocessing.Process(target=explore_moves, args=(subset, initial_state, results_queue))
        processes.append(p)
        p.start()

    full_graph = {}
    full_node_positions = {}
    for _ in processes:
        local_graph, local_node_positions = results_queue.get()

        # Update node positions
        full_node_positions.update(local_node_positions)

        # Update graph with nodes and edges
        for state, neighbors in local_graph.items():
            if state not in full_graph:
                full_graph[state] = neighbors
            else:
                for neighbor in neighbors:
                    if neighbor not in full_graph[state]:
                        full_graph[state].append(neighbor)

        # Update edges for bidirectional consistency
        for state, neighbors in local_graph.items():
            for neighbor in neighbors:
                if state not in full_graph[neighbor]:
                    full_graph[neighbor].append(state)

    for p in processes:
        p.join()
    all_moves = ["U", "Ui", "D", "Di", "L", "Li", "R", "Ri", "F", "Fi", "B", "Bi"]
    for state in full_node_positions.keys():
        cube = Cube(state)
        for move in all_moves:
            neighbor_state = apply_move_and_get_new_state(cube, move).flat_str()
            if neighbor_state in full_node_positions:
                if neighbor_state not in full_graph[state]:
                    full_graph[state].append(neighbor_state)
                if state not in full_graph[neighbor_state]:
                    full_graph[neighbor_state].append(state)

    pygame.init()
    screen = pygame.display.set_mode((max_x, max_y))
    pygame.display.set_caption('Rubik\'s Cube Visualizer')
    font = pygame.freetype.Font(None, 20)
    graph_surface = pygame.Surface((max_x * scren_scale, max_y * scren_scale))
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Clear the surface for new drawing
        #graph_surface.fill((0, 0, 0))

        # Draw a portion of the graph
        #print(len(full_node_positions))
        #print(full_node_positions)
        partial_graph = dict(list(full_graph.items())[current_index:current_index + step_size])
        draw_graph(graph_surface, font, partial_graph, full_node_positions, node_labels)

        # Update the current index
        current_index = (current_index + step_size) % len(full_graph)

        screen.fill((0, 0, 0))
        scaled_graph = pygame.transform.scale(graph_surface, (max_x, max_y))
        screen.blit(scaled_graph, (0, 0))
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()


