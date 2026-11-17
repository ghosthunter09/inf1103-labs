from product import Product
from order_line import OrderLine
from discount_strategy import DiscountStrategy, NoDiscount


class Order:
    """
    Manages OrderLine objects via Composition.
    Uses (but does not own) a DiscountStrategy: Association.
    """

    def __init__(self, order_id: str, discount: DiscountStrategy | None = None):
        self.order_id: str = str(order_id)
        self.order_lines: list[OrderLine] = []
        self.discount: DiscountStrategy = discount if discount is not None else NoDiscount()

    def set_discount(self, discount: DiscountStrategy) -> None:
        """Swap the discount strategy at any time."""
        self.discount = discount

    def add_order_line(self, product: Product, quantity: int) -> None:
        """Creates and attaches a new OrderLine internally."""
        order_line = OrderLine(product, quantity)
        self.order_lines.append(order_line)

    def calculate_total(self) -> float:
        """Sum of line subtotals, passed through the discount strategy."""
        total = sum(line.calculate_subtotal() for line in self.order_lines)
        return self.discount.apply(total)

    def display_order(self) -> None:
        print(f"\nOrder ID: {self.order_id}")
        for line in self.order_lines:
            line.display_line()
        print(f"Total: ${self.calculate_total():.2f}")

    def remove_order_line(self, product_id: str) -> None:
        """Removes the OrderLine matching the given product_id."""
        self.order_lines = [
            line for line in self.order_lines if line.product.product_id != product_id
        ]
