"""Demonstrates type hints, UML relationships, LSP and polymorphism.
Run:  python test_relationships.py
"""
import gc
import os
import sys
import inspect
import weakref
from typing import get_type_hints

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from supplier import Supplier
from product import Product
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from order import Order
from order_line import OrderLine
from can_be_shipped import CanBeShipped


def section(title: str) -> None:
    print(f"\n=== {title} ===")


def make_supplier() -> Supplier:
    return Supplier("S01", "Global Logistics Co.", "support@globallogistics.com")


def make_products(supplier: Supplier) -> list[Product]:
    return [
        PhysicalProduct("P001", "Laptop", 1200.00, 15, supplier, 2.2),
        DigitalProduct("P003", "Photo Editor", 49.99, 100, supplier, 350.0),
    ]


# ---------------------------------------------------------------- type hints
def test_type_hints() -> None:
    section("Type hints")
    checks = [
        (Supplier.__init__, ["supplier_id", "name", "contact_email"]),
        (Product.__init__, ["product_id", "name", "price", "stock_quantity", "supplier"]),
        (PhysicalProduct.__init__, ["product_id", "name", "price", "stock", "supplier", "weight"]),
        (Order.add_order_line, ["product", "quantity"]),
        (OrderLine.__init__, ["product", "quantity"]),
    ]
    for func, params in checks:
        hints = get_type_hints(func)
        for p in params:
            assert p in hints, f"{func.__qualname__}: '{p}' has no type hint"
        if func.__name__ != "__init__":      # __init__ in this code base has no "-> None"
            assert "return" in hints, f"{func.__qualname__}: no return hint"
        print(f"  OK {func.__qualname__}{inspect.signature(func)}")
    assert get_type_hints(Order.calculate_total)["return"] is float
    assert get_type_hints(Product.get_fulfilment_info)["return"] is str
    assert get_type_hints(Product.to_dict)["return"] is dict


# ------------------------------------------------------------- relationships
def test_composition() -> None:
    section("Composition: Order owns OrderLine")
    supplier = make_supplier()
    laptop = PhysicalProduct("P001", "Laptop", 1200.00, 15, supplier, 2.2)

    order = Order("ORD-1")
    order.add_order_line(laptop, 2)          # caller never builds an OrderLine
    assert isinstance(order.order_lines[0], OrderLine)

    line_ref = weakref.ref(order.order_lines[0])
    product_ref = weakref.ref(laptop)
    del order
    gc.collect()
    assert line_ref() is None, "OrderLine must die with its Order"
    assert product_ref() is not None, "Product must outlive the Order"
    print("  OK OrderLine destroyed with Order; Product survived")


def test_association_order_line_product() -> None:
    section("Association: OrderLine -> Product")
    supplier = make_supplier()
    mouse = PhysicalProduct("P002", "Mouse", 25.50, 40, supplier, 0.1)
    line = OrderLine(mouse, 5)
    assert line.product is mouse             # reference, not a copy
    assert line.calculate_subtotal() == 25.50 * 5
    print("  OK OrderLine references the same Product object")


def test_aggregation_product_supplier() -> None:
    section("Aggregation: Product has a Supplier (shared, independent lifetime)")
    supplier = make_supplier()
    products = make_products(supplier)
    assert all(p.supplier is supplier for p in products)

    supplier_ref = weakref.ref(supplier)
    products.clear()
    gc.collect()
    del_supplier_alive = supplier_ref() is not None
    assert del_supplier_alive, "Supplier must outlive its products"
    print("  OK one Supplier shared by 2 products; survives their deletion")


def test_inheritance() -> None:
    section("Inheritance / realization")
    assert issubclass(PhysicalProduct, Product)
    assert issubclass(DigitalProduct, Product)
    assert issubclass(PhysicalProduct, CanBeShipped)
    assert not issubclass(DigitalProduct, CanBeShipped)
    try:
        Product("X", "x", 1, 1, make_supplier())  # type: ignore[abstract]
    except TypeError:
        print("  OK Product is abstract (cannot be instantiated)")
    else:
        raise AssertionError("Product should be abstract")


# ---------------------------------------------------- LSP and polymorphism
def describe(product: Product) -> str:
    """Written only against Product (same idea as show_product_details)."""
    return f"{product.name}: {product.get_fulfilment_info()}"


def test_lsp() -> None:
    section("Liskov substitution")
    for product in make_products(make_supplier()):
        assert isinstance(describe(product), str)

        product.update_stock(10)             # inherited behaviour unchanged
        assert product.stock == 10
        try:
            product.update_stock(-5)         # same precondition for every subtype
        except ValueError:
            pass
        else:
            raise AssertionError("negative stock must be rejected for every subtype")
        assert product.stock == 10

        data = product.to_dict()             # contract: base keys always present
        assert {"id", "name", "price", "stock", "supplier"} <= data.keys()
        assert data["type"] in ("physical", "digital")
        print(f"  OK {type(product).__name__} substitutable for Product")


def test_polymorphism() -> None:
    section("Polymorphism through Product references")
    inventory: list[Product] = make_products(make_supplier())
    for product in inventory:
        print(f"  [{type(product).__name__}] {describe(product)}")
    messages = {describe(p) for p in inventory}
    assert len(messages) == 2, "each subtype must answer differently"

    shippable = [p for p in inventory if isinstance(p, CanBeShipped)]
    assert [type(p) for p in shippable] == [PhysicalProduct]
    print(f"  OK shipping cost only for physical: ${shippable[0].calculate_shipping_cost():.2f}")

    order = Order("ORD-2")
    for p in inventory:
        order.add_order_line(p, 1)           # Order accepts any Product
    assert round(order.calculate_total(), 2) == round(1200.00 + 49.99, 2)
    order.display_order()


def test_round_trip() -> None:
    section("Serialisation round trip")
    laptop = PhysicalProduct("P001", "Laptop", 1200.00, 15, make_supplier(), 2.2)
    clone = PhysicalProduct.from_dict(laptop.to_dict())
    assert clone.to_dict() == laptop.to_dict()
    print("  OK to_dict -> from_dict preserves PhysicalProduct")


if __name__ == "__main__":
    for t in (test_type_hints, test_composition, test_association_order_line_product,
              test_aggregation_product_supplier, test_inheritance, test_lsp,
              test_polymorphism, test_round_trip):
        t()
    print("\nAll checks passed.")
