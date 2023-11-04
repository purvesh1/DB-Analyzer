from prettytable import PrettyTable

# Metadata Storage
metadata_storage = {}

def fetch_and_store_metadata(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
    for table in cursor.fetchall():
        table_name = table[0]
        cursor.execute(f"SELECT column_name, data_type FROM information_schema.columns WHERE table_name = '{table_name}'")
        metadata_storage[table_name] = cursor.fetchall()

def get_field_semantics(field):
    # Implement your logic here to provide a one-line semantic description of the field
    return 'Sample description'

def prompt_user_for_field_choice(potential_fields):
    print("Multiple fields found. Please choose one:")
    for i, (table, field) in enumerate(potential_fields):
        print(f"{i+1}. {field} in {table} - {get_field_semantics(field)}")
    choice = input("Enter your choice: ")
    return potential_fields[int(choice) - 1]

def sql_result_to_table_str(sql_result):
    # Create a PrettyTable object
    table = PrettyTable()
    
    # If the result is empty, return a message
    if not sql_result:
        return "No results found."
    
    # Check if the result contains tuples or dictionaries
    if isinstance(sql_result[0], tuple):
        # If it's tuples, we don't have field names
        for row in sql_result:
            table.add_row(row)
    else:
        # If it's dictionaries, we can get field names
        table.field_names = sql_result[0].keys()
        for row in sql_result:
            table.add_row(row.values())
    
    table.float_format = ".2"
    return str(table)

def enforce_query_limit(query, max_rows=3):
    # Check if the query already has a LIMIT clause
    if "LIMIT" in query.upper():
        return query
    else:
        # If not, append a LIMIT clause to the query
        return f"{query.strip(';')} LIMIT {max_rows};"
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
