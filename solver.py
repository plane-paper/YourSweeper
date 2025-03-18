from utils import get_neighbors
import pyautogui
import random
from collections import defaultdict

def solve_grid(grid, remaining_mines):
    moves = {}
    safe_tiles = set()
    mines = set()
    
    # First pass - direct rules
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if grid[y][x].isdigit():
                cell_value = int(grid[y][x])
                neighbors = get_neighbors(grid, x, y)
                unopened = [(nx, ny) for nx, ny in neighbors if grid[ny][nx] == 'unopened']
                flagged = [(nx, ny) for nx, ny in neighbors if grid[ny][nx] == 'flag']

                # Rule 1: All mines found - click remaining
                if len(flagged) == cell_value:
                    for (nx, ny) in unopened:
                        if (nx, ny) not in moves or moves[(nx, ny)] != 'flag':
                            moves[(nx, ny)] = 'click'
                            safe_tiles.add((nx, ny))

                # Rule 2: All unopened are mines
                elif len(unopened) + len(flagged) == cell_value:
                    for (nx, ny) in unopened:
                        moves[(nx, ny)] = 'flag'
                        mines.add((nx, ny))

    # Second pass - advanced patterns (e.g., 1-2 pattern)
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if grid[y][x] == '1':
                neighbors = get_neighbors(grid, x, y)
                unopened = [(nx, ny) for nx, ny in neighbors if grid[ny][nx] == 'unopened']
                if len(unopened) == 2:
                    # Check if one of the unopened tiles is adjacent to a '2'
                    for (nx, ny) in unopened:
                        for (nx2, ny2) in get_neighbors(grid, nx, ny):
                            if grid[ny2][nx2] == '2':
                                # The other unopened tile is safe
                                other_tile = next((tx, ty) for (tx, ty) in unopened if (tx, ty) != (nx, ny))
                                if other_tile not in moves:
                                    moves[other_tile] = 'click'
                                    safe_tiles.add(other_tile)
                                break

    # Convert moves to list and filter conflicts
    final_moves = []
    for (x, y), action in moves.items():
        final_moves.append((x, y, action))
    
    # Generate guesses using probability if needed
    if not final_moves:
        guesses = calculate_probabilities(grid, remaining_mines - len(mines), safe_tiles)
    else:
        guesses = []

    return final_moves, guesses

def calculate_probabilities(grid, remaining_mines, safe_tiles):
    # Calculate probabilities for each unopened tile
    unopened_tiles = [(x, y) for y in range(len(grid)) for x in range(len(grid[0])) if grid[y][x] == 'unopened']
    probabilities = {}

    for (x, y) in unopened_tiles:
        if (x, y) in safe_tiles:
            probabilities[(x, y)] = 0  # Already safe
        else:
            # Count the number of adjacent numbered cells
            adjacent_numbers = 0
            for (nx, ny) in get_neighbors(grid, x, y):
                if grid[ny][nx].isdigit():
                    adjacent_numbers += 1
            probabilities[(x, y)] = adjacent_numbers

    # Normalize probabilities based on remaining mines
    total_weight = sum(probabilities.values())
    if total_weight > 0:
        for tile in probabilities:
            probabilities[tile] = (probabilities[tile] / total_weight) * remaining_mines

    # Sort tiles by lowest probability
    sorted_tiles = sorted(probabilities.keys(), key=lambda t: probabilities[t])
    return sorted_tiles

def perform_moves(moves):
    for x, y, action in moves:
        if action == 'click':
            pyautogui.click(x, y)
        elif action == 'flag':
            pyautogui.rightClick(x, y)

def handle_guesses(guesses):
    if guesses:
        guess = guesses[0]  # Pick the safest guess
        pyautogui.click(guess[0], guess[1])

def solve_minesweeper(grid, remaining_mines):
    while True:
        moves, guesses = solve_grid(grid, remaining_mines)
        if not moves:
            if guesses:
                handle_guesses(guesses)
            else:
                break  # No more moves or guesses
        else:
            perform_moves(moves)
        
        # Update grid and remaining_mines after performing moves
        # (This requires integration with your game interface)
        grid = update_grid_from_game()
        remaining_mines = update_remaining_mines_from_game()

def update_grid_from_game():
    # Implement this function to read the current grid state from the game
    pass

def update_remaining_mines_from_game():
    # Implement this function to read the remaining mine count from the game
    pass

# Initial call to start solving
# if __name__ == "__main__":
#     initial_grid = [['unopened' for _ in range(30)] for _ in range(16)]  # Example grid
#     remaining_mines = 99  # Example mine count
#     solve_minesweeper(initial_grid, remaining_mines)
