import psycopg2
import sys
from config.config import cfg

class DatabaseInteraction:
    def __init__(self):
        self.conn = None
        self.cursor = None

    def connect(self):
        self.conn = psycopg2.connect(
            host=cfg.pg_host,
            port=cfg.pg_port,
            user=cfg.pg_user,
            password=cfg.pg_password,
            database=cfg.pg_database
        )
        self.cursor = self.conn.cursor()

    def disconnect(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()

    def execute_sql(self, sql, params=None):
        try:
            self.connect()
            self.cursor.execute(sql, params)
            self.conn.commit()
            return self.cursor.fetchall()
        except Exception as e:
            self.conn.rollback()
            print(f"SQL error: {str(e)}")
        finally:
            self.disconnect()

    def select(self, table, columns="*", condition=None):
        sql = f"SELECT {columns} FROM {table}"
        if condition:
            sql += f" WHERE {condition}"
        return self.execute_sql(sql)

    def validate_sql_query(self, sql_query):
    # Basic validation logic here. For now, let's just check if the query is not empty.
        if not sql_query.strip():
            return False
        return True

    # Add more CRUD methods like insert, update, delete, etc.

