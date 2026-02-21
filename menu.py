import questionary
import os
from game import run_pygame

def get_model_list():
    """
    Get the list of available models in the "models" directory.
    """
    models_dir = "models"
    if not os.path.exists(models_dir):
        return []
    
    model_files = [f for f in os.listdir(models_dir) if f.endswith(".pkl")]
    return model_files

def main_menu():
    """
    Display the main menu and handle user choices.
    """
    choices = [
        "Game mode",
        "Training mode",
        "Player game",
        "Exit"
    ]
    choice = questionary.select("Choose an option:", choices=choices).ask()
    
    if choice == "Game mode":
        q_tables = get_model_list()
        if q_tables:
            model_choice = questionary.select("Choose a model to load: ", choices=q_tables).ask()
            model_path = os.path.join("models", model_choice)
            run_pygame(mode="game", board_size=10, cell_size=32, fps=8, model_path=model_path)
        else:
            print("No models found. Please train a model first.")

    elif choice == "Training mode":
        nb_sessions = questionary.text("Enter the number of training sessions: (default 100)").ask()
        if nb_sessions == "":
            nb_sessions = 100
        second_choice = questionary.confirm("Do you want to run training with display enabled?").ask()
        # Run training in headless mode by default to speed up learning
        run_pygame(mode="train", nb_sessions=int(nb_sessions), headless=not second_choice)
    elif choice == "Player game":
        run_pygame(mode="player game", board_size=10, cell_size=32, fps=8)
    elif choice == "Exit":
        print("Exiting the game. Goodbye!")
        return -1