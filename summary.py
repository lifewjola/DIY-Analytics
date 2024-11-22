def summarize_data(df):
    columns = list(df.columns)
    num_rows, num_columns = df.shape
    data_types = df.dtypes.to_dict()

    summary = (
        f"Columns: {columns}\n"
        f"Shape: {num_rows} rows, {num_columns} columns\n"
        f"Data Types: {data_types}\n"
    )
    return summary


