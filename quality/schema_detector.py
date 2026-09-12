EXPECTED_SCHEMA = {
    "transaction_id",
    "customer_id",
    "amount",
    "tax_amount",
    "currency",
    "payment_method",
    "timestamp",
}


def detect_schema_drift(event):
    actual_schema = set(event.keys())

    missing_fields = EXPECTED_SCHEMA - actual_schema
    extra_fields = actual_schema - EXPECTED_SCHEMA

    if missing_fields or extra_fields:
        return {
            "is_drift": True,
            "missing_fields": sorted(missing_fields),
            "extra_fields": sorted(extra_fields),
            "reason": "Schema drift detected",
        }

    return {
        "is_drift": False,
        "missing_fields": [],
        "extra_fields": [],
        "reason": "Schema matches expected schema",
    }