import os
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

class History:
    def __init__(self):
         self.dt = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    def save_q_table(self, q_table, map_name: str, episodes: int):
        os.makedirs("lecture9/q_tables", exist_ok=True)
        qtable_path_npy = f"lecture9/q_tables/frozenlake_{map_name}_ep_{episodes}_{self.dt}_qtable.npy"
        qtable_path_csv = f"lecture9/q_tables/frozenlake_{map_name}_ep_{episodes}_{self.dt}_qtable.csv"

        np.save(qtable_path_npy, q_table)
        np.savetxt(qtable_path_csv, q_table, delimiter=",")  

        print(f"Q-table uložena do:\n- {qtable_path_npy}\n- {qtable_path_csv}")
    
    def save_learning_rewards(self, rewards: list, map_name: str, episodes: int):
        os.makedirs("lecture9/figures", exist_ok=True)
        fig_path = f"lecture9/figures/rewards_{map_name}_episodes_{episodes}_{self.dt}.png"

        plt.figure()
        plt.plot(rewards)
        plt.xlabel("Epizoda")
        plt.ylabel("Odměna za epizodu")
        plt.title("Vývoj odměn v průběhu tréninku")
        plt.tight_layout()
        plt.savefig(fig_path, dpi = 150)
        plt.close()