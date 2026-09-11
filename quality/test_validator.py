from validator import validate_event


valid_event = {
    "transaction_id": "TXN-000001",
    "customer_id": "CUST-1234",
    "amount": 2500.00,
    "tax_amount": 450.00,
    "currency": "INR",
    "payment_method": "UPI",
    "timestamp": "2026-09-10T10:00:00+00:00",
}


invalid_customer = valid_event.copy()
invalid_customer["customer_id"] = None


negative_amount = valid_event.copy()
negative_amount["amount"] = -500


invalid_tax = valid_event.copy()
invalid_tax["tax_amount"] = None


schema_drift = valid_event.copy()
schema_drift["discount_code"] = "NEW10"


test_cases = [
    ("Valid Event", valid_event),
    ("Null Customer", invalid_customer),
    ("Negative Amount", negative_amount),
    ("Null Tax", invalid_tax),
    ("Schema Drift", schema_drift),
]


for name, event in test_cases:
    is_valid, reason = validate_event(event)

    status = "VALID" if is_valid else "INVALID"

    print(f"{name:20} | {status:7} | {reason}")