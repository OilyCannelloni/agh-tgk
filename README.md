This is a Pygame-based puzzle adventure inspired by [Untrusted](https://untrustedgame.com/), developed as part of the **TGK course at AGH University**.

You play as a **cybernetic knight** — a warrior who uses both skill and code to manipulate the environment, outsmart hazards, and move forward through a series of challenging levels.

---

## Gameplay Overview

Your goal in each level is to reach the **exit door**. But it might not be so easy — the path is filled with challenges.

### Controls

- `W`, `A`, `S`, `D` — Move
- `E` — Use object
- `T` — Hack object


### Key Mechanics

- **In-Game Terminal**: Use the terminal to write and execute Python code that modifies objects in the world.
- **Hackable Objects**: Some objects can be modified through code — change their properties, unlock areas, or disable threats.
- **Usable Items**: Certain objects can be used directly (e.g., levers, switches).
- **Hazards**: Enemies or traps may kill you. If that happens, you restart the level.
- **Progression**: Each level ends with a door that leads to the next.

---

## Getting Started

### Requirements

- Python 3.10+
- Pygame 2.5.2+

### Installation

1. **Clone the repository**:
   ```
   git clone https://github.com/OilyCannelloni/agh-tgk.git
   cd agh-tgk
   ```

2. **Install dependencies**:
    ```
   pip install -r requirements.txt
   ```

3. **Launch the game**:
    ```
   python main.py
   ```