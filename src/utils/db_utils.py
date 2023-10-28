import psycopg2

# Metadata Storage
metadata_storage = {}

def fetch_and_store_metadata(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
    for table in cursor.fetchall():
        table_name = table[0]
        cursor.execute(f"SELECT column_name, data_type FROM information_schema.columns WHERE table_name = '{table_name}'")
        metadata_storage[table_name] = cursor.fetchall()

def is_potential_field(metadata, value):
    # Implement your logic here to decide if a field is a potential match for the value
    return True

def identify_potential_fields(value):
    potential_fields = []
    for table, metadata in metadata_storage.items():
        for field, field_type in metadata:
            if is_potential_field(field_type, value):
                potential_fields.append((table, field))
    return potential_fields

def get_field_semantics(field):
    # Implement your logic here to provide a one-line semantic description of the field
    return 'Sample description'

def prompt_user_for_field_choice(potential_fields):
    print("Multiple fields found. Please choose one:")
    for i, (table, field) in enumerate(potential_fields):
        print(f"{i+1}. {field} in {table} - {get_field_semantics(field)}")
    choice = input("Enter your choice: ")
    return potential_fields[int(choice) - 1]

# Example usage
# Establish your PostgreSQL connection here
# conn = psycopg2.connect(...)

# Fetch and store metadata
# fetch_and_store_metadata(conn)

# Identify potential fields for a value
# potential_fields = identify_potential_fields('PEPSICO INC')

# Prompt user for field choice
# if len(potential_fields) > 1:
#     chosen_field = prompt_user_for_field_choice(potential_fields)
#     print(f"You chose: {chosen_field}")
