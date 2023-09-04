# Import the required libraries
import streamlit as st
import langchain as lc
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env file
api_key = os.getenv("OPENAI_API_KEY")
import openai

# Use the `api_key` variable wherever you need to authenticate with OpenAI
openai.api_key = api_key
# Create a title for the app
st.title("Habit Tracking App with Langchain and ChatGPT")
def main():
    # Create a sidebar for user input
    st.sidebar.header("User Input")
    user_name = st.sidebar.text_input("Enter your name")
    user_habit = st.sidebar.text_input("Enter your habit")

    # Create a main section for the app
    st.header(f"Hello, {user_name}!")
    st.write(f"Your habit is: {user_habit}")
    st.checkbox("Morning Rutine")
    """


"""
    # Create a button to end the app
    if st.button("End"):
        st.write("Thank you for using the Habit Tracking App. Have a nice day!")


if __name__ == "__main__":
    main()