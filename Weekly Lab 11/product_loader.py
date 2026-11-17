import csv

from Inventory import Inventory
from product_factory import ProductFactory
from supplier import Supplier


def load_products(path: str, inventory: Inventory, supplier: Supplier) -> None:
    """Load products from a CSV file into the inventory, skipping bad rows."""
    try:
        file = open(path, newline="")
    except FileNotFoundError:
        print(f"Products file not found: {path}")
    else:
        loaded = 0
        with file:
            reader = csv.reader(file)
            next(reader, None)                      # skip the header row
            for line_number, row in enumerate(reader, start=2):
                if not row:                         # ignore blank lines
                    continue
                try:
                    product_type, product_id, name, price, stock = row
                    if inventory.find_product(product_id.strip()):
                        raise ValueError(f"duplicate product ID {product_id.strip()}")
                    product = ProductFactory.create(product_type, product_id.strip(), name.strip(),
                                                    price, stock, supplier)
                    inventory.add_product(product)
                    loaded += 1
                except ValueError as error:         # unknown type, bad number, wrong column count, rule broken
                    print(f"Skipping line {line_number} ({error}).")
        print(f"{loaded} products loaded.")
    finally:
        print("Load attempt finished.")
