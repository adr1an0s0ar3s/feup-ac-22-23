import sqlite3

def migrate():
    with open("data/database.db", "w") as f:
        f.write("hello")

if __name__ == "__main__":
    migrate()