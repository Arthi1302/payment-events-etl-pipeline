import os
import pandas as pd

RAW_DATA_DIR = "data/raw"
CURATED_DATA_DIR = "data/curated"
CURATED_FILE_NAME = "payments_curated.parquet"


def read_raw_data():
    """
    Read all CSV and JSON files from raw data directory
    """
    dataframes = []

    for file in os.listdir(RAW_DATA_DIR):
        file_path = os.path.join(RAW_DATA_DIR, file)

        if file.endswith(".csv"):
            df = pd.read_csv(file_path)
            dataframes.append(df)

        elif file.endswith(".json"):
            df = pd.read_json(file_path, lines=True)
            dataframes.append(df)

    return pd.concat(dataframes, ignore_index=True)


def transform_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Apply cleaning and standardization rules
    """

    # Standardize column names
    df.columns = [col.lower() for col in df.columns]

    # Convert timestamp to datetime
    df["event_timestamp"] = pd.to_datetime(df["event_timestamp"], errors="coerce")

    # Ensure numeric amount
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")

    # Normalize status values
    df["status"] = df["status"].str.upper()

    # Fill missing failure reasons
    df["failure_reason"] = df["failure_reason"].fillna("NA")

    # Drop records with critical nulls
    df = df.dropna(subset=["transaction_id", "user_id", "event_timestamp"])

    return df


def write_curated_data(df: pd.DataFrame):
    """
    Write curated data as Parquet
    """
    os.makedirs(CURATED_DATA_DIR, exist_ok=True)

    output_path = os.path.join(CURATED_DATA_DIR, CURATED_FILE_NAME)
    df.to_parquet(output_path, index=False)

    print(f"✅ Curated data written to {output_path}")


def main():
    print("📥 Reading raw data...")
    raw_df = read_raw_data()

    print(f"🔄 Transforming {len(raw_df)} records...")
    curated_df = transform_data(raw_df)

    print("📦 Writing curated data...")
    write_curated_data(curated_df)

    print("✅ Transformation completed successfully")


if __name__ == "__main__":
    main()
