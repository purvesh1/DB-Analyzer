from cli_interface import main as cli_main
from nlq_processing import NLQProcessing
from config.config import cfg
import subprocess

def main():
    print("Welcome to the Natural Language SQL Query Interface!")
    print("1. CLI Interface" * True)
    print("2. Web App " * False)
    # Future options can go here
    # choice = input("Please select an interface to proceed: ")
    
    choice = input("Please select an interface to proceed: ")
    if choice == '1':
        cli_main()
    
    elif choice == '2':
        subprocess.run(["streamlit", "run", "app.py"])
    
    else:
        print("Invalid choice. Exiting.")

if __name__ == "__main__":
    main()
