from __future__ import annotations
import gymnasium as gym
from typing import Optional, Tuple, Dict, Any

class FrozenLakeEnv:
    def __init__(self, map_name: str = "8x8", is_slippery: bool = False, render_mode: Optional[str] = None, seed: Optional[int] = None):
        """Inicializace prostředí FrozenLake."""

        self.map_name = map_name
        self.is_slippery = is_slippery
        self.render_mode = render_mode
        self.seed = seed

        # vytvoření prostředí
        self.env = gym.make(
            "FrozenLake-v1", 
            map_name=self.map_name, 
            is_slippery=self.is_slippery, 
            render_mode=self.render_mode
        )

        # nastavení seed
        self._next_reset_seed = self.seed if self.seed is not None else None
        
        # uložení počtu stavů a akcí
        self.n_states = self.env.observation_space.n
        self.n_actions = self.env.action_space.n

    def reset(self) -> Tuple[int, Dict[str, Any]]:
        """Reset prostředí a vrátí počáteční stav."""
        if self._next_reset_seed is not None:
            state, info = self.env.reset(seed=self._next_reset_seed)
            self._next_reset_seed = None
        else:
            state, info = self.env.reset()
        return int(state), info
    
    def step(self, action: int) -> Tuple[int, float, bool, bool, Dict[str, Any]]:
        """Provede krok v prostředí a vrátí nové stavy."""
        observation, reward, terminated, truncated, info = self.env.step(action)
        return int(observation), float(reward), bool(terminated), bool(truncated), info
    
    def close(self) -> None:
        """Zavře prostředí."""
        self.env.close()
    
    def sample_action(self) -> int:
        """Vrátí náhodnou akci (0 až n_actions-1).
        Pro testovací účely.
        TODO: po dokončení testování, smazat tuto metodu."""
        return int(self.env.action_space.sample())