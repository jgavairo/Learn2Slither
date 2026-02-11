import random
import numpy as np

class Agent :
    q_table : dict[tuple[int, ...], list[float]]
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

    def get_q_values(self, state: str) -> list[float]:
        """
        Get Q-values for a given state, initializing if not present.
        """
        if state not in self.q_table:
            self.q_table[state] = [0.0 for _ in self.actions]
        return self.q_table[state]

    def choose_action(self, state):
        """
        Choose an action based on epsilon-greedy strategy.
        """
        print (f"[AGENT] Choosing action for state:\n{state}\nEpsilon: {self.epsilon:.4f}")
        if random.random() < self.epsilon:
            print (f"[AGENT] Exploring: choosing random action")
            return random.choice(self.actions)
        else:
            q_values = self.get_q_values(state)
            return np.argmax(q_values)
        

    def learn(self, old_state, action, reward, new_state, done):
        """
        Update Q-values based on the action taken and reward received.
        """
        q_values = self.get_q_values(old_state)
        old_q_value = q_values[action]

        if done:
            max_future_q = 0
        else:
            # On demande à la Q-Table le meilleur score de l'état suivant
            next_q_values = self.get_q_values(new_state)
            max_future_q = max(next_q_values)
        
        # 3. La formule magique (Bellman)
        # On calcule la nouvelle estimation : Reward actuel + 90% du futur
        new_q_value = old_q_value + self.lr * (reward + self.gamma * max_future_q - old_q_value)
        
        # 4. On enregistre cette nouvelle valeur dans notre mémoire
        self.q_table[old_state][action] = new_q_value

        # 5. Si la partie est finie, on réduit un peu le hasard (Epsilon Decay)
        if done:
            if self.epsilon > self.epsilon_min:
                self.epsilon *= self.epsilon_decay

    