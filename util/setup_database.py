import sqlite3

# Database file name
DB_NAME = "/Users/saurabhatri/Dev/virgil.sqlite"

# SQL file containing table initialization script
SQL_FILE = "init_users_table.sql"

def create_database():
    """Creates SQLite database and initializes tables."""
    try:
        # Connect to SQLite database (creates if not exists)
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        # Read and execute SQL script
        with open(SQL_FILE, "r") as sql_file:
            cursor.executescript(sql_file.read())

        # Commit and close connection
        conn.commit()

        print(f"{cursor.rowcount} users inserted successfully!")
        conn.close()
        print(f"✅ Database '{DB_NAME}' and 'users' table initialized successfully!")

    except Exception as e:
        print(f"❌ Error initializing database: {e}")

if __name__ == "__main__":
    create_database()
