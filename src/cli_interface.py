from database_interaction import DatabaseInteraction
from llm_integration import LLMIntegration
from nlq_processing import NLQProcessing

def main():
    db = DatabaseInteraction()
    llm = LLMIntegration()
    nlqp = NLQProcessing()

    while True:
        nl_query = input("Please enter your query in natural language: ")
        print("Natural Language Query: ", nl_query)
        # Convert NL query to SQL query
        sql_query = nlqp.process_query(nl_query)
        
        # Execute SQL query
        data = db.execute_sql(sql_query)
        insights = ""
        if "SELECT" in sql_query.upper():
            insights = llm.generate_insights(data)
        
        print(f"Insights:" + "\n" + insights)

        cont = input("Would you like to continue? (y/n): ")
        if cont.lower() != 'y':
            break

if __name__ == "__main__":
    main()
