import sqlite3

DB_NAME = "chat_history.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    # tabel chat
    c.execute('''
        CREATE TABLE IF NOT EXISTS chat (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role TEXT,
            content TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    # tabel character
    c.execute('''
        CREATE TABLE IF NOT EXISTS character (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            race TEXT,
            char_class TEXT,
            level INTEGER,
            ac INTEGER,
            current_hp INTEGER,
            max_hp INTEGER,
            temp_hp INTEGER,
            stats TEXT,
            armor TEXT,
            weapon TEXT,
            inventory TEXT,
            coin INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

# ===== CHAT =====
def add_message(role, content):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO chat (role, content) VALUES (?, ?)", (role, content))
    conn.commit()
    conn.close()

def get_messages():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT role, content FROM chat ORDER BY id ASC")
    messages = c.fetchall()
    conn.close()
    return messages

def reset_chat():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("DELETE FROM chat")
    conn.commit()
    conn.close()

# ===== CHARACTER =====
def save_character(data: dict):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    # hapus biar cuma ada 1 karakter aktif
    c.execute("DELETE FROM character")
    c.execute("""
        INSERT INTO character 
        (name, race, char_class, level, ac, current_hp, max_hp, temp_hp, stats, armor, weapon, inventory, coin)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        data["name"], data["race"], data["char_class"], data["level"], data["ac"],
        data["current_hp"], data["max_hp"], data["temp_hp"],
        str(data["stats"]), data["armor"], data["weapon"], str(data["inventory"]), data["coin"]
    ))
    conn.commit()
    conn.close()

def load_character():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM character ORDER BY id DESC LIMIT 1")
    row = c.fetchone()
    conn.close()
    return row
