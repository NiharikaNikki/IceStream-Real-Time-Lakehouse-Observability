from pyiceberg.catalog import load_catalog


catalog = load_catalog(
    "icestream",
    type="rest",
    uri="http://localhost:8181",
)

TABLE_NAME = "icestream.checkout_events"


def main():
    table = catalog.load_table(TABLE_NAME)

    print("IceStream - Iceberg Rollback Demo")
    print("=" * 45)

    snapshots = list(table.snapshots())

    print("\nAvailable snapshots:")

    for index, snapshot in enumerate(snapshots, start=1):
        print(
            f"{index}. Snapshot ID: {snapshot.snapshot_id}"
        )

    if len(snapshots) < 3:
        print("\nAt least 3 snapshots are required.")
        return

    # Snapshot 2 = healthy state before anomaly
    healthy_snapshot = snapshots[-2]

    print("\nHealthy snapshot selected:")
    print(f"Snapshot ID: {healthy_snapshot.snapshot_id}")

    print("\nRolling back table...")

    table.manage_snapshots().rollback_to_snapshot(
        healthy_snapshot.snapshot_id
    ).commit()

    # Reload table after rollback
    table = catalog.load_table(TABLE_NAME)

    current_snapshot = table.current_snapshot()

    print("\nRollback completed successfully!")
    print(f"Current Snapshot ID: {current_snapshot.snapshot_id}")

    # Verify current data
    rows = table.scan().to_arrow().to_pylist()

    print("\nCurrent table data after rollback:")
    print("-" * 45)

    for row in rows:
        print(
            f"{row['transaction_id']} | "
            f"{row['customer_id']} | "
            f"₹{row['amount']}"
        )

    print("\nRollback Verification")
    print("-" * 45)
    print(f"Records after rollback: {len(rows)}")

    anomaly_found = any(
        row["transaction_id"] == "TXN-ANOMALY-001"
        for row in rows
    )

    if anomaly_found:
        print("❌ Anomaly still present")
    else:
        print("✅ Anomaly removed")
        print("✅ Healthy snapshot restored")


if __name__ == "__main__":
    main()