from dataclasses import dataclass
from datetime import datetime


@dataclass
class CheckoutEvent:
    transaction_id: str
    customer_id: str | None
    amount: float
    tax_amount: float | None
    currency: str
    payment_method: str
    timestamp: str

    def to_dict(self):
        return {
            "transaction_id": self.transaction_id,
            "customer_id": self.customer_id,
            "amount": self.amount,
            "tax_amount": self.tax_amount,
            "currency": self.currency,
            "payment_method": self.payment_method,
            "timestamp": self.timestamp,
        }