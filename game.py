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
    for direction in ["UP", "DOWN", "LEFT", "RIGHT"]:
        res.extend(vision_dict[direction])
    return tuple(res)


def run_pygame(
    board_size: int = 10,
    cell_size: int = 32,
    fps: int = 8,
    mode: str = "train",
    model_path: str | None = None,
    nb_sessions: int = 100,
    headless: bool = False
):
    if pygame is None:
        print("Pygame is not installed. Please install pygame to run the game with graphics.")
        return

    pygame.init()
    game_board = Board(size=board_size)
    game_agent = Agent()

    try:
        epsilon_start = float(getattr(game_agent, "epsilon", 1.0))
        epsilon_min = float(getattr(game_agent, "epsilon_min", 0.01))
        if nb_sessions > 0 and epsilon_start > 0:
            game_agent.epsilon_decay = (epsilon_min / epsilon_start) ** (1.0 / nb_sessions)
    except Exception:
        pass

    if mode == "game" and model_path:
        game_agent.load_q_table(model_path)
        game_agent.epsilon = 0.0

    if not headless:
        screen = ensure_screen(board_size, cell_size)
    clock = pygame.time.Clock()
    running = True
    first_render = True
    training_sessions = 0
    training_enabled = mode != "game" and mode != "player game"
    best_score = 0
    step = 0

    while running:
        step += 1
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
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_ESCAPE,):
                        running = False
            old_state = get_state_tuple(game_board.get_snake_vision())
            action = game_agent.choose_action(old_state)
            directions = ["UP", "DOWN", "LEFT", "RIGHT"]
            if mode != "train":
                game_board.display_vision()
                print(f"Action chosen: {directions[action]}")
                print(f"Current score: {game_board.get_score()}")
                print(f"Current step: {step}")
            game_board.get_snake().set_direction(directions[action])

        if not headless:
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
            if training_enabled:
                training_sessions += 1
                if training_sessions == nb_sessions:
                    game_agent.save_q_table(f"models/q_table{training_sessions}.pkl")
                    print(f"[TRAINING] {nb_sessions} sessions atteintes. Entraînement terminé.")
                    running = False
            current_score = game_board.get_score()
            if current_score > best_score:
                best_score = current_score
            game_board.reset()
        if not headless:
            render(game_board, screen, cell_size=cell_size)
            clock.tick(fps)

    print("Best Score:", best_score) 
    pygame.quit()
