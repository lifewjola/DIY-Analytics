from groq import Groq
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import io
import traceback

def summarize_dataset(file_path):
    df = pd.read_csv(file_path)  # Or use `pd.read_excel` for Excel files
    summary = {
        "columns": list(df.columns),
        "dtypes": {col: str(df[col].dtype) for col in df.columns},
        "num_rows": len(df),
        "num_columns": len(df.columns),
        "sample_data": df.head(5).to_dict(orient="records")
    }
    return summary

# Set up Groq API
GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
groq_client = Groq(api_key=GROQ_API_KEY)

# Function to query the LLM
def ask_llm(query, data):

    system_message = (
       f"You are a data analyst. Based on the following dataset summary: {data_summary}",
    "Generate Python code using pandas and matplotlib/seaborn/plotly to:",
    f"1. Answer the question: '{query}'",
    "2. Always include a labeled visualization."
    )

    # Define messages for the chat completion
    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": query}
    ]

    # Call the Groq chat completion API
    response = groq_client.chat.completions.create(
        model="llama3-70b-8192",
        messages=messages
    )

    # Extract and return the response and code
    reply = response.choices[0].message.content
    # if "### Answer:" in reply and "### Code:" in reply:
    #     answer = reply.split("### Answer:")[1].split("### Code:")[0].strip()
    #     code = reply.split("### Code:")[1].strip()
    # else:
    #     answer = reply.strip()
    #     code = None

    # # return answer, code


def execute_code(generated_code, dataset_path):
    output = {"text": "", "visual": None, "error": None, "code": generated_code}
    try:
        namespace = {"plt": plt}
        exec(generated_code, namespace)

        # Capture text results
        output["text"] = namespace.get("result", "No textual output provided.")

        # Capture visualizations
        fig = plt.gcf()
        buf = io.BytesIO()
        fig.savefig(buf, format='png')
        buf.seek(0)
        output["visual"] = buf.read()

        plt.close(fig)
    except Exception as e:
        output["error"] = traceback.format_exc()

    return output


import streamlit as st

st.title("DIY Analytics Platform with LLM")

uploaded_file = st.file_uploader("Upload your dataset", type="csv")
if uploaded_file:
    query = st.text_input("Ask a question about your dataset:")
    show_code = st.checkbox("Show Python code")

    if st.button("Analyze"):
        # Summarize dataset
        file_path = f"{uploaded_file.name}"
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        data_summary = summarize_dataset(file_path)

        # Generate and execute code
        code = generate_code_from_query(query, data_summary)
        result = execute_code(code, file_path)

        # Display results
        if result["error"]:
            st.error(f"Error: {result['error']}")
        else:
            st.markdown(result["text"])
            st.image(result["visual"])
            if show_code:
                st.code(result["code"])
