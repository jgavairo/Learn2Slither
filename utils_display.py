# utils_display.py

def print_board_colored(board):
    """
    Prints the board with colors in the terminal.
    """
    size = board.get_size()
    
    # ANSI Color Codes
    RESET = "\033[0m"
    GREEN = "\033[92m"  # Green Apple
    RED = "\033[91m"    # Red Apple
    BLUE = "\033[94m"   # Snake Head
    CYAN = "\033[96m"   # Snake Body
    GRAY = "\033[90m"   # Empty Board Dot
    
    # Symbols
    SYMBOL_EMPTY = "·"
    SYMBOL_HEAD = "●"
    SYMBOL_BODY = "○"
    SYMBOL_APPLE = "" # Or use '@' if not displayed correctly
    
    # Prepare Grid
    grid = [[f"{GRAY}{SYMBOL_EMPTY}{RESET}" for _ in range(size)] for _ in range(size)]

    # 1. Place Food
    for food in board.get_food():
        x, y = food.get_position()
        if 0 <= x < size and 0 <= y < size:
            if food.get_color() == "GREEN":
                grid[y][x] = f"{GREEN}{SYMBOL_APPLE}{RESET}"
            else:
                grid[y][x] = f"{RED}{SYMBOL_APPLE}{RESET}"

    # 2. Place Snake
    # Use careful checks to avoid crashing if snake is momentarily out of bounds
    snake = board.get_snake()
    if snake:
        snake_body = snake.get_body()
        for i, (x, y) in enumerate(snake_body):
            if 0 <= x < size and 0 <= y < size:
                if i == 0:
                    grid[y][x] = f"{BLUE}{SYMBOL_HEAD}{RESET}"
                else:
                    grid[y][x] = f"{CYAN}{SYMBOL_BODY}{RESET}"

    # 3. Print Header
    print(f"\nGame State [Score: {board.get_score()}] [Alive: {snake.is_alive() if snake else False}]")
    print("  " + " ".join([str(i%10) for i in range(size)])) # Column numbers
    
    # 4. Print Rows
    for y, row in enumerate(grid):
        print(f"{y%10} " + " ".join(row))
    print("-" * (size * 2 + 2))


def print_board_basic(board):
    """Print the board in plain ASCII (no colors). Handy for quick startup logs."""
    size = board.get_size()
    grid = [['.' for _ in range(size)] for _ in range(size)]

    # Food
    for food in board.get_food():
        x, y = food.get_position()
        if 0 <= x < size and 0 <= y < size:
            grid[y][x] = 'G' if food.get_color() == "GREEN" else 'R'

    # Snake
    snake = board.get_snake()
    if snake:
        for i, (x, y) in enumerate(snake.get_body()):
            if 0 <= x < size and 0 <= y < size:
                grid[y][x] = 'H' if i == 0 else 'S'

    # Print
    print("  " + " ".join(str(i % 10) for i in range(size)))
    for y, row in enumerate(grid):
        print(f"{y % 10} " + " ".join(row))
    print()
