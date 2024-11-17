import sqlite3

def initialize_db():
    conn = sqlite3.connect('education.db')  # Create a new database file (or connect to an existing one)
    cursor = conn.cursor()

    # Create students table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        grade TEXT NOT NULL,
        notes TEXT
    )
    ''')

    # Create progress table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS progress (
        id INTEGER PRIMARY KEY,
        student_id INTEGER,
        subject TEXT NOT NULL,
        score REAL NOT NULL,
        FOREIGN KEY (student_id) REFERENCES students (id)
    )
    ''')

    # Insert dummy data
    cursor.execute("INSERT OR IGNORE INTO students (id, name, grade, notes) VALUES (1, 'John Doe', '5th', '')")
    cursor.execute("INSERT OR IGNORE INTO progress (student_id, subject, score) VALUES (1, 'Math', 85)")
    cursor.execute("INSERT OR IGNORE INTO progress (student_id, subject, score) VALUES (1, 'Science', 90)")

    conn.commit()
    conn.close()

if __name__ == "__main__":
    initialize_db()
