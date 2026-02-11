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
from agent import Agent

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def run_pygame(board_size: int = 10, cell_size: int = 32, fps: int = 8):
    if pygame is None:
        print("Pygame is not installed; falling back to terminal mode.")
        # run_terminal(board_size)
        return

    pygame.init()
    game_board = Board(size=board_size)
    game_agent = Agent()
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
        print (f"Step 1: sending state to agent\n\n")

        print (f"Step 2: receiving action from agent\n")
        action = game_agent.choose_action(game_board.get_snake_vision())

        match action:
            case 0:
                game_board.get_snake().set_direction('UP')
            case 1:
                game_board.get_snake().set_direction('DOWN')
            case 2:
                game_board.get_snake().set_direction('LEFT')
            case 3:
                game_board.get_snake().set_direction('RIGHT')
                
        if first_render:
            render(game_board, screen, cell_size=cell_size)
            time.sleep(1.5)  # Pause before first render
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
