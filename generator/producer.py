import json
import random
import time
from datetime import datetime, timezone

from anomaly_injector import inject_anomaly


PAYMENT_METHODS = ["UPI", "CARD", "NET_BANKING", "WALLET"]


def generate_event(transaction_number):

    event = {
        "transaction_id": f"TXN-{transaction_number:06d}",
        "customer_id": f"CUST-{random.randint(1000, 9999)}",
        "amount": round(random.uniform(100, 5000), 2),
        "tax_amount": None,
        "currency": "INR",
        "payment_method": random.choice(PAYMENT_METHODS),
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

    event["tax_amount"] = round(event["amount"] * 0.18, 2)

    return event


def main():

    transaction_number = 1

    print("🚀 IceStream E-commerce Event Generator Started")
    print("Press CTRL+C to stop.\n")

    while True:

        event = generate_event(transaction_number)

        event, anomaly_type = inject_anomaly(event)

        print(
            f"Event: {json.dumps(event)} | "
            f"Anomaly: {anomaly_type}"
        )

        transaction_number += 1

        time.sleep(2)


if __name__ == "__main__":
    main()