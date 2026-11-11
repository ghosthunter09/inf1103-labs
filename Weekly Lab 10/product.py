from abc import ABC, abstractmethod
from supplier import Supplier


class Product(ABC):
    """
    Abstract base class for all products in the inventory.
    Maintains an association reference to a Supplier.
    """

    def __init__(self, product_id: str, name: str, price: float, stock_quantity: int, supplier: Supplier):
        self._product_id: str = str(product_id)
        self.name: str = str(name)
        self._price: float = float(price)
        self.stock: int = int(stock_quantity)
        self.supplier: Supplier = supplier

    @property
    def product_id(self) -> str:
        return self._product_id

    @property
    def price(self) -> float:
        return self._price

    def update_stock(self, new_stock: int) -> None:
        """Updates the stock quantity for this product."""
        if new_stock >= 0:
            self.stock = int(new_stock)
        else:
            print("Stock quantity cannot be negative.")

    def display_information(self) -> None:
        """Prints common product information alongside its associated supplier."""
        print(f"ID: {self._product_id} | Name: {self.name} | "
              f"Price: ${self._price:.2f} | Stock: {self.stock} | "
              f"Supplier: {self.supplier.name}", end="")

    @abstractmethod
    def get_fulfilment_info(self) -> str:
        """Returns a message describing how this product is fulfilled."""
        pass

    def to_dict(self) -> dict:
        """Converts common product data into a dictionary for JSON persistence."""
        return {
            "id": self._product_id,
            "name": self.name,
            "price": self._price,
            "stock": self.stock,
            "supplier": self.supplier.to_dict()
        }