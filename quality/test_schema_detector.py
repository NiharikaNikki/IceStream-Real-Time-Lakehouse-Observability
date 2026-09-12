from schema_detector import detect_schema_drift


valid_event = {
    "transaction_id": "TXN-001",
    "customer_id": "CUST-001",
    "amount": 1000,
    "tax_amount": 180,
    "currency": "INR",
    "payment_method": "UPI",
    "timestamp": "2026-09-11T10:00:00+00:00",
}


extra_field_event = valid_event.copy()
extra_field_event["discount_code"] = "NEW10"


missing_field_event = valid_event.copy()
del missing_field_event["tax_amount"]


test_cases = [
    ("Valid Schema", valid_event),
    ("Extra Field", extra_field_event),
    ("Missing Field", missing_field_event),
]


for name, event in test_cases:
    result = detect_schema_drift(event)

    status = "DRIFT" if result["is_drift"] else "MATCH"

    print(f"\n{name}")
    print("-------------------------")
    print(f"Status         : {status}")
    print(f"Missing Fields : {result['missing_fields']}")
    print(f"Extra Fields   : {result['extra_fields']}")
    print(f"Reason         : {result['reason']}")