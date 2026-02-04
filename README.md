# Autonomous Chess Repository ♟️

[![Chess Simulation](https://github.com/Abhisheksinha1506/autonomous-chess/actions/workflows/chess.yml/badge.svg)](https://github.com/Abhisheksinha1506/autonomous-chess/actions/workflows/chess.yml)
[![Status](https://img.shields.io/badge/Status-Ongoing-green?style=flat-square)](https://github.com/Abhisheksinha1506/autonomous-chess/actions/workflows/chess.yml)

This repository is a living chessboard. It plays chess by itself, forever.
Every commit is a move. Every reset is a new game.

---

## How It Works
- Two invisible players (White and Black) take turns.
- Each commit represents one move.
- The game continues until checkmate or stalemate.
- When the game ends, the board resets and a new game begins.
- No move is repeated in the same game context, exploring the vast chess state space.

---

## Current Status
Last move: **Na6**

```
. . . k . . . .
. . . . . . . .
n . . . p . K .
. . . . P . . .
. . . . . . n .
. . . . . . . .
. . . . . . . .
. . . . . . . .
```
See [moves_log.md](moves_log.md) for the diary of moves.
See [principles.md](principles.md) for the philosophy behind this project.
See [ARCHITECTURE.md](ARCHITECTURE.md) for a visual guide to how the system works.

---

## Layman’s Analogy
Imagine two friends playing chess forever. They write down every move in a diary. When one wins, they start a new game immediately. This repo is that diary—an endless story of chess unfolding automatically.

---

## Files
- **[board_state.json](board_state.json):** Current board position in chess notation (FEN).
- **[moves_log.md](moves_log.md):** Human-readable diary of moves.
- **[principles.md](principles.md):** Explains the rules and philosophy.
- **[.github/workflows/chess.yml](.github/workflows/chess.yml):** Automation script that makes the repo play itself.
- **[scripts/play_move.py](scripts/play_move.py):** Logic for choosing moves and updating the board.
