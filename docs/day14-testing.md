# Day 14 – End-to-End Testing and Incident Logging

## Objective

Validate the complete IceStream observability pipeline and implement incident logging for pipeline failures and recovery.

## Test Scenarios

### 1. Valid Event

Valid checkout events pass all data quality checks.

### 2. Null Customer

Events with a null customer_id are rejected.

### 3. Negative Amount

Events with amount <= 0 are rejected.

### 4. Null Tax

Events with missing tax_amount are rejected.

### 5. Schema Drift

Unexpected fields such as discount_code are detected.

### 6. Circuit Breaker

The circuit remains CLOSED at 2% error rate and opens when the error rate exceeds 2%.

### 7. Dead Letter Queue

Invalid events are quarantined in the DLQ.

### 8. Incident Logging

Circuit opening and recovery events are recorded with timestamps, severity, error rate, DLQ count and circuit state.

### 9. Recovery

After recovery, the circuit returns to CLOSED state.

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

## Result

The end-to-end test suite validates data quality, schema drift detection, circuit breaker behavior, DLQ quarantine, incident logging and recovery.