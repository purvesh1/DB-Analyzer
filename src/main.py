from src.cli_interface import main as cli_main

def main():
    print("Welcome to the Natural Language SQL Query Interface!")
    print("1. CLI Interface")
    # Future options can go here
    choice = input("Please select an interface to proceed: ")

    if choice == '1':
        cli_main()
    else:
        print("Invalid choice. Exiting.")

if __name__ == "__main__":
    main()
