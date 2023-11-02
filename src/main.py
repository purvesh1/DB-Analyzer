from cli_interface import main as cli_main
from nlq_processing import NLQProcessing
import os
from langchain.llms import OpenAI
from langchain.utilities import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain
from config.config import cfg

PROMPT = """ 
Given an input question, first create a syntactically correct postgresql query to run,  
then look at the results of the query and return the answer.  
The question: {question}
"""

def main():
    print("Welcome to the Natural Language SQL Query Interface!")
    print("1. CLI Interface" * True)
    print("2. Use langchain" * False)
    # Future options can go here
    # choice = input("Please select an interface to proceed: ")
    choice = '3'
    if choice == '1':
        cli_main()
    elif choice == '2':
        # rough implementation of langchain method
        pg_uri = f"postgresql+psycopg2://{cfg.pg_user}:{cfg.pg_password}@{cfg.pg_host}:{cfg.pg_port}/{cfg.pg_database}"
        db = SQLDatabase.from_uri(pg_uri)
        llm = OpenAI(temperature=0, openai_api_key=cfg.openai_api_key, model_name=cfg.llm_model) 

        db_chain = SQLDatabaseChain(llm=llm, database=db, verbose=True, top_k=3)
        question = input("Please enter your question: ")
        db_chain.run(PROMPT.format(question=question))
    elif choice == '3':
        question = input("Please enter your question: ")
        nlqp = NLQProcessing()
        sql_query = nlqp.nl_to_sql(question, cfg.llm_model)
        print("SQL Query: ", sql_query) 
    else:
        print("Invalid choice. Exiting.")

if __name__ == "__main__":
    main()
