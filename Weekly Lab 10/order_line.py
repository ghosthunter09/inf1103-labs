from product import Product


class OrderLine:
    """
    Represents one line item within an order.
    Holds an association to a Product, but is owned by an Order (Composition).
    """

    def __init__(self, product: Product, quantity: int):
        self.product: Product = product
        self.quantity: int = int(quantity)

    def calculate_subtotal(self) -> float:
        """Returns the product price multiplied by the quantity."""
        return self.product.price * self.quantity

    def display_line(self) -> None:
        print(f"  - {self.product.name} (x{self.quantity}) @ ${self.product.price:.2f} each = ${self.calculate_subtotal():.2f}")