# Q-Learning Agent pro FrozenLake (Gymnasium)

Tento projekt implementuje **Q-learning** agenta, který se učí řešit prostředí **FrozenLake-v1** z knihovny [Gymnasium](https://gymnasium.farama.org/).  
Obsahuje kompletní pipeline od tréninku, přes vyhodnocení až po vizualizaci naučeného chování.

---

## 📂 Struktura projektu

```
.
├── agent.py         # Implementace Q-learning agenta
├── environment.py   # Wrapper pro prostředí FrozenLake
├── history.py       # Ukládání Q-tabulek a grafů odměn
├── main.py          # Hlavní skript pro spuštění tréninku, evaluace a vizualizace
├── train.py         # Tréninková smyčka a evaluace agenta
├── visualize.py     # Vizualizace chování naučeného agenta
├── requirements.txt # Závislosti projektu
```

---

## 🚀 Instalace

1. **Vytvoření a aktivace virtuálního prostředí** (doporučeno):
   ```bash
   python -m venv venv
   source venv/bin/activate   # Linux / macOS
   venv\Scripts\activate      # Windows
   ```

2. **Instalace závislostí**:
   ```bash
   pip install -r requirements.txt
   ```

---

## ⚙️ Spuštění tréninku

Hlavní skript `main.py` provede:
1. Inicializaci prostředí a agenta  
2. Trénink na zadaný počet epizod  
3. Vyhodnocení úspěšnosti  
4. Uložení Q-tabulek a grafů  
5. Vizualizaci chování agenta

Spuštění:
```bash
python main.py
```

Parametry pro trénink (mapa, počet epizod, epsilon decay apod.) lze upravit přímo v `main.py`:
```python
MAP_NAME = "8x8"        # velikost mapy
IS_SLIPPERY = True      # zda je led klouzavý
EPISODES = 200000       # počet tréninkových epizod
ALPHA = 0.2             # learning rate
GAMMA = 0.95            # discount faktor
```

---

## 📊 Výstupy

Po tréninku se vygenerují:
- **Q-tabule** (`.npy` a `.csv`) – uložené v `lecture9/q_tables/`
- **Graf průběhu odměn** (`.png`) – uložený v `lecture9/figures/`
- **Výpis evaluace** v konzoli
- **Vizualizace běhu agenta** v okně prostředí

---

## 🧠 Jak funguje Q-learning v tomto projektu
- Agent se učí **hodnoty stav-akce** (Q-values) na základě získaných odměn
- Používá **ε-greedy** strategii pro vyvažování průzkumu a využití
- Aktualizace Q-tabulek podle vzorce:
  \[
  Q(s,a) \leftarrow Q(s,a) + \alpha \cdot \left[ r + \gamma \cdot \max_{a'} Q(s', a') - Q(s,a) \right]
  \]
- Epsilon se postupně snižuje pomocí `epsilon_decay`

---

## 📦 Požadavky
Hlavní knihovny:
- `gymnasium` – prostředí FrozenLake
- `numpy` – práce s Q-tabulkou
- `matplotlib` – vizualizace odměn
- `pygame` – render prostředí

Podrobný seznam je v [`requirements.txt`](requirements.txt).

---
