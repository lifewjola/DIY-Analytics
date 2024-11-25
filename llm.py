from groq import Groq
import streamlit as st
from summary import summarize_data

# Initialize Groq API
GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
groq_client = Groq(api_key=GROQ_API_KEY)

def ask_llm(query, data_summary):
    system_message = (
        f"You are a professional data analyst proficient in Python programming.\n"
        f"Based on the following dataset summary:\n{data_summary}\n"
        "Provide clean python code using pandas and matplotlib (only the code, nothing else) that when executed will:\n"
        f" Answer the user's question: '{query}'.\n"
        "Note that the unique values of each column are supposed to guide you on how to generate value-specific code/ insights."
        "The code should contain a visualization that is well labelled and inprint whatever text you need to add on the visualization fig."
        "Assume the dataset has been read into a dataframe called df."
        "If the query involves generating a chart (e.g., bar plot), please ensure the chart displays no more than 10 categories (top or bottom)."
        "If the user specifically requests to show all categories, include that in the code. If no specific instruction is provided, limit the chart to the top or bottom 10 categories based on the count or value"
    )

    # Chat messages for the LLM
    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": query}
    ]

    # Query Llama
    response = groq_client.chat.completions.create(
        model="llama3-70b-8192",
        messages=messages
    )

    # Return generated code
    return response.choices[0].message.content