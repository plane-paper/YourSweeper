def get_neighbors(grid, x, y):
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    return [(x + dx, y + dy) for dx, dy in directions if 0 <= x + dx < len(grid[0]) and 0 <= y + dy < len(grid)]
