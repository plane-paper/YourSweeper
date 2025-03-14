import pyautogui
import cv2
import numpy as np

CELL_COLORS = {
    (0, 0, 255): '1',    # Blue
    (0, 128, 0): '2',     # Green
    (255, 0, 0): '3',     # Red
    (0, 0, 128): '4',     # Dark Blue
    (128, 0, 0): '5',     # Brown
    (0, 128, 128): '6',   # Cyan
    (0, 0, 0): '7',       # Black
    (128, 128, 128): '8'  # Gray
}


def find_game_window():
    screenshot = pyautogui.screenshot()
    screen_array = np.array(screenshot)
    
    # Convert screenshot to grayscale
    gray_screen = cv2.cvtColor(screen_array, cv2.COLOR_BGR2GRAY)
    
    # Load Minesweeper window template
    try:
        template = cv2.imread('minesweeper_template.png', 0)
        result = cv2.matchTemplate(gray_screen, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        
        if max_val > 0.8:
            top_left = max_loc
            bottom_right = (top_left[0] + template.shape[1], top_left[1] + template.shape[0])
            return top_left, bottom_right
        else:
            print("Minesweeper window not found!")
            return None
    except Exception as e:
        print(f"Error loading template: {e}")
        return None


def detect_grid(screen):
    # Convert screen to grayscale
    gray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
    
    # Apply edge detection to find grid lines
    edges = cv2.Canny(gray, 50, 150)
    
    # Find contours of the grid
    contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cell_size = 0
    grid_cells = []
    
    # Extract cells based on contours
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        if 20 < w < 50 and 20 < h < 50:  # Assume cell sizes are within this range
            cell_size = max(cell_size, w, h)
            grid_cells.append((x, y))
    
    # Sort cells to form a proper grid
    grid_cells = sorted(grid_cells, key=lambda cell: (cell[1] // cell_size, cell[0] // cell_size))
    
    # Determine grid size
    rows = len(set(y for _, y in grid_cells))
    cols = len(set(x for x, _ in grid_cells))
    
    # Build the grid layout with cell recognition
    grid = []
    try:
        for y in range(rows):
            row = []
            for x in range(cols):
                index = y * cols + x
                if index >= len(grid_cells):
                    row.append('unknown')
                    continue
                cell_x, cell_y = grid_cells[index]
                cell_crop = screen[cell_y:cell_y+cell_size, cell_x:cell_x+cell_size]
                avg_color = tuple(np.mean(cell_crop, axis=(0, 1)).astype(int))
                
                if np.all(cell_crop > 200):
                    row.append('unopened')
                elif np.all(cell_crop < 50):
                    row.append('flag')
                else:
                    row.append(CELL_COLORS.get(avg_color, 'unknown'))
            grid.append(row)
    except IndexError as e:
        print(f"Grid parsing error: {e}")
        return []
    
    return grid
