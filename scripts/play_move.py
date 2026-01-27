import chess
import json
import os
import random
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

def get_visual_board(board):
    # Mirror the board for white/black? No, standard view is fine.
    # Replace pieces with emojis for more "visual" feel?
    # Actually ASCII is safer for compatibility, but let's try a mix.
    board_str = str(board)
    return f"```\n{board_str}\n```"

def update_log(new_entry):
    if not os.path.exists(LOG_FILE):
        header = "# ChessBot Move Log ♟️\n\nThis file is the diary of the autonomous chess games played by ChessBot.\nEach entry records the move, the time, and a short commentary.\nGames never end—when one side wins, the board resets and a new game begins.\n\n---\n"
        content = ""
    else:
        with open(LOG_FILE, "r") as f:
            lines = f.readlines()
        
        header_end = 0
        for i, line in enumerate(lines):
            if line.strip() == "---":
                header_end = i + 1
                break
        
        if header_end == 0:
             header = "# ChessBot Move Log ♟️\n\n...\n\n---\n"
             content = "".join(lines)
        else:
            header = "".join(lines[:header_end])
            content = "".join(lines[header_end:])

    with open(LOG_FILE, "w") as f:
        f.write(header)
        f.write(new_entry)
        f.write(content)

def start_new_game_log(board):
    now = datetime.now(IST).strftime("%Y-%m-%d %H:%M IST")
    entry = f"\n\n## 🏁 New Game Started ({now})\n\n"
    update_log(entry)

def log_move(move, board, reset=False, san_move=None, commentary=""):
    now = datetime.now(IST).strftime("%Y-%m-%d %H:%M IST")
    if reset:
        outcome = board.outcome()
        winner = "White" if outcome and outcome.winner == chess.WHITE else "Black" if outcome and outcome.winner == chess.BLACK else "Draw"
        entry = f"\n### {now}\n**🏆 Game Over! Result: {winner}**\n\n{get_visual_board(board)}\n\n📝 Commentary: The game has concluded. The board will reset for a new match.\n\n---\n"
    else:
        entry = f"\n### {now}\n**Move: {san_move}**\n\n{get_visual_board(board)}\n\n📝 Commentary: {commentary}\n\n---\n"
    update_log(entry)

def generate_commentary(board, move):
    piece = board.piece_at(move.from_square)
    piece_name = chess.piece_name(piece.piece_type).capitalize() if piece else "A piece"
    target_square = chess.square_name(move.to_square)
    
    commentary = ""
    if board.is_capture(move):
        commentary = f"{piece_name} captures on {target_square}."
    elif board.is_check():
        commentary = f"{piece_name} moves to {target_square}, putting the opponent in check!"
    else:
        commentary = f"{piece_name} moves to {target_square}."
    
    return commentary

def update_readme(board, san_move=None, reset=False):
    if reset:
        status = "♟️ Game reset – new match started."
    elif san_move:
        status = f"Last move: **{san_move}**"
    else:
        status = "Game ongoing."

    if os.path.exists(README_FILE):
        with open(README_FILE, "r") as f:
            lines = f.readlines()
    else:
        lines = []

    new_lines = []
    skip = False
    status_found = False
    for line in lines:
        if "## Current Status" in line:
            new_lines.append(line)
            new_lines.append(f"{status}\n\n{get_visual_board(board)}\n")
            skip = True
            status_found = True
            continue
        if skip:
            if line.startswith("See [") or line.strip() == "---" or line.startswith("## "):
                new_lines.append(line)
                skip = False
            continue
        new_lines.append(line)

    if not status_found:
        new_lines.append("\n## Current Status\n")
        new_lines.append(f"{status}\n\n{get_visual_board(board)}\n")

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
        return

    legal_moves = list(board.legal_moves)
    if not legal_moves:
        log_move(None, board, reset=True)
        board.reset()
        save_board(board)
        start_new_game_log(board)
        update_readme(board, reset=True)
        return

    move = random.choice(legal_moves)
    san_move = board.san(move)
    commentary = generate_commentary(board, move)
    
    board.push(move)
    save_board(board)
    log_move(move, board, san_move=san_move, commentary=commentary)
    update_readme(board, san_move=san_move)
    print(f"Played move: {san_move}")

if __name__ == "__main__":
    main()
