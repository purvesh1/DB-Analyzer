import psycopg2
from config.config import cfg
from datetime import datetime
import subprocess
import pandas as pd
import os
from prettytable import PrettyTable
import re
import json

class DatabaseInteraction:
    ## TODO: Make a choice, either use psycopg2 or subprocess, not both. Not utilizing the psycopg2 right now. But kept. 
    def __init__(self):
        self.connect()
        self.metadata = self.fetch_metadata()
        self.session_id = datetime.now().strftime("%Y%m%d%H%M%S")
        self.file_path = f"src/artifacts/session_output_{self.session_id}.txt"

    def fetch_metadata(self, schema = 'public'):
        cursor = self.conn.cursor()

        # Fetching table names
        table_query = f"SELECT table_name FROM information_schema.tables WHERE table_schema='{schema}';"
        cursor.execute(table_query)
        tables = [table[0] for table in cursor.fetchall()]

        metadata = {}
        for table in tables:
            # Fetching column details for each table
            column_query = f"SELECT column_name, data_type FROM information_schema.columns WHERE table_name = '{table}';"
            cursor.execute(column_query)
            columns = cursor.fetchall()

            # Formatting metadata with empty descriptions
            metadata[table] = {
                "description": "",  # Table description (currently empty)
                "columns": {
                    column[0]: {
                        "data_type": column[1],
                        "description": ""  # Column description (currently empty)
                    } for column in columns
                }
            }

        self.disconnect()
        self.save_metadata_to_json(metadata)
        return metadata

    def save_metadata_to_json(self, metadata, filename = "src/artifacts/metadata.json"):
        # Check if the file already exists
        if not os.path.isfile(filename):
            # Convert dictionary to JSON string
            json_str = json.dumps(metadata, indent=4)
            
            # Write JSON string to file
            with open(filename, 'w') as file:
                file.write(json_str)
            print(f"Metadata saved to {filename}")
        else:
            print(f"File {filename} already exists. No new file was created.")

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
            sql = ' '.join(sql.split())
            print("Executing SQL: ", sql)
            self.connect()
            self.cursor.execute(sql, params)
            self.conn.commit()
            columns = [desc[0] for desc in self.cursor.description]
            return self.cursor.fetchall(), columns, None  # Success, no error message
        except Exception as e:
            self.conn.rollback()
            error_message = f"SQL error: {str(e)}"
            print(error_message)
            return None, None, error_message
        finally:
            self.disconnect()
    
    # Add more CRUD methods like insert, update, delete, etc.
    def display_query_results(self, results, columns):
        table = PrettyTable()
        table.field_names = columns

        row_count = 0
        for row in results:
            table.add_row(row)
            row_count += 1
        print(table)
        return pd.DataFrame(results, columns=columns)
    
    def log_to_file(self, query, sql=True):
        ''' ⚠️Deals with a subprocess right on the shell, prolly vulnerable to SQL injections.'''
        
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