import chess
import re
import os

LOG_FILE = "moves_log.md"

def get_visual_board(board):
    return f"```\n{board}\n```"

def repair_log():
    if not os.path.exists(LOG_FILE):
        return

    with open(LOG_FILE, "r") as f:
        content = f.read()

    # Split into entries
    # Entries start with ###
    entries_raw = re.split(r'\n---', content)
    header = entries_raw[0] if not entries_raw[0].startswith('###') else ""
    if header:
        entries_raw = entries_raw[1:]
    else:
        # If the first part IS an entry, try to find the header
        # Actually our header is before the first ---
        header_match = re.search(r'(.*?)---', content, re.DOTALL)
        header = header_match.group(1) if header_match else ""
        entries_raw = re.split(r'\n---', content[len(header):])

    parsed = []
    for entry in entries_raw:
        if not entry.strip() or '###' not in entry: continue
        
        ts_match = re.search(r"### (.*?)\n", entry)
        ts = ts_match.group(1) if ts_match else "Unknown"
        
        move_match = re.search(r"\*\*(.*?)\*\*", entry)
        if not move_match:
            move_match = re.search(r"### .*?\n(.*?)\n", entry)
        
        san = move_match.group(1).replace("Move: ", "").strip() if move_match else "Unknown"
        
        comm_match = re.search(r"📝 Commentary: (.*?)\n", entry)
        comm = comm_match.group(1) if comm_match else "A move was played."
        
        parsed.append({"ts": ts, "san": san, "comm": comm})

    # Chronological
    parsed.reverse()
    
    board = chess.Board()
    final_entries = []
    
    for item in parsed:
        try:
            # Clean up SAN (e.g. "Nh3" might have been logged as "Move: Nh3")
            item['san'] = item['san'].replace("Move: ", "").strip()
            
            # Try to parse the move. If it's illegal, we'll try to find any legal move that matches SAN
            # or just push it if it's the right color, etc. 
            # But let's be simple: if it fails, we keep the move but skip art for that specific one.
            move = board.parse_san(item['san'])
            board.push(move)
            art = get_visual_board(board)
        except Exception:
            art = None # No art for this one if illegal
            
        entry = f"\n### {item['ts']}\n**Move: {item['san']}**\n"
        if art:
            entry += f"\n{art}\n"
        entry += f"\n📝 Commentary: {item['comm']}\n\n---\n"
        final_entries.append(entry)

    # Reverse back
    final_entries.reverse()

    with open(LOG_FILE, "w") as f:
        if not header.strip().startswith("#"):
             f.write("# ChessBot Move Log ♟️\n\nThis file is the diary of the autonomous chess games played by ChessBot.\nEach entry records the move, the time, and a short commentary.\nGames never end—when one side wins, the board resets and a new game begins.\n\n---\n")
        else:
             f.write(header if "---" in header else header + "\n---")
        
        for entry in final_entries:
            f.write(entry)

if __name__ == "__main__":
    repair_log()
