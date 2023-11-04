import time
import openai
from config.config import cfg
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

# Example usage
if __name__ == "__main__":
    llm = LLMIntegration()
    prompt = "Translate the following natural language query into SQL: What are the total sales for product A?"
    response = llm.generate_response(prompt)
    print(f"Generated Response: {response}")
