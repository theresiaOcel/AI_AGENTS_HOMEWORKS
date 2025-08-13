from agent import QLearningAgent
from environment import FrozenLakeEnv
import numpy as np


class Visualizer:
    def __init__(self, 
                 agent: QLearningAgent, 
                 map_name: str = "8x8",
                 is_slippery: bool = False,
                 max_steps = 300,
                 max_episodes = 10,
                 seed: int = 42):
        """Inicializace vizualizátoru."""
        self.agent = agent
        self.environment = FrozenLakeEnv(map_name=map_name, 
                                        is_slippery=is_slippery, 
                                        render_mode="human",
                                        seed=seed
                                        )
        self.max_steps = max_steps
        self.max_episodes = max_episodes
        self.seed = seed

    def visualize(self) -> None:
        """Vizualizace chování agenta v prostředí."""
        epsilon = self.agent.epsilon
        self.agent.set_epsilon(0.0)

        try:
            for ep in range(self.max_episodes):
                state, _ = self.environment.reset()
                total_reward = 0.0

                for step in range(self.max_steps):
                    action = int(np.argmax(self.agent.q_table[state]))
                    observation, reward, terminated, truncated, _ = self.environment.step(action)
                    done = terminated or truncated

                    total_reward += reward
                    state = observation

                    if done:
                        break
                
                print(f"Episode {ep+1}/{self.max_episodes} | reward={total_reward:.0f}")
        finally:
            self.agent.set_epsilon(epsilon)
            self.environment.close()
