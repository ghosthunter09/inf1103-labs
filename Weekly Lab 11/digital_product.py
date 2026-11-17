from product import Product
from supplier import Supplier


class DigitalProduct(Product):
    """A product delivered digitally via download."""

    PRODUCT_TYPE: str = "digital"

    def __init__(self, product_id: str, name: str, price: float, stock: int, supplier: Supplier, download_size: float):
        super().__init__(product_id, name, price, stock, supplier)
        self.download_size: float = float(download_size)

    def display_information(self) -> None:
        super().display_information()
        print(f" | Download Size: {self.download_size:.2f} MB")

    def get_fulfilment_info(self) -> str:
        return "This product is delivered digitally via download."

    def to_dict(self) -> dict:
        data = super().to_dict()
        data["type"] = self.PRODUCT_TYPE
        data["download_size"] = self.download_size
        return data

    @classmethod
    def from_dict(cls, data: dict) -> "DigitalProduct":
        supplier = Supplier.from_dict(data["supplier"])
        return cls(
            product_id=data["id"],
            name=data["name"],
            price=data["price"],
            stock=data["stock"],
            supplier=supplier,
            download_size=data["download_size"]
        )