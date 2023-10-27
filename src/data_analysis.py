import openai
from config import cfg

class DataAnalysis:
    def __init__(self):
        self.model = cfg.llm_model
        self.token_limit = cfg.token_limit
        self.previous_queries = {}  # In-memory storage for previous queries

    def generate_insights(self, data, query_id=None):
        prompt = f"Generate insights for the following data: {data}"
        response = openai.Completion.create(
            engine=self.model,
            prompt=prompt,
            max_tokens=50
        )
        insights = response.choices[0].text.strip()

        # Save the result if a query_id is provided
        if query_id:
            self.previous_queries[query_id] = insights

        return insights

    def store_previous_query(self, query, result):
        self.previous_queries[query] = result

    def retrieve_previous_query(self, query):
        return self.previous_queries.get(query, None)

# Your existing testing code
def test_generate_insights():
    da = DataAnalysis()
    data = {
        'Product A': {'Sales': 100, 'Profit': 20},
        'Product B': {'Sales': 150, 'Profit': 30},
    }
    insights = da.generate_insights(data)
    assert insights == "Your expected output"

# Example usage
if __name__ == "__main__":
    # Run your existing tests
    test_generate_insights()
    
    # Demonstration of new methods
    da = DataAnalysis()
    
    # Storing a previous query and its result
    da.store_previous_query("What are the total sales for product A?", {'Sales': 100})
    
    # Retrieving the result of a previous query
    previous_result = da.retrieve_previous_query("What are the total sales for product A?")
    print(f"Previous Result: {previous_result}")
    
    # Generating insights based on the previous query result
    if previous_result:
        insights = da.generate_insights(previous_result)
        print(f"Insights: {insights}")
