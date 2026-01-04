import os
import uuid
import random
from datetime import datetime, timedelta

import pandas as pd

# -----------------------------------
# Configuration
# -----------------------------------
RAW_DATA_DIR = "data/raw"
NUM_RECORDS = 1000

PAYMENT_METHODS = ["UPI", "CARD"]
STATUSES = ["SUCCESS", "FAILED"]
FAILURE_REASONS = [
    "INSUFFICIENT_FUNDS",
    "NETWORK_ERROR",
    "BANK_DECLINED",
    "TIMEOUT"
]


# -----------------------------------
# Helper Functions
# -----------------------------------
def generate_random_timestamp(days_back=7):
    """
    Generate a random timestamp within the last N days
    """
    end_time = datetime.now()
    start_time = end_time - timedelta(days=days_back)
    random_seconds = random.randint(0, int((end_time - start_time).total_seconds()))
    return start_time + timedelta(seconds=random_seconds)


def generate_payment_event():
    """
    Generate a single payment transaction event
    """
    status = random.choices(
        STATUSES,
        weights=[0.85, 0.15]  # 85% success, 15% failure
    )[0]

    return {
        "transaction_id": str(uuid.uuid4()),
        "user_id": f"user_{random.randint(1, 300)}",
        "amount": round(random.uniform(10, 5000), 2),
        "currency": "INR",
        "payment_method": random.choice(PAYMENT_METHODS),
        "status": status,
        "failure_reason": random.choice(FAILURE_REASONS) if status == "FAILED" else None,
        "event_timestamp": generate_random_timestamp().isoformat()
    }


# -----------------------------------
# Main Execution
# -----------------------------------
def main():
    os.makedirs(RAW_DATA_DIR, exist_ok=True)

    events = [generate_payment_event() for _ in range(NUM_RECORDS)]
    df = pd.DataFrame(events)

    today = datetime.now().strftime("%Y%m%d")

    csv_file = os.path.join(RAW_DATA_DIR, f"payments_{today}.csv")
    json_file = os.path.join(RAW_DATA_DIR, f"payments_{today}.json")

    df.to_csv(csv_file, index=False)
    df.to_json(json_file, orient="records", lines=True)

    print(f"✅ Generated {NUM_RECORDS} payment events")
    print(f"📄 CSV file: {csv_file}")
    print(f"📄 JSON file: {json_file}")


if __name__ == "__main__":
    main()
