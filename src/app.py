import streamlit as st
from database_interaction import DatabaseInteraction
from llm_integration import LLMIntegration
import streamlit as st
import pandas as pd

def get_final_system_prompt():
    # Placeholder for the initial system prompt
    return "System is ready to answer your queries."

def run_chat_sequence(prompt):
    # Placeholder function to simulate processing the prompt
    # Replace with actual logic to get a response from the model
    return f"Response to: '{prompt}'"

def main():
    llm = LLMIntegration()
    db = DatabaseInteraction()

    st.title("🤖 AI Database Chatbot 🤓")

    # Initialize session state for chat history if not already set
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Chat input box

    for message in st.session_state.chat_history:
        if message['role'] == "You":
            st.markdown(f"**You**: {message['content']}")
        elif message['role'] == "System":
            # Reconstruct the DataFrame to display
            df_to_display = pd.DataFrame(message['content'])
            st.dataframe(df_to_display)

    user_input = st.chat_input("What do you want to know?")

    # When the user enters a prompt and presses Enter
    if user_input:
        # Append the user prompt to the chat history
        st.chat_message("You").markdown(user_input)
        st.session_state.chat_history.append({"role": "You", "content": user_input})
        df = llm.chain_of_thought(user_input, db)

        # Display the DataFrame
        st.dataframe(df)

        # Convert the DataFrame to a list of dictionaries and append a string representation to the chat history
        df_records = df.to_dict('records')
        st.session_state.chat_history.append({"role": "System", "content": df_records})

if __name__ == "__main__":
    main()