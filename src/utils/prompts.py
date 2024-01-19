
def on_error_prompt(error, mem_op): 
    return """We encountered the following:``` {error} ```, while trying to execute the following SQL query: ``` {mem_op} ``` Please try again to fix the issue and give a solution in the following format : 
            Format the SQL statements as markdown code snippets, structured as follows:
            Note: Make sure give out an executable SQL statement, complete with all the assignments. Find and replace the variables with the correct values.
            - Step 1: [Description of first step]
            ```sql
            [SQL command for step 1]
            ```

            - Step 2: [Description of second step]
            ```sql
            [SQL command for step 2]
            ```

            Continue this format for all required steps.""".format(error, mem_op)
            
def cot_prompt(metadata_description, context, user_input):
    return """
        Please analyze the following user input and provide appropriate pSQL statements. If multiple SQL operations are needed, list them in a sequential, step-by-step manner. Use all the information you have to build final executable SQL statements.
        If the user input doesn't require database interaction, please respond directly to the query.
        Database Schema Information:
        {}
        {}
        Format the SQL statements as markdown code snippets, structured as follows:

        - Step 1: [Description of first step]
        ```sql
        [SQL command for step 1]
        ```

        - Step 2: [Description of second step]
        ```sql
        [SQL command for step 2]
        ```

        Continue this format for all required steps.

        Then combine all the steps into a single SQL statement and execute it.
        USER INPUT: {}
        ANSWER:
        """.format(metadata_description, context, user_input)