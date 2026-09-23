from pyiceberg.catalog import load_catalog


catalog = load_catalog(
    "icestream",
    type="rest",
    uri="http://localhost:8181",
)


def get_catalog():
    return catalog


if __name__ == "__main__":
    print("IceStream Iceberg REST Catalog")
    print("Catalog loaded successfully!")
    print("Namespaces:", catalog.list_namespaces())