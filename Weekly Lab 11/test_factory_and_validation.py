import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from supplier import Supplier
from product import Product
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from order_line import OrderLine
from product_factory import ProductFactory

SUPPLIER = Supplier("S1", "Sup", "s@x.com")


class TestFactory(unittest.TestCase):
    def test_creates_physical(self):
        p = ProductFactory.create("physical", "P1", "Lamp", 25, 10, SUPPLIER, weight=1.5)
        self.assertIsInstance(p, PhysicalProduct)
        self.assertIsInstance(p, Product)
        self.assertEqual(p.weight, 1.5)

    def test_creates_digital(self):
        p = ProductFactory.create("digital", "D1", "App", 49.9, 100, SUPPLIER, download_size=20)
        self.assertIsInstance(p, DigitalProduct)
        self.assertEqual(p.download_size, 20)

    def test_type_is_case_insensitive(self):
        self.assertIsInstance(ProductFactory.create("PHYSICAL", "P1", "x", 1, 1, SUPPLIER), PhysicalProduct)

    def test_unknown_type_raises_clear_error(self):
        with self.assertRaises(ValueError) as ctx:
            ProductFactory.create("service", "S1", "Install", 30, 5, SUPPLIER)
        self.assertIn("Unknown product type: service", str(ctx.exception))

    def test_from_dict_round_trip_and_unknown(self):
        p = ProductFactory.create("physical", "P1", "Lamp", 25, 10, SUPPLIER, weight=1.5)
        self.assertEqual(ProductFactory.from_dict(p.to_dict()).to_dict(), p.to_dict())
        with self.assertRaises(ValueError):
            ProductFactory.from_dict({"type": "service"})


class TestValidation(unittest.TestCase):
    def test_price_must_be_positive(self):
        for bad in (0, -1, -0.01):
            with self.assertRaises(ValueError):
                ProductFactory.create("physical", "P1", "x", bad, 1, SUPPLIER)
            with self.assertRaises(ValueError):
                ProductFactory.create("digital", "D1", "x", bad, 1, SUPPLIER)

    def test_initial_stock_cannot_be_negative(self):
        with self.assertRaises(ValueError):
            ProductFactory.create("physical", "P1", "x", 5, -1, SUPPLIER)
        ProductFactory.create("physical", "P1", "x", 5, 0, SUPPLIER)   # zero is allowed

    def test_update_stock_rejects_negative_for_all_subtypes(self):
        for kind in ("physical", "digital"):
            p = ProductFactory.create(kind, "X", "x", 5, 3, SUPPLIER)
            with self.assertRaises(ValueError):
                p.update_stock(-1)
            self.assertEqual(p.stock, 3)          # unchanged

    def test_order_line_quantity_must_be_positive(self):
        p = ProductFactory.create("physical", "P1", "x", 5, 3, SUPPLIER)
        for bad in (0, -2):
            with self.assertRaises(ValueError):
                OrderLine(p, bad)
        self.assertEqual(OrderLine(p, 1).quantity, 1)


if __name__ == "__main__":
    unittest.main()
