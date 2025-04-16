import pyautogui
import cv2
import numpy as np

# Color definitions for minesweeper cells (BGR format)
CELL_COLORS = {
    (255, 0, 0): '1',    # Blue
    (0, 128, 0): '2',    # Green
    (0, 0, 255): '3',    # Red
    (128, 0, 0): '4',    # Dark Blue
    (0, 0, 128): '5',    # Brown/Dark Red
    (0, 128, 128): '6',  # Cyan
    (0, 0, 0): '7',      # Black
    (128, 128, 128): '8' # Gray
}

# Thresholds for unopened and flagged cells
UNOPENED_LOWER = np.array([200, 200, 200])
UNOPENED_UPPER = np.array([255, 255, 255])
FLAG_LOWER = np.array([0, 0, 200])
FLAG_UPPER = np.array([50, 50, 255])


def find_game_window():
    print("Searching for Minesweeper window...")
    screenshot = pyautogui.screenshot()
    screen_array = np.array(screenshot)
    
    # Save the screenshot for debugging
    cv2.imwrite('Workspace/debug_screenshot.png', cv2.cvtColor(screen_array, cv2.COLOR_RGB2BGR))
    print("Saved debug screenshot as 'debug_screenshot.png'.")

    # Convert screenshot to grayscale
    gray_screen = cv2.cvtColor(screen_array, cv2.COLOR_BGR2GRAY)
    
    # Load Minesweeper window template
    try:
        template = cv2.imread('Template/minesweeper_template.png', 0)
        if template is None:
            print("Error: Template image 'minesweeper_template.png' not found!")
            return None
        
        print(f"Template dimensions: width={template.shape[1]}, height={template.shape[0]}")
        result = cv2.matchTemplate(gray_screen, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        
        print(f"Template matching result: max_val={max_val}, max_loc={max_loc}")
        cv2.imwrite('Workspace/template_matching_result.png', (result * 255).astype(np.uint8))  # Save result for debugging
        
        if max_val > 0.6:  # Lowered threshold
            print("Minesweeper window found!")
            top_left = max_loc
            # Adjust bottom_right to include the full Minesweeper window
            bottom_right = (top_left[0] + 800, top_left[1] + 600)  # Adjust these values as needed
            
            # Validate coordinates
            height, width = gray_screen.shape
            if bottom_right[0] > width:
                bottom_right = (width, bottom_right[1])
            if bottom_right[1] > height:
                bottom_right = (bottom_right[0], height)
            
            print(f"Adjusted game window coordinates: top_left={top_left}, bottom_right={bottom_right}")
            return top_left, bottom_right
        else:
            print(f"Minesweeper window not found! max_val={max_val}")
            return None
    except Exception as e:
        print(f"Error loading template: {e}")
        return None
    
def detect_grid(screen):
    print("Detecting Minesweeper grid...")
    window = find_game_window()
    if not window:
        print("Error: Game window not found.")
        return None
    
    top_left, bottom_right = window
    print(f"Game window coordinates: top_left={top_left}, bottom_right={bottom_right}")
    
    # Crop the Minesweeper window
    cropped_screen = screen[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]]
    if cropped_screen.size == 0:
        print(f"Error: Cropped region is empty! top_left={top_left}, bottom_right={bottom_right}")
        return None
    cv2.imwrite('Workspace/debug_cropped_screen.png', cropped_screen)  # Save for debugging
    
    # Convert cropped screen to grayscale
    gray = cv2.cvtColor(cropped_screen, cv2.COLOR_BGR2GRAY)
    print("Converted screen to grayscale.")

    # Apply edge detection to find grid lines
    edges = cv2.Canny(gray, 50, 150)
    print("Applied edge detection.")

    # Find contours of the grid
    contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    print(f"Found {len(contours)} contours.")

    # Draw contours for debugging
    contour_debug = cropped_screen.copy()
    cv2.drawContours(contour_debug, contours, -1, (0, 255, 0), 1)  # Draw all contours in green
    cv2.imwrite('Workspace/debug_contours.png', contour_debug)
    print("Saved debug_contours.png with detected contours.")

    # Filter contours by size and position
    grid_start_y = 100  # Adjust this value based on the position of the grid
    cell_size = 16  # Approximate size of a Minesweeper cell
    filtered_contours = []
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        if 14 < w < 18 and 14 < h < 18 and y > grid_start_y:  # Exclude contours above the grid
            filtered_contours.append(contour)

    print(f"Filtered {len(filtered_contours)} contours matching cell size.")

    # Sort contours into rows
    filtered_contours = sorted(filtered_contours, key=lambda c: cv2.boundingRect(c)[1])  # Sort by y-coordinate
    rows = []
    current_row = []
    last_y = None
    tolerance = cell_size // 2  # Allow some tolerance for misalignment

    for contour in filtered_contours:
        x, y, w, h = cv2.boundingRect(contour)
        if last_y is None or abs(y - last_y) < tolerance:  # Same row
            current_row.append((x, y, w, h))
        else:  # New row
            rows.append(sorted(current_row, key=lambda c: c[0]))  # Sort row by x-coordinate
            current_row = [(x, y, w, h)]
        last_y = y

    if current_row:
        rows.append(sorted(current_row, key=lambda c: c[0]))  # Add the last row

    print(f"Detected grid with {len(rows)} rows and {len(rows[0]) if rows else 0} columns.")

    # Validate grid dimensions
    expected_rows = 16  # Adjust based on the Minesweeper level
    expected_cols = 30  # Adjust based on the Minesweeper level

    if len(rows) != expected_rows or any(len(row) != expected_cols for row in rows):
        print(f"Error: Detected grid dimensions ({len(rows)}x{len(rows[0]) if rows else 0}) do not match expected dimensions ({expected_rows}x{expected_cols}).")
        return None

    # Draw grid cells for debugging
    grid_debug = cropped_screen.copy()
    for row in rows:
        for x, y, w, h in row:
            cv2.rectangle(grid_debug, (x, y), (x + w, y + h), (255, 0, 0), 1)  # Draw rectangles in blue

    cv2.imwrite('Workspace/debug_grid.png', grid_debug)
    print("Saved debug_grid.png with detected grid cells.")

    return rows