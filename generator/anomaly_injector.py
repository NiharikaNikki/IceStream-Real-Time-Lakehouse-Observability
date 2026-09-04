import random


def inject_anomaly(event):
    anomaly_type = random.choice([
        "none",
        "none",
        "none",
        "null_customer",
        "negative_amount",
        "null_tax",
        "schema_drift"
    ])

    if anomaly_type == "null_customer":
        event["customer_id"] = None

    elif anomaly_type == "negative_amount":
        event["amount"] = -abs(event["amount"])

    elif anomaly_type == "null_tax":
        event["tax_amount"] = None

    elif anomaly_type == "schema_drift":
        event["discount_code"] = "NEW10"

    return event, anomaly_type