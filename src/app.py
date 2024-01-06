import streamlit as st
from database_interaction import DatabaseInteraction
from llm_integration import LLMIntegration
import streamlit as st
import pandas as pd
import json
from prettytable import PrettyTable

def display_json_schema(json_file_path):
    with open(json_file_path, 'r') as file:
        schema = json.load(file)
    st.json(schema) 

def get_final_system_prompt():
    # Placeholder for the initial system prompt
    return "System is ready to answer your queries."

def run_chat_sequence(prompt):
    # Placeholder function to simulate processing the prompt
    # Replace with actual logic to get a response from the model
    return f"Response to: '{prompt}'"

def schema_diagram_page():
    st.title("🗂 Database Schema")

    # Generate the diagram
    display_json_schema('src/artifacts/metadata.json')

def chat_interface(llm, db):

    st.title("🤖 AI Database Chatbot 🤓")

    # Initialize session state for chat history if not already set
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Chat input box

    for message in st.session_state.chat_history:
        if message['role'] == "💬":
            st.markdown(f"**💬**: {message['content']}")
        elif message['role'] == "🤖":
            # Reconstruct the DataFrame to display
            print("df to display: ", message['content'])
            df_to_display = message['content']

            if isinstance(df_to_display, str):
                st.markdown(f"```\n{df_to_display}\n```")
            elif isinstance(df_to_display, str):
                st.chat_message("🤖").markdown(df_to_display)

    user_input = st.chat_input("What do you want to know?")

    # When the user enters a prompt and presses Enter
    if user_input:
        
        if "context" not in st.session_state:
            st.session_state.context = []  
        # Append the user prompt to the chat history
        st.chat_message("💬").markdown(user_input)
        st.session_state.chat_history.append({"role": "💬", "content": user_input})
        bool_dataframe, df = llm.chain_of_thought(user_input, db)
        
        # Display the DataFrame
        

        if isinstance(df, pd.DataFrame):
            st.dataframe(df)
            table = PrettyTable()
            table.field_names = df.columns

            row_count = 0
            for row in df.itertuples(index=False):
                if row_count < 5:  # Limit to first 5 rows
                    table.add_row(row)
                row_count += 1

            # Convert the PrettyTable object to a string
            table_str = table.get_string()
            if row_count > 5:
                table_str += f"\nTotal rows in DataFrame: {row_count}"  
            st.session_state.chat_history.append({"role": "🤖", "content": table_str, "is_df": True})
        else:
            st.chat_message("🤖").markdown(df)
            st.session_state.chat_history.append({"role": "🤖", "content": df, "is_df": False})

        st.session_state['waiting_for_followup'] = True


        if st.session_state.get('follow_up_needed', True):
        # Create a radio button prompt
            follow_up_option = st.multiselect("Do you want to finish or have a follow-up question?", 
                                        ['Finish', 'Follow Up'])

            if follow_up_option == 'Finish':
                st.session_state['follow_up_needed'] = False
                st.success("Great! How else can I assist you?")
                st.session_state['last_response'] = None  # Clear last response
                # You can use a flag or other mechanism instead of break if needed

            elif follow_up_option == 'Follow Up':
                st.session_state['follow_up_needed'] = True
                st.info("Please type your follow-up question.")

        print("chat history: ", st.session_state.chat_history)

def main():
    llm = LLMIntegration()
    db = DatabaseInteraction()

    # Page selection
    page = st.sidebar.selectbox("Choose a view", ["Chat Interface", "Schema"])

    # Page routing
    if page == "Chat Interface":
        chat_interface(llm, db)
    elif page == "Schema Diagram":
        schema_diagram_page()

if __name__ == "__main__":
    main()


