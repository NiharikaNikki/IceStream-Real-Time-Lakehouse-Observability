from .circuit_breaker import CircuitBreaker


breaker = CircuitBreaker(threshold=2.0)


print("Initial Status")
print("-------------------------")
print(breaker.status())


# 98 valid + 2 invalid = exactly 2%
for _ in range(98):
    breaker.record_valid()

for _ in range(2):
    breaker.record_invalid()


print("\nAfter 2% Error Rate")
print("-------------------------")
print(breaker.status())


# Add one more invalid record
breaker.record_invalid()


print("\nAfter Error Rate Exceeds 2%")
print("-------------------------")
print(breaker.status())


# Recovery
breaker.reset()


print("\nAfter Circuit Reset")
print("-------------------------")
print(breaker.status())