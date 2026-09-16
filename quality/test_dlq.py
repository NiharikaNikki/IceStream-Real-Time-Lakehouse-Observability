from dlq import DeadLetterQueue


dlq = DeadLetterQueue()


valid_event = {
    "transaction_id": "TXN-001",
    "customer_id": "CUST-001",
    "amount": 1000,
    "tax_amount": 180,
    "currency": "INR",
    "payment_method": "UPI",
    "timestamp": "2026-09-16T10:00:00+00:00",
}


invalid_event_1 = valid_event.copy()
invalid_event_1["customer_id"] = None


invalid_event_2 = valid_event.copy()
invalid_event_2["amount"] = -500


invalid_event_3 = valid_event.copy()
invalid_event_3["tax_amount"] = None


dlq.quarantine(
    invalid_event_1,
    "customer_id is null",
    "NULL_VALUE",
)

dlq.quarantine(
    invalid_event_2,
    "amount must be greater than 0",
    "INVALID_AMOUNT",
)

dlq.quarantine(
    invalid_event_3,
    "tax_amount is null",
    "NULL_VALUE",
)


print("Dead Letter Queue")
print("-------------------------")
print(f"DLQ Count : {dlq.count()}")

for index, record in enumerate(dlq.get_records(), start=1):
    print(f"\nDLQ Record {index}")
    print(f"Transaction ID : {record['original_event']['transaction_id']}")
    print(f"Reason         : {record['reason']}")
    print(f"Error Type     : {record['error_type']}")
    print(f"Pipeline       : {record['pipeline']}")
    print(f"Timestamp      : {record['timestamp']}")