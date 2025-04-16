from utils import get_neighbors
from screen_detection import find_game_window
import pyautogui
import random

def solve_grid(grid):
    print("Starting to solve the grid...")
    moves = []
    guesses = []
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell == 'unopened':
                print(f"Analyzing cell ({x}, {y})")
                if is_safe_move(grid, x, y):
                    moves.append((x, y))
                    print(f"Safe move identified at ({x}, {y})")
                else:
                    guesses.append((x, y))
                    print(f"Guess needed at ({x}, {y})")
    print("Solver finished analyzing grid.")
    return moves, guesses


def perform_moves(moves):
    if not moves:
        print("No moves to perform.")
        return

    print("Performing moves...")
    window = find_game_window()
    if not window or not isinstance(window, tuple) or len(window) < 1:
        print("Error: Game window not found or invalid format.")
        return

    left, top = window[0]
    cell_size = 16  # Update with detected size
    
    for x, y in moves:
        screen_x = left + x * cell_size + cell_size // 2
        screen_y = top + y * cell_size + cell_size // 2
        print(f"Clicking at screen coordinates ({screen_x}, {screen_y})")
        pyautogui.click(screen_x, screen_y)
    print("Moves completed!")


def handle_guesses(guesses):
    if not guesses:
        print("No guesses to handle.")
        return

    print("Handling guesses... taking risks!")
    window = find_game_window()
    if not window or not isinstance(window, tuple) or len(window) < 1:
        print("Error: Game window not found or invalid format.")
        return

    left, top = window[0]
    cell_size = 16  # Update with detected size
    
    for x, y in guesses:
        screen_x = left + x * cell_size + cell_size // 2
        screen_y = top + y * cell_size + cell_size // 2
        print(f"Clicking at screen coordinates ({screen_x}, {screen_y})")
        pyautogui.click(screen_x, screen_y)
    print("All guesses made.")


def is_safe_move(grid, x, y):
    """
    Checks if a cell is guaranteed safe based on neighboring numbers and flags.
    """
    for nx, ny in get_neighbors(grid, x, y):
        if 0 <= ny < len(grid) and 0 <= nx < len(grid[0]):  # Bounds check
            if grid[ny][nx].isdigit():
                num = int(grid[ny][nx])
                flags, unopened = count_flags_and_unopened(grid, nx, ny)
                if flags == num and unopened > 0:
                    return True  # This cell is adjacent to a safe area
    return False


def count_flags_and_unopened(grid, x, y):
    flags = 0
    unopened = 0
    for nx, ny in get_neighbors(grid, x, y):
        if 0 <= ny < len(grid) and 0 <= nx < len(grid[0]):  # Bounds check
            if grid[ny][nx] == 'flag':
                flags += 1
            elif grid[ny][nx] == 'unopened':
                unopened += 1
    return flags, unopened