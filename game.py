import time

# Pygame is optional; fallback to terminal mode if not installed
try:
    import pygame
except ImportError:  # pragma: no cover - runtime fallback
    pygame = None

from board import Board
from render import ensure_screen, render
from agent import Agent


def get_state_tuple(vision_dict):
    res = []
    # On force l'ordre pour que l'IA ne soit pas perdue
    for direction in ["UP", "DOWN", "LEFT", "RIGHT"]:
        res.extend(vision_dict[direction])
    return tuple(res)


def run_pygame(
    board_size: int = 10,
    cell_size: int = 32,
    fps: int = 8,
    mode: str = "train",
    model_path: str | None = None,
    nb_sessions: int = 100
):
    if pygame is None:
        # print("Pygame is not installed; falling back to terminal mode.")
        return

    pygame.init()
    game_board = Board(size=board_size)
    game_agent = Agent()

    # Configure epsilon decay so epsilon reaches epsilon_min after nb_sessions
    # formula: epsilon_decay = (epsilon_min / epsilon_start) ** (1 / nb_sessions)
    try:
        epsilon_start = float(getattr(game_agent, "epsilon", 1.0))
        epsilon_min = float(getattr(game_agent, "epsilon_min", 0.01))
        if nb_sessions > 0 and epsilon_start > 0:
            game_agent.epsilon_decay = (epsilon_min / epsilon_start) ** (1.0 / nb_sessions)
    except Exception:
        # keep agent defaults on any unexpected issue
        pass

    if mode == "game" and model_path:
        game_agent.load_q_table(model_path)
        game_agent.epsilon = 0.0

    screen = ensure_screen(board_size, cell_size)
    clock = pygame.time.Clock()
    running = True
    first_render = True
    counter_games = 0
    training_sessions = 0
    training_enabled = mode != "game" and mode != "player game"

    # print("Pygame mode: arrows or WASD to steer, ESC to quit")

    while running:
        if mode == "player game":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_ESCAPE,):
                        running = False
                    elif event.key in (pygame.K_UP, pygame.K_w):
                        game_board.get_snake().set_direction("UP")
                    elif event.key in (pygame.K_DOWN, pygame.K_s):
                        game_board.get_snake().set_direction("DOWN")
                    elif event.key in (pygame.K_LEFT, pygame.K_a):
                        game_board.get_snake().set_direction("LEFT")
                    elif event.key in (pygame.K_RIGHT, pygame.K_d):
                        game_board.get_snake().set_direction("RIGHT")
        else:
            # print (f"Step 1: sending state to agent...\n\n")
            old_state = get_state_tuple(game_board.get_snake_vision())

            # print (f"Step 2: receiving action from agent...\n")
            action = game_agent.choose_action(old_state)
            directions = ["UP", "DOWN", "LEFT", "RIGHT"]
            game_board.get_snake().set_direction(directions[action])

        if mode == "game" or mode == "player game":
            if first_render:
                render(game_board, screen, cell_size=cell_size)
                time.sleep(1.5)
                first_render = False
                clock.tick(fps)
                continue

        if not game_board.is_gameOver():
            reward = game_board.update()
            done = game_board.is_gameOver()
            new_state = get_state_tuple(game_board.get_snake_vision())
            if training_enabled:
                game_agent.learn(old_state, action, reward, new_state, done)
        else:
            counter_games += 1
            if training_enabled:
                if counter_games == 1:
                    training_sessions += 1
                    counter_games = 0
                    if training_sessions == nb_sessions:
                        game_agent.save_q_table(f"models/q_table{training_sessions}.pkl")
                        running = False
            game_board.reset()
        if mode == "game" or mode == "player game":
            render(game_board, screen, cell_size=cell_size)
            clock.tick(fps)
    pygame.quit()
