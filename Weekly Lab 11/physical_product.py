from product import Product
from can_be_shipped import CanBeShipped
from supplier import Supplier


class PhysicalProduct(Product, CanBeShipped):
    """A product that is physically stored and shipped."""

    PRODUCT_TYPE: str = "physical"
    BASE_SHIPPING_FEE: float = 5.00
    RATE_PER_KG: float = 2.50

    def __init__(self, product_id: str, name: str, price: float, stock: int, supplier: Supplier, weight: float):
        super().__init__(product_id, name, price, stock, supplier)
        self.weight: float = float(weight)

    def display_information(self) -> None:
        super().display_information()
        print(f" | Weight: {self.weight:.2f} kg")

    def get_fulfilment_info(self) -> str:
        return "This product requires physical shipping."

    def calculate_shipping_cost(self) -> float:
        return self.BASE_SHIPPING_FEE + (self.RATE_PER_KG * self.weight)

    def to_dict(self) -> dict:
        data = super().to_dict()
        data["type"] = self.PRODUCT_TYPE
        data["weight"] = self.weight
        return data

    @classmethod
    def from_dict(cls, data: dict) -> "PhysicalProduct":
        supplier = Supplier.from_dict(data["supplier"])
        return cls(
            product_id=data["id"],
            name=data["name"],
            price=data["price"],
            stock=data["stock"],
            supplier=supplier,
            weight=data["weight"]
        )