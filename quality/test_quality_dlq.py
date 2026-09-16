from .validator import validate_event
from .dlq import DeadLetterQueue


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


events = []

# 3 valid events
for i in range(3):
    event = valid_event.copy()
    event["transaction_id"] = f"TXN-{i + 1:03d}"
    events.append(event)


# Invalid: null customer
event = valid_event.copy()
event["transaction_id"] = "BAD-001"
event["customer_id"] = None
events.append(event)


# Invalid: negative amount
event = valid_event.copy()
event["transaction_id"] = "BAD-002"
event["amount"] = -500
events.append(event)


# Invalid: schema drift
event = valid_event.copy()
event["transaction_id"] = "BAD-003"
event["discount_code"] = "NEW10"
events.append(event)


valid_count = 0
invalid_count = 0


for event in events:
    is_valid, reason = validate_event(event)

    if is_valid:
        valid_count += 1
        print(
            f"{event['transaction_id']} | "
            f"VALID | Sent to Main Pipeline"
        )
    else:
        invalid_count += 1

        dlq.quarantine(
            event,
            reason,
            "DATA_QUALITY",
        )

        print(
            f"{event['transaction_id']} | "
            f"INVALID | Sent to DLQ | {reason}"
        )


print("\nPipeline Summary")
print("-------------------------")
print(f"Total Records   : {len(events)}")
print(f"Valid Records   : {valid_count}")
print(f"Invalid Records : {invalid_count}")
print(f"DLQ Count       : {dlq.count()}")