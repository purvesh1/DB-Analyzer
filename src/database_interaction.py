import psycopg2
from config.config import cfg
from datetime import datetime
import subprocess
import os
import re

class DatabaseInteraction:
    ## TODO: Make a choice, either use psycopg2 or subprocess, not both. Not utilizing the psycopg2 right now. But kept. 
    def __init__(self):
        self.connect()
        self.metadata = self.fetch_metadata()
        self.session_id = datetime.now().strftime("%Y%m%d%H%M%S")
        self.file_path = f"src/artifacts/session_output_{self.session_id}.txt"

    def fetch_metadata(self):
        cursor = self.conn.cursor()
        query = "SELECT table_name FROM information_schema.tables WHERE table_schema='public';"
        cursor.execute(query)
        tables = [table[0] for table in cursor.fetchall()]
        metadata = {}
        for table in tables:
            query = f"SELECT column_name, data_type FROM information_schema.columns WHERE table_name = '{table}';"
            cursor.execute(query)
            columns = cursor.fetchall()
            metadata[table] = {column[0]: column[1] for column in columns}
        self.disconnect()
        return metadata

    def refresh_metadata(self):
        self.metadata = self.fetch_metadata()


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
        #TODO: Add write permission management
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
    
    def extract_sql_blocks(self, text):
        # This regular expression looks for ```sql followed by any characters
        # and ending with ```, capturing the content in between.
        pattern = r"```sql(.*?)```"
        
        # re.DOTALL allows the dot (.) to match newlines as well
        matches = re.findall(pattern, text, re.DOTALL)
        
        # Clean up any leading or trailing whitespace and join the matches
        # Each match is stripped of leading/trailing whitespace and returned in a list
        sql_blocks = [match.strip() for match in matches]
        
        return sql_blocks
    # Add more CRUD methods like insert, update, delete, etc.
    def log_to_file(self, query, sql=True):
        
        with open(self.file_path, 'a') as f:
            f.write("\n-------------------------\n")
            f.write((not sql)*"User Query:\n")
            f.write(sql*"SQL Query:\n")
            f.write(f"{query}\n")
            f.write(sql*"\n Response:\n")
            f.close()
        env = os.environ.copy()
        env['PGPASSWORD'] = cfg.pg_password
        if sql:
            query = ' '.join(query.split())
            command = f'psql -h {cfg.pg_host} -p {cfg.pg_port} -U {cfg.pg_user} -d {cfg.pg_database} -c "{query}" >> {self.file_path} 2>&1'
            return subprocess.call(command, shell=True,  env=env)
        return 0