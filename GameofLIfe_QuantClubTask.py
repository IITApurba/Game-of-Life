import pygame
import numpy as np
import math

grid_size = 40
cell_size = 40

pygame.init()
size=width,height=800,800

screen = pygame.display.set_mode(size)
pygame.display.set_caption('Hexagonal Grid Simulation')

def get_neighbors_hexagonal(i, j):
    neighbors = []
    if j % 2 == 0:
        neighbors = [(i-1, j-1), (i-1, j), (i, j-1), (i, j+1), (i+1, j-1), (i+1, j)]
    else:
        neighbors = [(i-1, j), (i-1, j+1), (i, j-1), (i, j+1), (i+1, j), (i+1, j+1)]
    valid_neighbors = [(x, y) for x, y in neighbors if 0 <= x < grid_size and 0 <= y < grid_size]
    return valid_neighbors


def update_grid(grid, generation_count):
    new_grid = grid.copy()
    newly_born_cells = set()  # Track cells born in the current generation
    cells_died_underpop = set()  # Track cells that died due to underpopulation
    cells_died_overpop = set()  # Track cells that died due to overpopulation
    
    for i in range(grid_size):
        for j in range(grid_size):
            cell = grid[i, j]
            neighbor_count = sum(grid[n] for n in get_neighbors_hexagonal(i, j))
            if cell == 1:
                if neighbor_count < 2:
                    new_grid[i, j] = 0  # Cell dies due to underpopulation
                    cells_died_underpop.add((i, j))  # Track cells that died due to underpopulation
                elif neighbor_count == 2 or neighbor_count == 3:
                    new_grid[i, j] = 1  # Cell lives on to the next generation
                elif neighbor_count > 3:
                    new_grid[i, j] = 0  # Cell dies due to overpopulation
                    cells_died_overpop.add((i, j))  # Track cells that died due to overpopulation
            else:
                if neighbor_count == 3:
                    new_grid[i, j] = 1  # Cell is born due to exactly 3 live neighbors
                    newly_born_cells.add((i, j))  # Track newly born cells
                elif generation_count % 6 == 0:
                    new_grid[i, j] = 1  # Resurrect dead cell after 6 generations
                elif generation_count % 4 == 0:
                    if np.random.choice([True, False]):
                        new_grid[i, j] = 1  # Randomly bring dead cell to life every 4 generations
    
    # Ensure cells born in the current generation do not die in the same generation
    for i, j in newly_born_cells:
        new_grid[i, j] = 1
    
    # Ensure cells that died due to underpopulation or overpopulation do not die again by the same reasons
    for i, j in cells_died_underpop:
        if sum(grid[n] for n in get_neighbors_hexagonal(i, j)) >= 2:
            new_grid[i, j] = 1
    for i, j in cells_died_overpop:
        if sum(grid[n] for n in get_neighbors_hexagonal(i, j)) <= 3:
            new_grid[i, j] = 1
            
    return new_grid

initial_state = np.random.choice([0, 1], size=(grid_size, grid_size))

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED =  (255,0,0)

# Function to visualize the hexagonal grid using pygame
def visualize_hexagonal_grid(grid):
    screen.fill(WHITE)
    for i in range(grid_size):
        for j in range(grid_size):
            x = j * 1.5 * cell_size
            y = i * math.sqrt(3) * cell_size + j % 2 * math.sqrt(3) / 2 * cell_size
            color = RED if grid[i, j] == 1 else BLACK
            pygame.draw.polygon(screen, color, [(x, y - cell_size/2), (x + 0.75 * cell_size, y - cell_size/2), (x + cell_size, y), (x + 0.75 * cell_size, y + cell_size/2), (x, y + cell_size/2), (x - 0.25 * cell_size, y)])
    pygame.display.flip()

# Update and visualize the grid for a few iterations using pygame
num_iterations = 100
clock = pygame.time.Clock()
running = True
generation_count = 0

while running and generation_count < num_iterations:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    visualize_hexagonal_grid(initial_state)
    initial_state = update_grid(initial_state, generation_count)
    generation_count += 1

    clock.tick(10)

pygame.quit()
