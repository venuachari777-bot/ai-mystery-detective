import sqlite3

DB_NAME = "game_database.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Player progress table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS player_stats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            player_name TEXT DEFAULT 'Detective',
            current_level INTEGER DEFAULT 1,
            score INTEGER DEFAULT 0,
            cases_solved INTEGER DEFAULT 0
        )
    ''')
    
    # Clues collected log
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS collected_clues (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            level_num INTEGER,
            clue_id TEXT,
            clue_name TEXT
        )
    ''')
    
    # First time default record insert cheyadam
    cursor.execute('SELECT COUNT(*) FROM player_stats')
    if cursor.fetchone()[0] == 0:
        cursor.execute('INSERT INTO player_stats (player_name, current_level, score, cases_solved) VALUES (?, ?, ?, ?)', ('Detective', 1, 0, 0))
    
    conn.commit()
    conn.close()

def get_stats():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT current_level, score, cases_solved FROM player_stats WHERE id = 1')
    row = cursor.fetchone()
    conn.close()
    return {"level": row[0], "score": row[1], "cases_solved": row[2]} if row else {"level": 1, "score": 0, "cases_solved": 0}

def update_score_on_solve(level_num):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    # Prathi correct case solve ki 100 points
    cursor.execute('''
        UPDATE player_stats 
        SET score = score + 100, 
            cases_solved = cases_solved + 1,
            current_level = ?
        WHERE id = 1
    ''', (level_num,))
    conn.commit()
    conn.close()

def log_clue(level_num, clue_id, clue_name):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO collected_clues (level_num, clue_id, clue_name) VALUES (?, ?, ?)', (level_num, clue_id, clue_name))
    conn.commit()
    conn.close()

def reset_db_progress():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('UPDATE player_stats SET current_level = 1, score = 0, cases_solved = 0 WHERE id = 1')
    cursor.execute('DELETE FROM collected_clues')
    conn.commit()
    conn.close()