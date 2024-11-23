import streamlit as st
import pandas as pd
from summary import summarize_data
from llm import ask_llm
from execute import execute_generated_code

# Streamlit UI
st.title("DIY Analytics")

uploaded_file = st.file_uploader("Upload your CSV dataset to get started!", type=["csv"])


if uploaded_file:
    data = pd.read_csv(uploaded_file)
    summary_data = summarize_data(data)
    st.write("#### Data Preview:")
    st.dataframe(data.head())

    if st.checkbox("Show Data Summary"):
        missing_values, duplicated_values, summary_statistics = st.tabs(["Missing Values", "Duplicated Values", "Summary Statistics"])
        total_missing_values_by_column = data.isnull().sum()
        missing_values.write(total_missing_values_by_column)
        missing_values.write(f"There are {total_missing_values_by_column.sum()} missing values in your dataset.")

        total_duplicated_values_by_column = data.duplicated().sum()
        duplicated_values.write(total_duplicated_values_by_column)
        duplicated_values.write(f"There are {total_duplicated_values_by_column.sum()} duplicated values in your dataset.")

        summary_statistics.write("#### Summary Statistics")
        summary_statistics.dataframe(data.describe())


    st.header("Chat with your data!")
    user_query = st.text_input("Ask a question about your dataset:")
    
    with st.spinner("Insights cooking..."):
        if user_query:
            code = ask_llm(user_query, summary_data)
            if st.checkbox("Show code"):
                st.code(code, language="python")
            
            try:
                results, output = execute_generated_code(code, data)

                if "plt" in results:
                    st.pyplot(results["plt"].gcf())  
                if output:
                    st.write(output) 

                if isinstance(results, str): 
                    st.error(results)
                else:
                    st.toast("Code executed successfully.")
                
            except Exception as e:
                st.error(f"Error executing code: {e}")
