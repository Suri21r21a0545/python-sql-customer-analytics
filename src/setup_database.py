import mysql.connector
from pathlib import Path
from config import DB_CONFIG

def main():
    cfg = DB_CONFIG.copy()
    db_name = cfg.pop("database")

    connection = mysql.connector.connect(**cfg)
    cursor = connection.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{db_name}`")
    connection.commit()
    cursor.close()
    connection.close()

    connection = mysql.connector.connect(**DB_CONFIG)
    cursor = connection.cursor()

    sql_file = Path(__file__).resolve().parents[1] / "sql" / "database.sql"
    sql_text = sql_file.read_text(encoding="utf-8")

    for statement in sql_text.split(";"):
        statement = statement.strip()
        if statement:
            cursor.execute(statement)

    connection.commit()
    cursor.close()
    connection.close()
    print("Database and tables created successfully.")

if __name__ == "__main__":
    main()
