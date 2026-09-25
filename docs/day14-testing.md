# Day 14 – End-to-End Testing and Incident Logging

## Objective

Validate the complete IceStream observability pipeline and implement incident logging for pipeline failures and recovery.

## Test Scenarios

### 1. Valid Event

Valid checkout events pass all data quality checks.

### 2. Null Customer

Events with a null `customer_id` are rejected.

### 3. Negative Amount

Events with `amount <= 0` are rejected.

### 4. Null Tax

Events with missing `tax_amount` are rejected.

### 5. Schema Drift

Unexpected fields such as `discount_code` are detected.

### 6. Circuit Breaker

The circuit remains `CLOSED` at exactly 2% error rate and opens when the error rate exceeds 2%.

### 7. Dead Letter Queue

Invalid events are quarantined in the DLQ with their original event, reason, error type, timestamp and pipeline information.

### 8. Incident Logging

Circuit opening and recovery events are recorded with incident ID, timestamp, severity, error rate, DLQ count and circuit state.

### 9. Recovery

The circuit can be reset and returned to the `CLOSED` state.

## End-to-End Flow

Python Generator  
→ Kafka  
→ Flink  
→ Data Quality  
→ Iceberg / DLQ  
→ Circuit Breaker  
→ Incident Logger  
→ WebSocket Alert  
→ React Flow Dashboard

## Test Configuration

Pytest configuration is defined in `pytest.ini`:

- `quality`
- `tests`

Test files follow the `test_*.py` naming convention.

## Test Result

```text
35 passed in 0.16s