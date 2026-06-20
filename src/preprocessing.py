import pandas as pd

def load_data(file_path):
    """Load the dataset"""
    df = pd.read_csv(file_path)
    return df

def clean_data(df):
    """Clean the dataset"""

    # Convert Timestamp to datetime
    df["Timestamp"] = pd.to_datetime(df["Timestamp"])

    # Remove duplicate rows
    df = df.drop_duplicates()

    # Remove missing values
    df = df.dropna()

    # Sort by timestamp
    df = df.sort_values("Timestamp")

    # Reset index
    df.reset_index(drop=True, inplace=True)

    return df

def save_clean_data(df, output_path):
    """Save cleaned data"""
    df.to_csv(output_path, index=False)

if __name__ == "__main__":

    input_file = "data/Toronto Island Ferry Tickets.csv"
    output_file = "data/cleaned_ferry_data.csv"

    df = load_data(input_file)
    df = clean_data(df)
    save_clean_data(df, output_file)

    print("✅ Data cleaned successfully!")