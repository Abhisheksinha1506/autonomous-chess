import os
import json
import chess

FILES = {
    "board_state.json": '{"fen": "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"}',
    "moves_log.md": "# ChessBot Move Log ♟️\n\nThis file is the diary of the autonomous chess games played by ChessBot.\nEach entry records the move, the time, and a short commentary.\nGames never end—when one side wins, the board resets and a new game begins.\n\n---\n",
    "principles.md": "# Principles Behind the Autonomous Chess Repository ♟️\n\nThis repository is a self-sustaining chess simulation.\n\n## Autonomy & Reliability\n- The system is entirely self-contained within GitHub Actions.\n- **Safety Guards:** Every move is mathematically verified.\n- **State Validation:** Validated on every load, with auto-recovery.\n",
    "README.md": "# Autonomous Chess Repository ♟️\n\nThis repository plays chess by itself, forever.\n\n## Current Status\nGame ongoing.\n\nSee [moves_log.md](moves_log.md) for history.\n"
}

def check_integrity():
    healed = []
    
    for filename, default_content in FILES.items():
        if not os.path.exists(filename):
            print(f"🛠️ Healing: {filename} is missing. Restoring default.")
            with open(filename, "w") as f:
                f.write(default_content)
            healed.append(filename)
            
    # Extra check for board_state validity
    if os.path.exists("board_state.json"):
        try:
            with open("board_state.json", "r") as f:
                data = json.load(f)
                chess.Board(data.get("fen"))
        except Exception:
            print("🛠️ Healing: Corrupted board_state.json. Resetting.")
            with open("board_state.json", "w") as f:
                f.write(FILES["board_state.json"])
            healed.append("board_state.json (corrupted)")

    if healed:
        print(f"✅ Self-healing complete. Restored: {', '.join(healed)}")
    else:
        print("🟢 System integrity confirmed. No issues found.")

if __name__ == "__main__":
    check_integrity()
