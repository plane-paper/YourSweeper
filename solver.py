from utils import get_neighbors
import pyautogui
import random

def solve_grid(grid):
    moves = []
    guesses = []
    safe_tiles = set()
    
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell.isdigit():
                cell_value = int(cell)
                neighbors = get_neighbors(grid, x, y)
                unopened = [(nx, ny) for nx, ny in neighbors if grid[ny][nx] == 'unopened']
                flagged = [(nx, ny) for nx, ny in neighbors if grid[ny][nx] == 'flag']
                
                # If number of unopened equals the cell value, flag them
                if len(unopened) + len(flagged) == cell_value and len(flagged) < cell_value:
                    for nx, ny in unopened:
                        moves.append((nx, ny, 'flag'))
                        safe_tiles.discard((nx, ny))
                
                # If number of flagged neighbors equals the cell value, click the rest
                if len(flagged) == cell_value:
                    for nx, ny in unopened:
                        moves.append((nx, ny, 'click'))
                        safe_tiles.add((nx, ny))

                # Advanced pattern: Check for 1-2 patterns
                if cell_value == 1 and len(unopened) == 2:
                    for nx, ny in unopened:
                        if any(grid[ny+dy][nx+dx] == '2' for dx, dy in get_neighbors(grid, nx, ny)):
                            guesses.append((nx, ny))
                
                # Track risky guesses for unresolved tiles
                if len(unopened) > 0 and len(flagged) < cell_value and (x, y) not in guesses:
                    guesses.extend(unopened)

    # Probability analysis: pick safest guess if needed
    if guesses and safe_tiles:
        guess_probabilities = {guess: sum(1 for dx, dy in get_neighbors(grid, *guess) if grid[dy][dx].isdigit()) for guess in guesses}
        best_guess = min(guess_probabilities, key=guess_probabilities.get)
        guesses = [best_guess]

    return moves, guesses

def perform_moves(moves):
    for x, y, action in moves:
        if action == 'click':
            pyautogui.click(x, y)
        elif action == 'flag':
            pyautogui.rightClick(x, y)

def handle_guesses(guesses):
    guess = random.choice(guesses)
    pyautogui.click(guess[0], guess[1])