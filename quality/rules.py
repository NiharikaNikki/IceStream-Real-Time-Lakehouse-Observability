EXPECTED_FIELDS = {
    "transaction_id",
    "customer_id",
    "amount",
    "tax_amount",
    "currency",
    "payment_method",
    "timestamp",
}


def validate_required_fields(event):
    if not event.get("transaction_id"):
        return False, "transaction_id is null"

    if not event.get("customer_id"):
        return False, "customer_id is null"

    if event.get("tax_amount") is None:
        return False, "tax_amount is null"

    return True, None


def validate_amount(event):
    amount = event.get("amount")

    if amount is None:
        return False, "amount is null"

    try:
        if float(amount) <= 0:
            return False, "amount must be greater than 0"
    except (TypeError, ValueError):
        return False, "amount is invalid"

    return True, None


def validate_timestamp(event):
    timestamp = event.get("timestamp")

    if not timestamp:
        return False, "timestamp is null"

    try:
        from datetime import datetime
        datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
    except (TypeError, ValueError):
        return False, "timestamp is invalid"

    return True, None


def validate_schema(event):
    actual_fields = set(event.keys())

    missing_fields = EXPECTED_FIELDS - actual_fields
    extra_fields = actual_fields - EXPECTED_FIELDS

    if missing_fields:
        return False, f"missing fields: {sorted(missing_fields)}"

    if extra_fields:
        return False, f"unexpected fields: {sorted(extra_fields)}"

    return True, None