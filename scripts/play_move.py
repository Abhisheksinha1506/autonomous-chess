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
    """Loads the board from JSON and validates its state."""
    if os.path.exists(BOARD_FILE):
        try:
            with open(BOARD_FILE, "r") as f:
                data = json.load(f)
                fen = data.get("fen")
                board = chess.Board(fen)
                
                # Safety Guard: Validate if the FEN is a legally reachable/valid position
                if board.is_valid():
                    return board
                else:
                    log_system_event("⚠️ Invalid FEN detected. Resetting to standard setup.")
                    return chess.Board()
        except Exception as e:
            log_system_event(f"⚠️ Board load failed: {str(e)}. Resetting state.")
            return chess.Board()
    else:
        return chess.Board()

def save_board(board):
    """Saves the board state atomically to prevent corruption."""
    temp_file = f"{BOARD_FILE}.tmp"
    with open(temp_file, "w") as f:
        json.dump({"fen": board.fen()}, f)
    os.replace(temp_file, BOARD_FILE)

def get_visual_board(board):
    board_str = str(board)
    return f"```\n{board_str}\n```"

def log_system_event(message):
    """Logs internal system errors or state changes to the diary."""
    now = datetime.now(IST).strftime("%Y-%m-%d %H:%M IST")
    entry = f"\n### {now}\n**SYSTEM EVENT**\n\n{message}\n\n---\n"
    update_log(entry)

def update_log(new_entry):
    """Appends to the log file atomically."""
    temp_file = f"{LOG_FILE}.tmp"
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

    with open(temp_file, "w") as f:
        f.write(header)
        f.write(new_entry)
        f.write(content)
    os.replace(temp_file, LOG_FILE)

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
    
    if board.is_capture(move):
        return f"{piece_name} captures on {target_square}."
    elif board.is_check():
        return f"{piece_name} moves to {target_square}, putting the opponent in check!"
    return f"{piece_name} moves to {target_square}."

def update_readme(board, san_move=None, reset=False):
    """Updates the README atomically."""
    temp_file = f"{README_FILE}.tmp"
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

    with open(temp_file, "w") as f:
        f.writelines(new_lines)
    os.replace(temp_file, README_FILE)

def main():
    try:
        board = load_board()

        # Check for Game Over (Checkmate, Stalemate, Insufficient Material, etc.)
        if board.is_game_over():
            log_move(None, board, reset=True)
            board.reset()
            save_board(board)
            start_new_game_log(board)
            update_readme(board, reset=True)
            return

        legal_moves = list(board.legal_moves)
        
        # Safety Guard: If somehow there are no moves but not game over, force reset
        if not legal_moves:
            log_system_event("⚠️ No legal moves found in a non-terminal state. Forcing reset.")
            board.reset()
            save_board(board)
            start_new_game_log(board)
            update_readme(board, reset=True)
            return

        # Play a random move from the list of verified legal moves
        move = random.choice(legal_moves)
        san_move = board.san(move)
        commentary = generate_commentary(board, move)
        
        board.push(move)
        save_board(board)
        log_move(move, board, san_move=san_move, commentary=commentary)
        update_readme(board, san_move=san_move)
        print(f"Played move: {san_move}")

    except Exception as e:
        log_system_event(f"❌ Critical Error during move execution: {str(e)}")
        # Attempt to recover by resetting board
        board = chess.Board()
        save_board(board)
        update_readme(board, reset=True)

if __name__ == "__main__":
    main()
