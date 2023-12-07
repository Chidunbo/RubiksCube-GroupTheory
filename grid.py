import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Create grid dimensions
grid_size = 100
grid = np.zeros((grid_size, grid_size))

# Initialize the figure and axes
fig, ax = plt.subplots()

# Create an empty plot with grid lines
plot = ax.imshow(grid, cmap='binary', interpolation='none')
ax.grid(True, which='both', color='blu', linewidth=1)

# Define the coordinates of the dot
dot_positions = [(0, 0), (1, 1), (0, 0)]
dot_index = 0

# Update function for the animation
def update(frame):
    global dot_index

    # Update the grid with the dot position
    grid.fill(0)
    dot_pos = dot_positions[dot_index]
    grid[dot_pos] = 1

    # Update the plot with the new grid
    plot.set_array(grid)

    # Move to the next dot position
    dot_index = (dot_index + 1) % len(dot_positions)

    return [plot]

# Create the animation
ani = animation.FuncAnimation(fig, update, frames=100, interval=200, blit=True)

# Show the animation
plt.show()