import time
import openai
from config.config import cfg
import re
from utils import db_utils
class LLMIntegration:
    def __init__(self):
        self.model = cfg.llm_model
        self.temperature = cfg.temperature
        self.token_limit = cfg.token_limit
        self.previous_queries = {}

    def generate_response(self, prompt):
        messages = [
            {
                "role": "system",
                "content": f"For my database: {cfg.pg_database}. Remember the context:"
            },
            {"role": "user","content": f"{prompt}. Write working psql code." }
        ]
        num_retries = 1
        for attempt in range(num_retries):
            try:
                response = openai.ChatCompletion.create(
                    model=self.model,
                    messages=messages,
                    temperature=self.temperature,
                )
                return response.choices[0].message["content"].strip()
            except openai.error.RateLimitError:
                if cfg.debug_mode:
                    print("API Rate Limit Reached. Waiting 20 seconds...")
                time.sleep(20)
            except openai.error.APIError as e:
                # Handle other API errors
                pass
    
    def generate_insights(self, result):
        #print result
        print("Results: ", result)
        print("Generating insights...")
        print(db_utils.sql_result_to_table_str(result))
        messages = [
            {"role": "system", "content": "You are a seasoned data analyst with years of experience with SQL databases, python programming and Business Analytics."},
            {"role": "user", "content": db_utils.sql_result_to_table_str(result)}
        ]
        num_retries = 5
        for attempt in range(num_retries):
            try:
                response = openai.ChatCompletion.create(
                    model=self.model,
                    messages=messages,
                    temperature=self.temperature,
                    max_tokens=self.token_limit
                )
                return response.choices[0].message["content"].strip()
            except openai.error.RateLimitError:
                if cfg.debug_mode:
                    print("API Rate Limit Reached. Waiting 20 seconds...")
                time.sleep(20)
            except openai.error.APIError as e:
                # Handle other API errors
                pass
    
    def chain_of_thought(self, initial_input, db):
        # might migrate to llm_integration.py
        mem_ops = self.llm_get_steps(db.metadata, initial_input)
        print("no. of mem_ops: ", len(mem_ops))
        for mem_op in mem_ops:
            print("mem_op: ", mem_op)
            print("Step Description: ", mem_op['description'])
            db.log_to_file(mem_op['description'], False)
            db.log_to_file(mem_op['sql_code'], True)
        results ,columns = db.execute_sql(mem_op['sql_code'])
        print("colums: ", columns)
        print("results: ", results)
        db.display_query_results(results, columns)
        # final_response = self.llm_summary()
        # return final_response

    def parse_steps(self, response):
    # Define a regex pattern to capture step number, description, and SQL code
        pattern = re.compile(
            r'Step (\d+): ([\s\S]+?)```sql\n([\s\S]+?)\n```',\
        )

        # Find all matches in the response
        matches = pattern.findall(response)

        # Create a list to hold the parsed steps
        parsed_steps = []

        # Loop through the matches and structure them into a dictionary
        for match in matches:
            step = {
                'step_number': match[0],
                'description': match[1].strip(),
                'sql_code': match[2].strip()
            }
            parsed_steps.append(step)

        return parsed_steps


    def llm_get_steps(self, metadata, user_input):
        # Use LLM to break down the user_input into a series of SQL queries or other operations
        metadata_description = ""

        # Generate a description from the metadata for each table
        for table, details in metadata.items():
            table_description = details.get('description', 'No description available')
            column_details = ', '.join([f"{col}: {col_details['data_type']}" for col, col_details in details.get('columns', {}).items()])
            metadata_description += f"Table '{table}' ({table_description}): Columns - {column_details}. "
        messages = [
            {
                "role": "system",
                "content": "PostgreSQL connection established. Details - Host: {}, Port: {}, User: {}, Database: {}.".format(cfg.pg_host, cfg.pg_port, cfg.pg_user, cfg.pg_database)
            },
            {
                "role": "user",
                "content": """
        Please analyze the following user input and provide appropriate pSQL statements. If multiple SQL operations are needed, list them in a sequential, step-by-step manner. If the user input doesn't require database interaction, please respond directly to the query.
        Database Schema Information:
        {}
        Format the SQL statements as markdown code snippets, structured as follows:

        - Step 1: [Description of first step]
        ```sql
        [SQL command for step 1]
        ```

        - Step 2: [Description of second step]
        ```sql
        [SQL command for step 2]
        ```

        Continue this format for all required steps.

        USER INPUT: {}
        ANSWER:
        """.format(metadata_description, user_input)
            }
        ]
        num_retries = 1
        for attempt in range(num_retries):
            try:
                response = openai.ChatCompletion.create(
                    model=self.model,
                    messages=messages,
                    temperature=self.temperature,
                )
                print("llm response: ", response.choices[0].message["content"].strip())
                # return response.choices[0].message["content"].strip()
            except openai.error.RateLimitError:
                if cfg.debug_mode:
                    print("API Rate Limit Reached. Waiting 20 seconds...")
                time.sleep(20)
            except openai.error.APIError as e:
                # Handle other API errors
                pass
            
        return self.parse_steps(response.choices[0].message["content"].strip())
    
    
# Example usage
if __name__ == "__main__":
    llm = LLMIntegration()
    prompt = "Translate the following natural language query into SQL: What are the total sales for product A?"
    response = llm.generate_response(prompt)
    print(f"Generated Response: {response}")
