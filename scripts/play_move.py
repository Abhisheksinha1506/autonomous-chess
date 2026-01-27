import chess
import json
import os
import subprocess
from datetime import datetime, timezone, timedelta

# IST is UTC + 5:30
IST = timezone(timedelta(hours=5, minutes=30))

BOARD_FILE = "board_state.json"
LOG_FILE = "moves_log.md"
README_FILE = "README.md"

def load_board():
    if os.path.exists(BOARD_FILE):
        try:
            with open(BOARD_FILE, "r") as f:
                data = json.load(f)
                fen = data.get("fen")
                return chess.Board(fen)
        except Exception:
            return chess.Board()
    else:
        return chess.Board()

def save_board(board):
    with open(BOARD_FILE, "w") as f:
        json.dump({"fen": board.fen()}, f)

def start_new_game_log(board):
    now = datetime.now(IST).strftime("%Y-%m-%d %H:%M IST")
    with open(LOG_FILE, "a") as f:
        f.write(f"\n---\n\n## New Game (Started: {now})\n")

def log_move(move, board, reset=False, san_move=None):
    now = datetime.now(IST).strftime("%Y-%m-%d %H:%M IST")
    with open(LOG_FILE, "a") as f:
        if reset:
            outcome = board.outcome()
            winner = "White" if outcome and outcome.winner == chess.WHITE else "Black" if outcome and outcome.winner == chess.BLACK else "Draw"
            f.write(f"\n### {now}\nGame Over! Result: {winner}\n")
            f.write("📝 Commentary: The game has concluded. The board will reset for a new match.\n")
        else:
            f.write(f"\n### {now}\n**{san_move}**\n")
            f.write(f"📝 Commentary: {generate_commentary(board, move)}\n")

def generate_commentary(board, move):
    piece = board.piece_at(move.from_square)
    piece_name = chess.piece_name(piece.piece_type).capitalize() if piece else "A piece"
    target_square = chess.square_name(move.to_square)
    
    if board.is_capture(move):
        return f"{piece_name} captures on {target_square}."
    if board.is_check():
        return f"{piece_name} moves to {target_square}, putting the opponent in check!"
    return f"{piece_name} moves to {target_square}."

def update_readme(board, san_move=None, reset=False):
    if reset:
        status = "♟️ Game reset – new match started."
    elif san_move:
        status = f"Last move: **{san_move}**"
    else:
        status = "Game ongoing."

    with open(README_FILE, "r") as f:
        lines = f.readlines()

    new_lines = []
    skip = False
    for line in lines:
        if "## Current Status" in line:
            new_lines.append(line)
            new_lines.append(f"{status}\n")
            skip = True
            continue
        if skip:
            if line.startswith("See [") or line.strip() == "":
                new_lines.append(line)
                skip = False
            continue
        new_lines.append(line)

    with open(README_FILE, "w") as f:
        f.writelines(new_lines)

def main():
    board = load_board()

    if board.is_game_over():
        log_move(None, board, reset=True)
        board.reset()
        save_board(board)
        start_new_game_log(board)
        update_readme(board, reset=True)
        print("Game over, resetting board.")
        return

    # Simple logic: pick the first legal move
    # In a more advanced version, we could use an engine or track history to avoid repeats
    legal_moves = list(board.legal_moves)
    if not legal_moves:
        log_move(None, board, reset=True)
        board.reset()
        save_board(board)
        start_new_game_log(board)
        update_readme(board, reset=True)
        print("No legal moves, resetting board.")
        return

    move = legal_moves[0]
    san_move = board.san(move)
    
    log_move(move, board, san_move=san_move)
    board.push(move)
    save_board(board)
    update_readme(board, san_move=san_move)
    print(f"Played move: {san_move}")

if __name__ == "__main__":
    main()
