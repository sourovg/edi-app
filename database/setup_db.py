import sqlite3

import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Access the DB_PATH variable
db_path = os.getenv("DB_PATH", "./data/education_app.db")  # Default to ./data/education_app.db if not set
print(f"Database path: {db_path}")


def initialize_db():
    conn = sqlite3.connect(db_path)  # Create a new database file (or connect to an existing one)
    cursor = conn.cursor()

    # Cleanup old tables (if necessary)
    cursor.execute('DROP TABLE IF EXISTS students')
    cursor.execute('DROP TABLE IF EXISTS progress')
    cursor.execute('DROP TABLE IF EXISTS psychometrics')

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
    
    # Create psychometrics table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS psychometrics (
        id INTEGER PRIMARY KEY,
        student_id INTEGER,
        trait TEXT,
        score REAL,
        FOREIGN KEY (student_id) REFERENCES students (id)
    )
    ''')

    # Insert dummy data
    cursor.execute("INSERT OR IGNORE INTO students (id, name, grade, notes) VALUES (1, 'John Doe', '5th', '')")
    cursor.executemany('''
    INSERT INTO students (id, name, grade, notes) VALUES (?, ?, ?,?)
    ''', [
        (2, 'Mat Vue', '5th',''),
        (3, 'Smith Jones', '6th',''),
        (4, 'Sanjana Sethi', '5th',''),
        (5, 'Nancy Doe', '6th','')
    ])

    cursor.execute("INSERT OR IGNORE INTO progress (student_id, subject, score) VALUES (1, 'Math', 85)")
    cursor.execute("INSERT OR IGNORE INTO progress (student_id, subject, score) VALUES (1, 'Science', 90)")

    cursor.executemany('''
    INSERT INTO progress (student_id, subject, score) VALUES (?, ?, ?)
    ''', [
        (2, 'Math', 89),
        (2, 'Science', 45),
        (3, 'Math', 98),
        (3, 'Science', 75),
        (4, 'Math', 79),
        (4, 'Science', 91),
        (5, 'Math', 72),
        (5, 'Science', 82)
    ])
    
    cursor.executemany('''
    INSERT INTO psychometrics (student_id, trait, score) VALUES (?, ?, ?)
    ''', [
        (1, 'focus', 89),
        (1, 'Intelligence', 80),
        (1, 'Aptitude', 75),
        (1, 'Values', 75),
        (1, 'Motivation', 79),
        (1, 'Behavior', 80),
        (1, 'Values', 72),
        (1, 'Skills', 12),
        (2, 'focus', 87),
        (2, 'Intelligence', 82),
        (2, 'Aptitude', 71),
        (2, 'Values', 79),
        (2, 'Motivation', 69),
        (2, 'Behavior', 50),
        (2, 'Values', 92),
        (2, 'Skills', 42),
        (3, 'focus', 99),
        (3, 'Intelligence', 60),
        (3, 'Aptitude', 65),
        (3, 'Values', 55),
        (3, 'Motivation', 89),
        (3, 'Behavior', 60),
        (3, 'Values', 78),
        (3, 'Skills', 85),
        (4, 'Motivation', 75),
        (4, 'Behavior', 83),
        (4, 'Values', 82),
        (4, 'Skills', 92),
        (5, 'Values', 82),
        (5, 'Skills', 62),
        (5, 'Motivation', 69),
        (5, 'Behavior', 85),
        (5, 'Values', 70),
        (5, 'Skills', 80),
    ])

    conn.commit()
    conn.close()

if __name__ == "__main__":
    initialize_db()
