from product import Product
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from supplier import Supplier


class ProductFactory:
    """Single place that knows which concrete Product class to build.
    Depends on Product subclasses («creates») but stores nothing."""

    @staticmethod
    def create(product_type: str, product_id: str, name: str, price: float,
               stock_quantity: int, supplier: Supplier,
               weight: float = 0.0, download_size: float = 0.0) -> Product:
        """Build a product from a type string.
        weight is used for 'physical', download_size for 'digital' (both optional,
        because e.g. the CSV file does not contain them)."""
        product_type = str(product_type).strip().lower()
        if product_type == PhysicalProduct.PRODUCT_TYPE:
            return PhysicalProduct(product_id, name, price, stock_quantity, supplier, weight)
        elif product_type == DigitalProduct.PRODUCT_TYPE:
            return DigitalProduct(product_id, name, price, stock_quantity, supplier, download_size)
        else:
            raise ValueError(f"Unknown product type: {product_type}")

    @staticmethod
    def from_dict(data: dict) -> Product:
        """Rebuild a product from saved JSON data (used by load_inventory)."""
        product_type = data.get("type")
        if product_type == PhysicalProduct.PRODUCT_TYPE:
            return PhysicalProduct.from_dict(data)
        elif product_type == DigitalProduct.PRODUCT_TYPE:
            return DigitalProduct.from_dict(data)
        else:
            raise ValueError(f"Unknown product type: {product_type!r}")
