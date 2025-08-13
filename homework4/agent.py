import numpy as np
from typing import Optional

class QLearningAgent:
    def __init__(self, 
                 n_states: int, 
                 n_actions: int, 
                 alpha: float = 0.1, 
                 gamma: float = 0.99, 
                 epsilon: float = 1.0, 
                 seed: Optional[int] = None):
        
        """
        Inicializace Q-learning agenta.
        Args:
            n_states: počet stavů v prostředí,
            n_actions: počet možných akcí v prostředí,
            alpha: learning rate,
            gamma: discount factor,
            epsilon: míra náhodnosti,
            seed: seed
        """

        self.n_states = n_states
        self.n_actions = n_actions
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        
        self.random_num = np.random.default_rng(seed)

        # Inicializace Q-tabulky, inicializace na nuly
        self.q_table = np.zeros((n_states, n_actions))
    
    def choose_action(self, state: int) -> int:
        if self.random_num.random() < self.epsilon:
            return int(self.random_num.integers(0, self.n_actions))
        q = self.q_table[state]
        best = np.flatnonzero(q == q.max())
        return int(self.random_num.choice(best))

    
    def learn(self, state: int, action: int, reward: float, next_state: int, done: bool) -> None:
        """Q-learning update"""
        bn = 0.0 if done else np.max(self.q_table[next_state])
        td_target = reward + self.gamma * bn
        td_error = td_target - self.q_table[state, action]
        self.q_table[state, action] += self.alpha * td_error

    def decay_epsilon(self, decay: float, min_epsilon: float) -> None:
        """Sníží hodnotu epsilonu"""
        self.epsilon = max(min_epsilon, self.epsilon * decay)
    
    def set_epsilon(self, epsilon: float) -> None:
        """Nastaví hodnotu epsilonu"""
        self.epsilon = float(epsilon)
    