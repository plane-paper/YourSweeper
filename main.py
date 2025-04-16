import cv2
import pyautogui
import numpy as np
from screen_detection import detect_grid
from solver import solve_grid, perform_moves, handle_guesses
from utils import print_grid, save_grid_to_file

def main():
    print("Starting Minesweeper Bot...")

    # Capture screen (replace with live capture if needed)
    screen = pyautogui.screenshot()
    screen = np.array(screen)
    
    if screen is None:
        print("Failed to load screen!")
        return
    print(f"Full screenshot dimensions: height={screen.shape[0]}, width={screen.shape[1]}")

    # Detect the grid from the screenshot
    grid = detect_grid(screen)
    if not grid:
        print("Failed to detect Minesweeper grid!")
        return

    # Convert grid of tuples to a grid of placeholder strings
    string_grid = [['?' for _ in row] for row in grid]

    # Print and save the grid
    print_grid(string_grid)
    save_grid_to_file(string_grid)

    # Solve the grid
    moves, guesses = solve_grid(grid)

    # Perform moves first, guesses last
    perform_moves(moves)
    handle_guesses(guesses)

    print("Minesweeper Bot finished!")

if __name__ == "__main__":
    main()