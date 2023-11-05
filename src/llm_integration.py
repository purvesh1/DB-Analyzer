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
                print("llm response: ", response)
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
        mem_ops = self.llm_get_steps(initial_input)
        print("no. of mem_ops: ", len(mem_ops))
        for mem_op in mem_ops:
            print("mem_op: ", mem_op)
            db.log_to_file(mem_op['description'], False)
            db.log_to_file(mem_op['sql_code'], True)
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


    def llm_get_steps(self, user_input):
        # Use LLM to break down the user_input into a series of SQL queries or other operations
        messages = [
    {
        "role": "system",
        "content": f"user info: host: {cfg.pg_host}, port: {cfg.pg_port}, User: {cfg.pg_user}, database: {cfg.pg_database}."
    },
    {"role": "user","content":f"""
Please tell me what standard SQL statements should I use in order to respond to the "USER INPUT". \
If it needs multiple SQL operations on the database, please list them step by step concisely. \
If there is no need to use the database, reply to the "USER INPUT" directly.
The output should be a markdown code snippet formatted in the following schema, \
including the leading and trailing "\`\`\`" and "\`\`\`":

Step1: <Description of first step>
``` SQL command for step1 ```

Step2: <Description of second step>
``` SQL command for step2 ```

......

USER INPUT: {user_input}
ANSWER:
""" }
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
