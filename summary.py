import pandas as pd

def summarize_data(df):
    columns = list(df.columns)
    data_types = df.dtypes.to_dict()

    unique_values = {}

    for column in df.columns:
        if df[column].dtype == 'object' or df[column].dtype.name == 'category':
            unique_values[column] = df[column].unique().tolist()
        elif 'datetime' in str(df[column].dtype):
            date_sample = df[column].dropna().iloc[0]
            inferred_format = pd.to_datetime([date_sample]).strftime('%Y-%m-%d')[0]
            unique_values[column] = f"Date format: {inferred_format}"


    summary = (
        f"Columns: {columns}\n"
        f"Data Types: {data_types}\n"
        f"Unique Values for Categorical/Date Columns:\n{unique_values}"
    )
    
    return summary
