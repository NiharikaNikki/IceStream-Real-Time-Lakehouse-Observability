from .validator import validate_event
from .circuit_breaker import CircuitBreaker


breaker = CircuitBreaker(threshold=2.0)


def process_event(event):
    is_valid, reason = validate_event(event)

    if is_valid:
        breaker.record_valid()
        status = "VALID"
    else:
        breaker.record_invalid()
        status = "INVALID"

    return status, reason


base_event = {
    "transaction_id": "TXN-001",
    "customer_id": "CUST-001",
    "amount": 1000,
    "tax_amount": 180,
    "currency": "INR",
    "payment_method": "UPI",
    "timestamp": "2026-09-15T10:00:00+00:00",
}


# 98 valid records
for i in range(98):
    event = base_event.copy()
    event["transaction_id"] = f"TXN-{i:06d}"
    process_event(event)


# 3 invalid records
for i in range(3):
    event = base_event.copy()
    event["transaction_id"] = f"BAD-{i:06d}"
    event["amount"] = -100
    process_event(event)


print("Quality + Circuit Breaker")
print("-------------------------")

print(f"Total Records : {breaker.total_records}")
print(f"Invalid Records : {breaker.invalid_records}")
print(f"Error Rate : {breaker.error_rate():.2f}%")
print(f"Circuit State : {breaker.state}")