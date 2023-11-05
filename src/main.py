from cli_interface import main as cli_main
from nlq_processing import NLQProcessing
from config.config import cfg

def main():
    print("Welcome to the Natural Language SQL Query Interface!")
    print("1. CLI Interface" * True)
    print("2. Web App " * False)
    # Future options can go here
    # choice = input("Please select an interface to proceed: ")
    
    choice = '1'
    if choice == '1':
        cli_main()
    
    elif choice == '2':
        question = input("Please enter your question: ")
        nlqp = NLQProcessing()
        sql_query = nlqp.nl_to_sql(question, cfg.llm_model)

        print("SQL Query: ", sql_query) 
    else:
        print("Invalid choice. Exiting.")

if __name__ == "__main__":
    main()
