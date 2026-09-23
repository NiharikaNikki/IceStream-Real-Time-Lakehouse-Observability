from datetime import datetime, timezone

from pyiceberg.catalog import load_catalog
from pyarrow import Table as ArrowTable


catalog = load_catalog(
    "icestream",
    type="rest",
    uri="http://localhost:8181",
)

TABLE_NAME = "icestream.checkout_events"


def append_records(table, records):
    arrow_table = ArrowTable.from_pylist(
        records,
        schema=table.schema().as_arrow(),
    )

    table.append(arrow_table)


def print_snapshots(table):
    print("\nSnapshot history:")

    for snapshot in table.history():
        print(
            f"Snapshot ID: {snapshot.snapshot_id} | "
            f"Timestamp: {snapshot.timestamp_ms}"
        )


def main():
    table = catalog.load_table(TABLE_NAME)

    print("IceStream - Snapshot 3 Anomaly Demo")
    print("=" * 45)

    # Intentional bad record
    anomaly_record = {
        "transaction_id": "TXN-ANOMALY-001",
        "customer_id": None,
        "amount": -500.0,
        "tax_amount": None,
        "currency": "INR",
        "payment_method": "CARD",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

    append_records(table, [anomaly_record])

    print("\nAnomalous record appended:")
    print(f"Transaction ID : {anomaly_record['transaction_id']}")
    print(f"Customer ID    : {anomaly_record['customer_id']}")
    print(f"Amount         : {anomaly_record['amount']}")
    print(f"Tax Amount     : {anomaly_record['tax_amount']}")

    print_snapshots(table)


if __name__ == "__main__":
    main()