from agent import QLearningAgent
from environment import FrozenLakeEnv
from typing import Tuple, List

class Trainer:
    def __init__(self, 
             environment: FrozenLakeEnv,
             agent: QLearningAgent,
             max_steps_ep: int = 300,
             epsilon_start: float = 1.0,
             epsilon_min: float = 0.05,
             epsilon_decay: float = 0.995):
        """Inicializace tréninkového procesu."""

        self.environment = environment
        self.agent = agent
        self.max_steps = max_steps_ep
        self.epsilon_start = epsilon_start
        self.epsilon_min = epsilon_min
        self.epsilon_decay = epsilon_decay

        self.agent.set_epsilon(self.epsilon_start)

        self.log_ep = 100
    
    def train(self, n_episodes: int) -> List[float]:
        """Trénink agenta v prostředí."""
        ep_rewards: List[float] = [] # pro uložení odměn v každé epizodě

        # tréninkový cyklus (do maximálního počtu epizod)
        for ep in range(n_episodes): 
            state, _ = self.environment.reset() # začátek epizody (uvedení do počátečního stavu)
            total_reward = 0.0 # vynuluju si odměnu pro tuto epizodu

            # omezení počtu kroků v epiizodě --> aby nedošlo k nekonečnému cyklu
            for _ in range(self.max_steps):
                action = self.agent.choose_action(state) # agent vybere akci
                observation, reward, terminated, truncated, _ = self.environment.step(action) # provedení akce a získání infa
                done = terminated or truncated

                # provede se učení agenta na základě získaných informací
                self.agent.learn(state=state, action=action, reward=reward, next_state=observation, done=done)
                total_reward += reward # přičtení odměny k celkové odměně v epizodě
                state = observation # aktualizace stavu

                # pokud je done, pak ukončení epizody
                if done:
                    break
            
            self.agent.decay_epsilon(self.epsilon_decay, self.epsilon_min) # snížení epsilonu 
            ep_rewards.append(total_reward)

            # logování průběhu po x epizodách
            if (ep + 1) % self.log_ep == 0:
                avg_reward = sum(ep_rewards[-self.log_ep:]) / min(self.log_ep, len(ep_rewards))
                print(f"Episode {ep + 1}/{n_episodes} | Average Reward: {avg_reward:.2f} | Epsilon: {self.agent.epsilon:.2f}")
        
        return ep_rewards
        
    def evaluate(self, n_episodes: int = 20) -> Tuple[float, float]:
        """Vyhodnocení agenta v prostředí."""
        epsilon = self.agent.epsilon
        self.agent.set_epsilon(0.0)

        succces_ep_count = 0 # počet úspěšných epizod
        reward_sum = 0.0 # součet odměn v epizodách

        # průchod epizodami
        for _ in range(n_episodes):
            state, _ = self.environment.reset() # nastavení počátečního stavu
            total_reward = 0.0

            for _ in range(self.max_steps):
                action = int(self.agent.q_table[state].argmax()) # výběr akce z q-tabulky s nejvyšší hodnotou q pro aktuýální stav
                observation, reward, terminated, truncated, _ = self.environment.step(action) # provedení akce a získání infa
                done = terminated or truncated

                total_reward += reward # přičtení odměny
                state = observation # aktualizace stavu

                if done: # pokdu je epizoda ukončena
                    if reward > 0: # a agent dosáhl úspěchu
                        succces_ep_count += 1 # pak se zvýší počet úspěšných epizod
                    break

            reward_sum += total_reward 

        self.agent.set_epsilon(epsilon) # vrátí epsilon do původního stavu

        avg_reward = reward_sum / n_episodes # výpočet průměrné hodnoty na epizodu
        success_rate = succces_ep_count / n_episodes # podíl epizod, kde agent uspěl
        return avg_reward, success_rate


