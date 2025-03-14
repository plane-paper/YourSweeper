from screen_detection import find_game_window, detect_grid
from solver import solve_grid, perform_moves, handle_guesses
import pyautogui
import numpy as np

# Main flow
def main():
    window_coords = find_game_window()
    if window_coords:
        top_left, bottom_right = window_coords
        screen = pyautogui.screenshot(region=(top_left[0], top_left[1], bottom_right[0] - top_left[0], bottom_right[1] - top_left[1]))
        grid = detect_grid(np.array(screen))
        moves, guesses = solve_grid(grid)
        perform_moves(moves)
        if guesses:
            handle_guesses(guesses)

if __name__ == "__main__":
    main()