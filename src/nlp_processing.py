from llm_integration import LLMIntegration
from database_interaction import DatabaseInteraction

class NLPProcessing:
    def __init__(self):
        self.llm = LLMIntegration()
        self.db = DatabaseInteraction()

    def process_query(self, nl_query):
        # Step 1: Generate SQL Query using LLM
        prompt = f"Translate the following natural language query into SQL: {nl_query}"
        sql_query = self.llm.generate_response(prompt)
        
        # Step 2: Validate SQL Query
        is_valid = self.db.validate_sql_query(sql_query)
        if not is_valid:
            return "Invalid SQL query generated. Please try again."
        
        # Step 3: Execute SQL Query
        result = self.db.execute_sql(sql_query)
        
        # Step 4: Generate insights (if needed)
        insights = ""
        if "SELECT" in sql_query.upper():
            insights = self.llm.generate_insights(result)
        
        return result, insights

# Example usage
if __name__ == "__main__":
    nlp = NLPProcessing()
    nl_query = "What are the total sales for product A?"
    result, insights = nlp.process_query(nl_query)
    print(f"Query Result: {result}")
    print(f"Insights: {insights}")
