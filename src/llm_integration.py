import time
import openai
from config.config import cfg
import re
from utils import prompts

class LLMIntegration:
    def __init__(self):
        self.model = cfg.llm_model
        self.temperature = cfg.temperature
        self.token_limit = cfg.token_limit
        self.context = []
        self.tries = 0 # unused, track number of retries per erranoous response

    def generate_insights(self, result):
        #TODO: generate insights suing results and query
        messages = [
            {"role": "system", "content": "You are a seasoned data analyst with years of experience with SQL databases, python programming and Business Analytics."},
            {"role": "user", "content": ""}
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
    
    def update_context(self, user_query, sql_query):
        self.context.append({
            "user_query": user_query,
            "sql_query": sql_query
        })
        # Optionally, limit the context size to the last N interactions, conserve session memory.
        self.context = self.context[-10:]

    def get_context(self):
        # Format the context as a string
        formatted_context = ""
        if len(self.context) > 0:
            formatted_context += f"User Query: {self.context[-1]['user_query']}\n"
            formatted_context += f"SQL Query: {self.context[-1]['sql_query']}\n\n"
        return formatted_context
    
    def chain_of_thought(self, initial_input, db , context = ""):
        context = ""
        if len(self.context) > 0:
            context = "Previous Query if required: " + self.get_context()

        prompt = prompts.cot_prompt(db.get_metadata_description(), context, initial_input)
        mem_ops, response = self.llm_get_steps(prompt)
        
        if len(mem_ops) < 1 :
            return False, response
        # db.log_to_file(initial_input, False) # log user input
        results ,columns, error = db.execute_sql(mem_ops[-1]['sql_code'])
        
        if error:
            print("Error: ", error)
            prompt = prompts.on_error_prompt(error=error, mem_op=mem_ops[-1]['sql_code'])
            mem_ops = self.llm_get_steps(prompt)
            
            if len(mem_ops) < 1:
                return False, response
            # db.log_to_file(initial_input, False) # log user input
            results ,columns, error = db.execute_sql(mem_ops[-1]['sql_code'])
        
        if error:
            print("New Error: ", error)
            return False, error
        self.update_context(initial_input, mem_ops[-1]['sql_code'])
        return True, db.display_query_results(results, columns)
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
        
        return parsed_steps, response

    def unparse_steps(self, mem_ops):
        formatted_str = ""
        for mem_op in mem_ops:
            step_str = f"Step {mem_op['step_number']}: {mem_op['description']}\n```sql\n{mem_op['sql_code']}\n```\n"
            formatted_str += step_str
        return formatted_str

    def llm_get_steps(self, prompt):
        # Use LLM to break down the user_input into a series of SQL queries or other operations
        messages = [
            {
                "role": "system",
                "content": "Give executable queries, don't instruct. PostgreSQL connection established. Details - Host: {}, Port: {}, User: {}, Database: {}.".format(cfg.pg_host, cfg.pg_port, cfg.pg_user, cfg.pg_database)
            },
            {
                "role": "user",
                "content": prompt
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
