import questionary
import os
from game import run_pygame


SPEED_OPTIONS = {
    "Fast": 100 // 8,
    "Normal": 1000 // 8,
}


def get_model_list():
    """
    Get the list of available models in the "models" directory.
    """
    models_dir = "models"
    if not os.path.exists(models_dir):
        return []

    model_files = [f for f in os.listdir(models_dir) if f.endswith(".pkl")]
    return model_files


def ask_speed():
    """Ask the user for a speed and return the corresponding game_tick_ms."""
    speed_choice = questionary.select(
        "Choose a speed:", choices=list(SPEED_OPTIONS.keys()) + ["← Back"]
    ).ask()

    if speed_choice is None or speed_choice == "← Back":
        return None

    return SPEED_OPTIONS[speed_choice]


def game_mode_menu():
    q_tables = get_model_list()
    if not q_tables:
        print("No models found. Please train a model first.")
        return

    choices = q_tables + ["← Back"]
    model_choice = questionary.select(
        "Choose a model to load:", choices=choices
    ).ask()

    if model_choice is None or model_choice == "← Back":
        return

    game_tick_ms = ask_speed()
    if game_tick_ms is None:
        return

    model_path = os.path.join("models", model_choice)
    run_pygame(
        mode="game",
        board_size=10,
        cell_size=32,
        game_tick_ms=game_tick_ms,
        model_path=model_path,
    )


def training_mode_menu():
    def validate_sessions(value):
        if value == "":
            return True
        if not value.strip().lstrip("-").isdigit():
            return "Please enter a valid integer."
        if int(value) <= 0:
            return "Number of sessions must be greater than 0."
        return True

    nb_sessions = questionary.text(
        "Enter the number of training sessions \
            (default 100, or 'back' to go back):",
        validate=lambda v: (
            True if v.strip().lower() == "back" else validate_sessions(v)
        ),
    ).ask()

    if nb_sessions is None or nb_sessions.strip().lower() == "back":
        return

    nb_sessions = int(nb_sessions) if nb_sessions.strip() != "" else 100

    second_choice = questionary.confirm(
        "Do you want to run training with display enabled?"
    ).ask()

    if second_choice is None:
        return

    game_tick_ms = 0
    if second_choice:
        game_tick_ms = ask_speed()
        if game_tick_ms is None:
            return

    run_pygame(
        mode="train",
        nb_sessions=nb_sessions,
        game_tick_ms=game_tick_ms,
        headless=not second_choice,
    )


def main_menu():
    """
    Display the main menu and handle user choices.
    """
    choices = ["Game mode", "Training mode", "Player game", "Exit"]

    while True:
        choice = questionary.select("Choose an option:", choices=choices).ask()

        if choice is None or choice == "Exit":
            print("Exiting the game. Goodbye!")
            return -1
        elif choice == "Game mode":
            game_mode_menu()
        elif choice == "Training mode":
            training_mode_menu()
        elif choice == "Player game":
            run_pygame(
                mode="player game",
                board_size=10,
                cell_size=32,
            )
