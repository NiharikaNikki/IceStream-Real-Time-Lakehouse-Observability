import json
import random
import time
from datetime import datetime, timezone

from kafka import KafkaProducer

from anomaly_injector import inject_anomaly


KAFKA_BROKER = "localhost:9092"
KAFKA_TOPIC = "checkout-events"

PAYMENT_METHODS = ["UPI", "CARD", "NET_BANKING", "WALLET"]


def generate_event(transaction_number):

    event = {
        "transaction_id": f"TXN-{transaction_number:06d}",
        "customer_id": f"CUST-{random.randint(1000, 9999)}",
        "amount": round(random.uniform(100, 5000), 2),
        "tax_amount": None,
        "currency": "INR",
        "payment_method": random.choice(PAYMENT_METHODS),
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

    event["tax_amount"] = round(event["amount"] * 0.18, 2)

    return event


def main():

    producer = KafkaProducer(
        bootstrap_servers=KAFKA_BROKER,
        value_serializer=lambda value: json.dumps(value).encode("utf-8")
    )

    transaction_number = 1

    print("🚀 IceStream Kafka Producer Started")
    print(f"📡 Broker: {KAFKA_BROKER}")
    print(f"📦 Topic: {KAFKA_TOPIC}")
    print("Press CTRL+C to stop.\n")

    try:

        while True:

            event = generate_event(transaction_number)

            event, anomaly_type = inject_anomaly(event)

            producer.send(KAFKA_TOPIC, value=event)

            producer.flush()

            print(
                f"Sent: {event['transaction_id']} | "
                f"Anomaly: {anomaly_type}"
            )

            transaction_number += 1

            time.sleep(2)

    except KeyboardInterrupt:

        print("\n🛑 Producer stopped.")

    finally:

        producer.close()


if __name__ == "__main__":
    main()