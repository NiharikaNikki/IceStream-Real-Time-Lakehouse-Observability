from pyiceberg.catalog import load_catalog


catalog = load_catalog(
    "icestream",
    type="rest",
    uri="http://localhost:8181",
)

TABLE_NAME = "icestream.checkout_events"


def main():
    table = catalog.load_table(TABLE_NAME)

    print("IceStream - Iceberg Time Travel")
    print("=" * 45)

    snapshots = list(table.snapshots())

    print("\nAvailable snapshots:")

    for snapshot in snapshots:
        print(
            f"Snapshot ID: {snapshot.snapshot_id} | "
            f"Timestamp: {snapshot.timestamp_ms}"
        )

    if len(snapshots) < 3:
        print("\nAt least 3 snapshots are required.")
        return

    # Snapshot 2 = state before anomaly
    healthy_snapshot = snapshots[-2]

    print("\nHealthy snapshot selected:")
    print(f"Snapshot ID: {healthy_snapshot.snapshot_id}")
    print(f"Timestamp: {healthy_snapshot.timestamp_ms}")

    # Read the table as it existed at Snapshot 2
    scan = table.scan(
        snapshot_id=healthy_snapshot.snapshot_id
    )

    rows = scan.to_arrow().to_pylist()

    print("\nTime-travelled data:")
    print("-" * 45)

    for row in rows:
        print(
            f"{row['transaction_id']} | "
            f"{row['customer_id']} | "
            f"₹{row['amount']}"
        )

    print("\nTime Travel Result")
    print("-" * 45)
    print(f"Records visible at Snapshot 2: {len(rows)}")

    anomaly_found = any(
        row["transaction_id"] == "TXN-ANOMALY-001"
        for row in rows
    )

    if anomaly_found:
        print("Anomaly present: YES")
    else:
        print("Anomaly present: NO")
        print("Healthy state successfully recovered through Time Travel.")


if __name__ == "__main__":
    main()