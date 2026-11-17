from product import Product


class Inventory:
    """
    Aggregates Product instances.
    Products exist independently of the inventory.
    """

    def __init__(self):
        self.products: list[Product] = []

    def add_product(self, product: Product) -> None:
        """Add an existing Product object to the inventory."""
        self.products.append(product)

    def remove_product(self, product_id: str) -> None:
        """Remove matching Product reference from inventory."""
        self.products = [p for p in self.products if p.product_id != product_id]

    def find_product(self, product_id: str) -> Product | None:
        """Return the matching Product, or None if not found."""
        for product in self.products:
            if product.product_id == str(product_id):
                return product
        return None

    def display_all_products(self) -> None:
        """Demonstrates polymorphism and LSP across all stored products."""
        print("\nCurrent Inventory")
        print("-" * 75)
        if not self.products:
            print("No products currently in inventory.")
        else:
            for product in self.products:
                product.display_information()
        print("-" * 75)