import sqlite3

# Initialize the database and create table if not exists
def init_db():
    conn = sqlite3.connect("candidates.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS submitted_emails (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE ,score INT
        )
    """)
    conn.commit()
    conn.close()

# Check if email already exists in the table
def email_exists(email):
    conn = sqlite3.connect('candidates.db')
    c = conn.cursor()
    c.execute('SELECT * FROM submitted_emails WHERE email = ?', (email,))
    result = c.fetchone()
    conn.close()
    return result is not None

# Insert new email into the table
def insert_email(email):
    try:
        conn = sqlite3.connect('candidates.db')
        cursor = conn.cursor()
        cursor.execute("INSERT OR IGNORE INTO submitted_emails (email, score) VALUES (?, ?)", (email, 0))
        conn.commit()
        conn.close()
    except Exception as e:
        print("Insert error:", e)

def get_leaderboard():
    conn = sqlite3.connect('candidates.db')
    cursor = conn.cursor()
    cursor.execute("SELECT email, score FROM submitted_emails ORDER BY score DESC")
    leaderboard = cursor.fetchall()
    conn.close()
    return leaderboard

def update_score(email, score):
    conn = sqlite3.connect("candidates.db")
    c = conn.cursor()
    c.execute("UPDATE submitted_emails SET score = ? WHERE email = ?", (score, email))
    conn.commit()
    conn.close()