from llm_integration import LLMIntegration
from database_interaction import DatabaseInteraction
import requests
import config.config as cfg

def hf_query(payload, api_url):
    headers = {"Authorization": f"Bearer {cfg.Config().hf_api_key}"}
    print("Payload: ", payload)
    print(f"Bearer {cfg.Config().hf_api_key}")
    response = requests.post(api_url, headers=headers, json=payload)
    return response.json()

class NLQProcessing:
    def __init__(self):
        self.llm = LLMIntegration()
        self.db = DatabaseInteraction()
        self.sql_results = []
        self.new_mem_ops = []

    
    
    def process_query(self, nl_query, only_code=True):
        # Step 1: Generate SQL Query using LLM
        prompt = f"Translate the following natural language query into SQL: {nl_query}." + only_code*"Only code."
        sql_query = self.llm.generate_response(prompt)
        # Step 2: Validate SQL Query
        is_valid = self.db.validate_sql_query(sql_query)
        if not is_valid:
            return "Invalid SQL query generated. Please try again."
        return sql_query
    
    def chain_of_thought(self, initial_input):
        mem_ops = self.llm_get_steps(initial_input)
        for mem_op in mem_ops:
            new_mem_op = self.llm_update_operation(mem_op)
            sql_result = self.db.execute_sql(new_mem_op)
            self.sql_results.append(sql_result)
            self.new_mem_ops.append(new_mem_op)
        final_response = self.llm_summary()
        return final_response
    
    def llm_get_steps(self, user_input):
        # Use LLM to break down the user_input into a series of SQL queries or other operations
        return []

    def llm_update_operation(self, mem_op):
        # Use LLM to update the operation based on previous results if needed
        return mem_op

    def llm_summary(self):
        # Use LLM to summarize the final response based on the results of all executed SQL queries
        return ""
    
    def nl_to_sql(self, nl_query, model="sqlcoder2"):

        if model == "sqlcoder2":
            API_URL = "https://api-inference.huggingface.co/models/defog/sqlcoder2"
            payload = {
                "inputs": {
                    "question": nl_query,
                    "context": "Only produce SQL code. You don't know anything about the database. Query what you need to know.",
                }
            }
            return hf_query(payload, API_URL)
        else :
            print("Using LLM config")
            prompt = f"You know nothing about the database. Query what you need: {nl_query}. Only code"
            sql_query = self.llm.generate_response(prompt)
            return sql_query
        
# Example usage
if __name__ == "__main__":
    nlqp = NLQProcessing()
    nl_query = "What are the total sales for product A?"
    result, insights = nlqp.process_query(nl_query)
    print(f"Query Result: {result}")
    print(f"Insights: {insights}")
