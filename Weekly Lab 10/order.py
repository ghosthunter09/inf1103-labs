from product import Product
from order_line import OrderLine


class Order:
    """
    Manages OrderLine objects via Composition.
    Responsible for creating and managing OrderLine lifecycles.
    """

    def __init__(self, order_id: str):
        self.order_id: str = str(order_id)
        self.order_lines: list[OrderLine] = []

    def add_order_line(self, product: Product, quantity: int) -> None:
        """Creates and attaches a new OrderLine internally."""
        order_line = OrderLine(product, quantity)
        self.order_lines.append(order_line)

    def calculate_total(self) -> float:
        """Calculates total value across all composed order lines."""
        return sum(line.calculate_subtotal() for line in self.order_lines)

    def display_order(self) -> None:
        print(f"\nOrder ID: {self.order_id}")
        for line in self.order_lines:
            line.display_line()
        print(f"Total: ${self.calculate_total():.2f}")