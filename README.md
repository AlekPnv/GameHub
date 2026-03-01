# 🎮 GameHub

Eine Sammlung von 8 klassischen Spielen, gebaut mit Python & Pygame.

## Spiele

| Spiel | Steuerung |
|-------|-----------|
| 🔴 Connect 4 | Maus |
| 🍪 Cookie Clicker | Maus |
| 🐦 Flappy Bird | `Space` zum Fliegen, `R` zum Neustart |
| 🔢 2048 | Pfeiltasten, `R` Neustart, `Q` Beenden |
| 🏓 Ping Pong | Spieler 1: `W`/`S` · Spieler 2: `↑`/`↓` |
| ✂️ Rock Paper Scissors | Maus |
| 🐍 Snake | Pfeiltasten |
| ❌ Tic Tac Toe | Maus, `R` Neustart, `Q` Beenden |

## Voraussetzungen

- Python 3.8 oder neuer → [python.org](https://www.python.org/downloads/)

## Installation & Start

```bash
# 1. Repository herunterladen
git clone https://github.com/DEIN-USERNAME/GameHub.git
cd GameHub

# 2. Abhängigkeiten installieren
pip install -r requirements.txt

# 3. Hub starten
python GameHub/Hub.py
```

> Einzelne Spiele können auch direkt gestartet werden, z.B.:
> ```bash
> python GameHub/Snake/Snake.py
> ```

## Projektstruktur

```
GameHub/
├── Hub.py                  ← Hauptmenü
├── Connect_4/
├── Cookie_Clicker/
├── Flappy_Bird/
├── Game_2048/
├── Ping_Pong/
├── RPS/
├── Snake/
└── Tic_Tac_Toe/
```
