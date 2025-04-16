def get_neighbors(grid, x, y):
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    return [(x + dx, y + dy) for dx, dy in directions if 0 <= x + dx < len(grid[0]) and 0 <= y + dy < len(grid)]

def print_grid(grid):
    print("Current grid state:")
    for row in grid:
        print(' '.join(row))
    print("Grid printed.")


def save_grid_to_file(grid, filename="grid_snapshot.txt"):
    print("Saving grid snapshot to file...")
    with open(filename, 'w') as file:
        for row in grid:
            file.write(' '.join(row) + '\n')
    print(f"Grid snapshot saved as {filename}")