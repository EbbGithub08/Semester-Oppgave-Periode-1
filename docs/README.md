# Pygame Platformer

Et 2D platformer-spill laget i **Python med Pygame**.  
Flere verdener, timer, deaths, leaderboard og en ekstra **Demon World**.

---

## Gameplay
- Løp og hopp gjennom levels
- Unngå fiender, lava og spikes
- Fullfør alle levels i en verden for å vinne
- Tiden din blir målt

---

## Verdener
- World 1–3
- Tutorial
- Demon World (egen musikk + leaderboard)

---

## Leaderboard
- Lagres lokalt med SQLite
- Beste tid per spiller per verden
- Top scores vises i menyen

---

## Kontroller
- **A / ←** – venstre  
- **D / →** – høyre  
- **W / ↑ / SPACE** – hopp  
- **R** – restart level  
- **ESC** – tilbake / meny  
- **ENTER** – lagre navn etter win  

---

## Teknisk
- Python
- Pygame
- SQLite
- Level-data lagret med pickle

---

## Hvordan kjøre
```bash
pip install pygame
python main.py
