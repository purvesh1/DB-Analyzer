from database_interaction import DatabaseInteraction
from llm_integration import LLMIntegration

def main():
    db = DatabaseInteraction()
    llm = LLMIntegration()

    while True:
        nl_query = input("Please enter your query in an unambigous way: ")
        
        llm.chain_of_thought(nl_query, db)
        # Log NL query
        # print(db.log_to_file(nl_query, False))
        
        # # Convert NL query to SQL query
        # sql_query = db.extract_sql_blocks(llm.generate_response(nl_query))[0]
        # print("SQL Query: ", sql_query)
        # print("-"*20)
        
        # # Log SQL query
        # print(db.log_to_file(sql_query, True))
        
        # Execute SQL query
        # data = db.execute_sql(sql_query)
        # insights = ""
        # if "SELECT" in sql_query.upper():
        #     insights = llm.generate_insights(data)
        
        # print(f"Insights:" + "\n" + insights)

        cont = input("Would you like to continue? (y/n): ")
        if cont.lower() != 'y':
            break

if __name__ == "__main__":
    main()
