import sqlite3
import hashlib

def get_db_connection():
    return sqlite3.connect("university.db")

def initialize_db(conn):
    cursor = conn.cursor()

    # جدول الطلاب
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS students (
        student_id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        level TEXT NOT NULL,
        department TEXT NOT NULL
    )
    """)

    # Complaints table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS complaints (
        complaint_id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id TEXT,
        description TEXT NOT NULL,
        status TEXT CHECK(status IN ('pending', 'reviewed', 'closed')) DEFAULT 'pending',
        type TEXT NOT NULL DEFAULT 'complaint',
        priority TEXT CHECK(priority IN ('Low', 'Medium', 'High')) DEFAULT 'medium',
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (student_id) REFERENCES students(student_id)
    )
    """)

    # جدول الأدمن
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS admins (
        username TEXT PRIMARY KEY,
        password TEXT NOT NULL,
        first_login INTEGER DEFAULT 1
    )
    """)

    # بيانات الطلاب الافتراضية
    students_data = [
        ("30404141601782", "Esraa elmaghraby", "UG_31159886@ics.tanta.edu.eg", "3", "CS"),
        ("30407271601155", "zyad ramadan", "UG_31159668@ics.tanta.edu.eg", "3", "CS"),
        ("30401011609065" , "Mayar Muhamed" , "UG_31159354@ics.tanta.edu.eg" , "3" , "CS")
    ]

    cursor.executemany("""
    INSERT OR IGNORE INTO students (student_id, name, email, level, department)
    VALUES (?, ?, ?, ?, ?)
    """, students_data)

    conn.commit()
    cursor.close()

def create_default_admin(conn, username, password):
    cursor = conn.cursor()
    hashed = hashlib.sha256(password.encode()).hexdigest()
    cursor.execute("INSERT OR IGNORE INTO admins (username, password) VALUES (?, ?)", (username, hashed))
    conn.commit()
    cursor.close()

def authenticate(username, password, conn):
    cursor = conn.cursor()
    hashed = hashlib.sha256(password.encode()).hexdigest()
    cursor.execute("SELECT * FROM admins WHERE username = ? AND password = ?", (username, hashed))
    admin = cursor.fetchone()
    cursor.close()
    return (admin is not None, admin[2] == 1 if admin else False)

def change_password(username, old_password, new_password, conn):
    cursor = conn.cursor()
    hashed_old = hashlib.sha256(old_password.encode()).hexdigest()
    cursor.execute("SELECT * FROM admins WHERE username = ? AND password = ?", (username, hashed_old))
    if cursor.fetchone():
        hashed_new = hashlib.sha256(new_password.encode()).hexdigest()
        cursor.execute("UPDATE admins SET password = ?, first_login = 0 WHERE username = ?", (hashed_new, username))
        conn.commit()
        return True
    return False

def validate_student_id_only(student_id, conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students WHERE student_id = ?", (student_id,))
    student = cursor.fetchone()
    cursor.close()
    return student is not None

def load_data(conn):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM complaints
        ORDER BY timestamp DESC
    """)
    rows = cursor.fetchall()
    cursor.close()
    return rows
