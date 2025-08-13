from environment import FrozenLakeEnv
from agent import QLearningAgent
from train import Trainer
from visualize import Visualizer
from history import History

import matplotlib.pyplot as plt
import os

SEED = 42
MAP_NAME = "8x8"
IS_SLIPPERY = True
RENDER_MODE_TRAIN = None
EPSILON = 1.0
ALPHA = 0.2
GAMMA = 0.95
#MAX_STEPS = 300
MAX_STEPS = 500
EPSILON_MIN = 0.10
EPSILON_DECAY = 0.99995

#EPISODES = 10000
EPISODES = 200000

if __name__ == "__main__":
    env = FrozenLakeEnv(map_name=MAP_NAME, is_slippery=IS_SLIPPERY, render_mode=RENDER_MODE_TRAIN, seed=SEED)
    agent = QLearningAgent(n_states=env.n_states, 
                           n_actions=env.n_actions, 
                           seed=SEED, 
                           epsilon=EPSILON,
                           alpha=ALPHA,
                           gamma=GAMMA)
    trainer = Trainer(environment=env, 
                      agent=agent, 
                      max_steps_ep=MAX_STEPS, 
                      epsilon_start=EPSILON,
                      epsilon_min = EPSILON_MIN,
                      epsilon_decay=EPSILON_DECAY)
    
    # Trénink agenta
    print("Starting training...")
    rewards = trainer.train(n_episodes=EPISODES)
    print("Training completed.")

    # Vyhodnocení agenta
    print("Evaluating agent...")
    avg_reward, success_rate = trainer.evaluate(n_episodes=100)
    print(f"\nEVAL -> avg_reward={avg_reward:.3f}, success_rate={success_rate*100:.1f}%")
    print("Evaluation completed.")

    hist = History()
    hist.save_q_table(q_table=agent.q_table, map_name=MAP_NAME, episodes=EPISODES)
    hist.save_learning_rewards(rewards=rewards, map_name=MAP_NAME, episodes=EPISODES)

    env.close()

    # vizualizace výsledků
    print("Visualizing agent's behavior...")
    visualizer = Visualizer(agent=agent, 
                            map_name=MAP_NAME,
                            is_slippery=IS_SLIPPERY,
                            max_steps = 300,
                            max_episodes = 5,
                            seed=SEED)
    visualizer.visualize()
    print("Visualization completed.")

        