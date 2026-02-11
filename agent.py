import random


class Agent :
    q_table : dict[str, list[float]]
    actions : list[int] 

    def __init__(self) -> None:
        self.q_table = {}
        self.actions = [0, 1, 2, 3] # UP, DOWN, LEFT, RIGHT

        # Hyperparamètres
        self.lr = 0.1        # Alpha : vitesse à laquelle l'IA remplace l'ancienne info
        self.gamma = 0.9     # Gamma : importance accordée aux récompenses futures
        self.epsilon = 1.0   # Taux d'exploration (100% au début)
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995 # Diminue le hasard à chaque partie

    def choose_action(self, state):
        """
        Choose an action based on epsilon-greedy strategy.
        """
        print (f"[AGENT] Choosing action for state:\n{state}\n\n")
        return random.choice(self.actions)


    