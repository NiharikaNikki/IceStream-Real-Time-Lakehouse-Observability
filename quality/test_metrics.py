from metrics import QualityMetrics


metrics = QualityMetrics()

metrics.record_valid()
metrics.record_valid()
metrics.record_valid()

metrics.record_invalid()
metrics.record_invalid()

print("Quality Metrics")
print("-------------------------")
print(f"Total Records : {metrics.total_records}")
print(f"Valid Records : {metrics.valid_records}")
print(f"Invalid Records : {metrics.invalid_records}")
print(f"Error Rate : {metrics.error_rate():.2f}%")