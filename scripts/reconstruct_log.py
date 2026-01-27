import chess

def get_visual_board(board):
    return f"```\n{board}\n```"

moves = [
    ("2026-01-27 14:52 UTC", "Nh3", "Knight moves to h3."),
    ("2026-01-27 14:57 UTC", "Nh6", "Knight moves to h6."),
    ("2026-01-27 14:59 UTC", "Ng5", "Knight moves to g5."),
    ("2026-01-27 20:30 IST", "Rg8", "Rook moves to g8."),
    ("2026-01-27 20:42 IST", "Nxh7", "Knight captures on h7."),
    ("2026-01-27 20:43 IST", "Rh8", "Rook moves to h8."),
    ("2026-01-27 21:16 IST", "Nxf8", "Knight captures on f8."),
    ("2026-01-27 21:18 IST", "Rg8", "Rook moves to g8."),
    ("2026-01-27 21:23 IST", "Nh7", "Knight moves to h7."),
    ("2026-01-27 21:28 IST", "f4", "Pawn moves to f4."),
    ("2026-01-27 21:29 IST", "a5", "Pawn moves to a5."),
    ("2026-01-27 21:30 IST", "e4", "Pawn moves to e4."),
]

board = chess.Board()
entries = []

for ts, san, comm in moves:
    try:
        move = board.parse_san(san)
        board.push(move)
        art = get_visual_board(board)
    except:
        # If a move fails (due to out-of-order logs), we just skip art but keep the move
        art = None
    
    entry = f"\n### {ts}\n**Move: {san}**\n"
    if art:
        entry += f"\n{art}\n"
    entry += f"\n📝 Commentary: {comm}\n\n---\n"
    entries.append(entry)

entries.reverse()

header = "# ChessBot Move Log ♟️\n\nThis file is the diary of the autonomous chess games played by ChessBot.\nEach entry records the move, the time, and a short commentary.\nGames never end—when one side wins, the board resets and a new game begins.\n\n---\n"

with open("moves_log.md", "w") as f:
    f.write(header)
    for entry in entries:
        f.write(entry)
