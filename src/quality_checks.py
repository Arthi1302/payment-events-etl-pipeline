import os
import pandas as pd

CURATED_DATA_PATH = "data/curated/payments_curated.parquet"

REQUIRED_COLUMNS = {
    "transaction_id",
    "user_id",
    "amount",
    "currency",
    "payment_method",
    "status",
    "failure_reason",
    "event_timestamp"
}

ALLOWED_STATUSES = {"SUCCESS", "FAILED"}


def load_curated_data() -> pd.DataFrame:
    if not os.path.exists(CURATED_DATA_PATH):
        raise FileNotFoundError("❌ Curated data file not found")

    return pd.read_parquet(CURATED_DATA_PATH)


def check_schema(df: pd.DataFrame):
    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise ValueError(f"❌ Schema check failed. Missing columns: {missing}")
    print("✅ Schema check passed")


def check_nulls(df: pd.DataFrame):
    critical_cols = ["transaction_id", "user_id", "event_timestamp"]
    null_counts = df[critical_cols].isnull().sum()

    if null_counts.any():
        raise ValueError(f"❌ Null check failed:\n{null_counts}")
    print("✅ Null check passed")


def check_duplicates(df: pd.DataFrame):
    dup_count = df.duplicated(subset=["transaction_id"]).sum()
    if dup_count > 0:
        raise ValueError(f"❌ Duplicate check failed. {dup_count} duplicates found")
    print("✅ Duplicate check passed")


def check_business_rules(df: pd.DataFrame):
    if (df["amount"] <= 0).any():
        raise ValueError("❌ Business rule failed: amount must be > 0")

    invalid_status = set(df["status"].unique()) - ALLOWED_STATUSES
    if invalid_status:
        raise ValueError(f"❌ Invalid status values found: {invalid_status}")

    print("✅ Business rules check passed")


def main():
    print("🔍 Loading curated data...")
    df = load_curated_data()

    print("🔎 Running data quality checks...")
    check_schema(df)
    check_nulls(df)
    check_duplicates(df)
    check_business_rules(df)

    print("🎉 All data quality checks passed successfully!")


if __name__ == "__main__":
    main()
