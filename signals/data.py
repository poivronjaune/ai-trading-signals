# signals/data.py

import pandas as pd

def load_data(file_path: str) -> pd.DataFrame:
    """
    Loads and validates stock data from a CSV file.

    Args:
        file_path: The path to the CSV file.

    Returns:
        A pandas DataFrame with the loaded data.

    Raises:
        FileNotFoundError: If the file is not found.
        ValueError: If required columns are missing.
    """
    try:
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        raise FileNotFoundError(f"Error: The file at {file_path} was not found.")

    required_columns = ['Date', 'Close', 'High']
    if not all(col in df.columns for col in required_columns):
        raise ValueError(f"Input CSV must contain the following columns: {required_columns}")

    df['Date'] = pd.to_datetime(df['Date'])
    return df
