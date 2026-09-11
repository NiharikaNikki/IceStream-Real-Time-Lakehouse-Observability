from .rules import (
    validate_required_fields,
    validate_amount,
    validate_timestamp,
    validate_schema,
)


def validate_event(event):
    checks = [
        validate_required_fields,
        validate_amount,
        validate_timestamp,
        validate_schema,
    ]

    for check in checks:
        is_valid, reason = check(event)

        if not is_valid:
            return False, reason

    return True, "VALID"