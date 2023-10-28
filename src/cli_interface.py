from database_interaction import DatabaseInteraction
from llm_integration import LLMIntegration
from nlp_processing import NLPProcessing
from data_analysis import DataAnalysis

def main():
    db = DatabaseInteraction()
    llm = LLMIntegration()
    nlp = NLPProcessing()
    da = DataAnalysis()

    while True:
        nl_query = input("Please enter your query in natural language: ")
        print("Natural Language Query: ", nl_query)
        # Convert NL query to SQL query
        sql_query = nlp.process_query(nl_query)
        
        # Execute SQL query
        data = db.execute_sql(sql_query)
        
        # Generate insights
        insights = da.generate_insights(data)
        
        print(f"Insights: {insights}")

        cont = input("Would you like to continue? (y/n): ")
        if cont.lower() != 'y':
            break

if __name__ == "__main__":
    main()
