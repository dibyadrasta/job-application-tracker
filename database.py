import sqlite3

DATABASE_NAME = "applications.db"


def get_connection():
    return sqlite3.connect(DATABASE_NAME)


def initialize_database():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company TEXT NOT NULL,
            role TEXT NOT NULL,
            date_applied TEXT,
            status TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


def add_application(company, role, date_applied, status):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO applications
        (company, role, date_applied, status)
        VALUES (?, ?, ?, ?)
    """, (company, role, date_applied, status))

    conn.commit()
    conn.close()


def get_applications():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, company, role, date_applied, status
        FROM applications
        ORDER BY id DESC
    """)

    applications = cursor.fetchall()

    conn.close()

    return applications


def update_application(
    application_id,
    company,
    role,
    date_applied,
    status
):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE applications
        SET company = ?,
            role = ?,
            date_applied = ?,
            status = ?
        WHERE id = ?
    """, (
        company,
        role,
        date_applied,
        status,
        application_id
    ))

    conn.commit()
    conn.close()


def delete_application(application_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM applications
        WHERE id = ?
    """, (application_id,))

    conn.commit()
    conn.close()


def search_applications(search_text="", status="All"):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
        SELECT id, company, role, date_applied, status
        FROM applications
        WHERE (company LIKE ? OR role LIKE ?)
    """

    params = [
        f"%{search_text}%",
        f"%{search_text}%"
    ]

    if status != "All":
        query += " AND status = ?"
        params.append(status)

    query += " ORDER BY id DESC"

    cursor.execute(query, params)

    applications = cursor.fetchall()

    conn.close()

    return applications


def get_status_count(status):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM applications WHERE status = ?",
        (status,)
    )

    count = cursor.fetchone()[0]

    conn.close()

    return count


def get_total_count():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM applications"
    )

    count = cursor.fetchone()[0]

    conn.close()

    return count