from processor import QualityProcessor


processor = QualityProcessor()


events = [
    {
        "transaction_id": "TXN-001",
        "customer_id": "CUST-001",
        "amount": 1000,
        "tax_amount": 180,
        "currency": "INR",
        "payment_method": "UPI",
        "timestamp": "2026-09-10T10:00:00+00:00",
    },
    {
        "transaction_id": "TXN-002",
        "customer_id": None,
        "amount": 1500,
        "tax_amount": 270,
        "currency": "INR",
        "payment_method": "CARD",
        "timestamp": "2026-09-10T10:01:00+00:00",
    },
    {
        "transaction_id": "TXN-003",
        "customer_id": "CUST-003",
        "amount": -500,
        "tax_amount": 90,
        "currency": "INR",
        "payment_method": "UPI",
        "timestamp": "2026-09-10T10:02:00+00:00",
    },
]


for event in events:
    result = processor.process(event)

    print(
        f"{event['transaction_id']} | "
        f"{result['status']} | "
        f"{result['reason']}"
    )


print("\nQuality Metrics")
print("-------------------------")

metrics = processor.get_metrics()

for key, value in metrics.items():
    print(f"{key}: {value}")