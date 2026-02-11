import os
import time

# Pygame is optional; fallback to terminal mode if not installed
try:
    import pygame
except ImportError:  # pragma: no cover - runtime fallback
    pygame = None

# import msvcrt  # Windows non-blocking input
from board import Board
from utils_display import print_board_colored, print_board_basic
from render import ensure_screen, render

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# def get_input_non_blocking():
#     # Windows specific non-blocking input
#     if msvcrt.kbhit():
#         key = msvcrt.getch()
#         try:
#             char = key.decode('utf-8').lower()
#             return char
#         except:
#             return None
#     return None

# def run_terminal(board_size: int = 10):
#     game_board = Board(size=board_size)
#     print(f"Initialized game board of size {board_size}x{board_size}.")

#     last_move_time = time.time()
#     move_delay = 1.0  # 1 second between each move

#     print("Initial State (basic):")
#     print_board_basic(game_board)
#     print("Initial State (colored):")
#     print_board_colored(game_board)
#     print("Controls: W (Up), A (Left), S (Down), D (Right) or CTRL+C to quit")

#     try:
#         while not game_board.is_gameOver():
#             current_time = time.time()

#             # 1. Input Handling (Non-blocking)
#             key = get_input_non_blocking()
#             if key:
#                 direction = None
#                 if key == 'w':
#                     direction = 'UP'
#                 elif key == 's':
#                     direction = 'DOWN'
#                 elif key == 'a':
#                     direction = 'LEFT'
#                 elif key == 'd':
#                     direction = 'RIGHT'

#                 if direction:
#                     try:
#                         game_board.get_snake().set_direction(direction)
#                         print(f"Direction changed to {direction}")
#                     except ValueError:
#                         pass  # Ignore invalid directions (like 180 turn)

#             # 2. Game Logic (Every 1 second)
#             if current_time - last_move_time > move_delay:
#                 os.system('cls' if os.name == 'nt' else 'clear')  # Clear for smooth animation
#                 game_board.update()
#                 print_board_colored(game_board)
#                 last_move_time = current_time

#             # Small pause to avoid CPU overload
#             time.sleep(0.01)

#     except KeyboardInterrupt:
#         print("\nGame stopped by user.")

#     print("GAME OVER")


def run_pygame(board_size: int = 10, cell_size: int = 32, fps: int = 8):
    if pygame is None:
        print("Pygame is not installed; falling back to terminal mode.")
        # run_terminal(board_size)
        return

    pygame.init()
    game_board = Board(size=board_size)
    screen = ensure_screen(board_size, cell_size)
    clock = pygame.time.Clock()
    running = True
    first_render = True

    print("Pygame mode: arrows or WASD to steer, ESC to quit")

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_ESCAPE,):
                    running = False
                elif event.key in (pygame.K_UP, pygame.K_w):
                    game_board.get_snake().set_direction('UP')
                elif event.key in (pygame.K_DOWN, pygame.K_s):
                    game_board.get_snake().set_direction('DOWN')
                elif event.key in (pygame.K_LEFT, pygame.K_a):
                    game_board.get_snake().set_direction('LEFT')
                elif event.key in (pygame.K_RIGHT, pygame.K_d):
                    game_board.get_snake().set_direction('RIGHT')
        print (game_board.get_snake_vision())
        if first_render:
            render(game_board, screen, cell_size=cell_size)
            time.sleep(20.5)  # Pause before first render
            first_render = False
            clock.tick(fps)
            continue

        if not game_board.is_gameOver():
            game_board.update()
        else:
            running = False
        render(game_board, screen, cell_size=cell_size)
        clock.tick(fps)

    print("Final Score:", game_board.get_score())  # Placeholder for actual score
    pygame.quit()


if __name__ == "__main__":
    # Toggle here: True for Pygame, False for terminal ASCII
    USE_PYGAME = True
    BOARD_SIZE = 10

    if USE_PYGAME:
        run_pygame(board_size=BOARD_SIZE, cell_size=32, fps=8)
    # else:
    #     run_terminal(board_size=BOARD_SIZE)