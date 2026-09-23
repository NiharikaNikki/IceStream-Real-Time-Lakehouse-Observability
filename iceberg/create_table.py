from pyiceberg.catalog import load_catalog
from pyiceberg.schema import Schema
from pyiceberg.types import (
    NestedField,
    StringType,
    DoubleType,
)
from pyiceberg.partitioning import PartitionSpec


catalog = load_catalog(
    "icestream",
    type="rest",
    uri="http://localhost:8181",
)

NAMESPACE = "icestream"
TABLE_NAME = "checkout_events"


def main():
    # Create namespace if it does not exist
    namespaces = catalog.list_namespaces()

    if (NAMESPACE,) not in namespaces:
        catalog.create_namespace(NAMESPACE)
        print(f"Created namespace: {NAMESPACE}")
    else:
        print(f"Namespace already exists: {NAMESPACE}")

    # Define Iceberg schema
    schema = Schema(
        NestedField(
            id=1,
            name="transaction_id",
            type=StringType(),
            required=True,
        ),
        NestedField(
            id=2,
            name="customer_id",
            type=StringType(),
            required=False,
        ),
        NestedField(
            id=3,
            name="amount",
            type=DoubleType(),
            required=True,
        ),
        NestedField(
            id=4,
            name="tax_amount",
            type=DoubleType(),
            required=False,
        ),
        NestedField(
            id=5,
            name="currency",
            type=StringType(),
            required=True,
        ),
        NestedField(
            id=6,
            name="payment_method",
            type=StringType(),
            required=True,
        ),
        NestedField(
            id=7,
            name="timestamp",
            type=StringType(),
            required=True,
        ),
    )

    table_identifier = f"{NAMESPACE}.{TABLE_NAME}"

    # Create table if it does not exist
    if catalog.table_exists(table_identifier):
        print(f"Table already exists: {table_identifier}")
    else:
        table = catalog.create_table(
            identifier=table_identifier,
            schema=schema,
            partition_spec=PartitionSpec(),
        )
        print(f"Created table: {table.identifier}")

    # Load table
    table = catalog.load_table(table_identifier)

    print("\nIceberg table ready!")
    print(f"Table: {table._identifier}")
    print(f"Location: {table.location()}")

    print("\nSchema:")
    print(table.schema())


if __name__ == "__main__":
    main()