import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

import inspect

from supplier import Supplier
from physical_product import PhysicalProduct
from order import Order
import order as order_module
from discount_strategy import (DiscountStrategy, NoDiscount, PercentageDiscount,
                               BulkDiscount, StudentDiscount)


def make_order(order_id="O1", discount=None) -> Order:
    supplier = Supplier("S1", "Sup", "s@x.com")
    product = PhysicalProduct("P1", "Thing", 125.00, 10, supplier, 1.0)
    order = Order(order_id, discount) if discount else Order(order_id)
    order.add_order_line(product, 2)          # total = 250
    return order


class TestDiscounts(unittest.TestCase):
    def test_strategies_inherit_from_base(self):
        for cls in (NoDiscount, PercentageDiscount, BulkDiscount, StudentDiscount):
            self.assertTrue(issubclass(cls, DiscountStrategy))
        with self.assertRaises(TypeError):
            DiscountStrategy()                # abstract

    def test_default_is_no_discount(self):
        order = make_order()
        self.assertIsInstance(order.discount, NoDiscount)
        self.assertAlmostEqual(order.calculate_total(), 250)

    def test_each_strategy(self):
        self.assertEqual(NoDiscount().apply(250), 250)
        self.assertAlmostEqual(PercentageDiscount(10).apply(250), 225)
        self.assertEqual(BulkDiscount(200, 20).apply(250), 230)
        self.assertEqual(BulkDiscount(200, 20).apply(199), 199)   # below threshold
        self.assertEqual(BulkDiscount(200, 20).apply(200), 180)   # at threshold
        self.assertAlmostEqual(StudentDiscount().apply(100), 95)

    def test_order_uses_strategy_given_at_creation(self):
        self.assertEqual(make_order(discount=BulkDiscount(200, 20)).calculate_total(), 230)

    def test_set_discount_changes_existing_order(self):
        order = make_order(discount=BulkDiscount(200, 20))
        self.assertEqual(order.calculate_total(), 230)
        order.set_discount(PercentageDiscount(10))
        self.assertAlmostEqual(order.calculate_total(), 225)

    def test_new_strategy_needs_no_change_to_order(self):
        class HalfPrice(DiscountStrategy):    # defined here, Order has never heard of it
            def apply(self, total: float) -> float:
                return total / 2
        self.assertEqual(make_order(discount=HalfPrice()).calculate_total(), 125)

    def test_order_has_no_discount_if_elif_logic(self):
        source = inspect.getsource(order_module.Order.calculate_total)
        self.assertNotIn("elif", source)
        self.assertNotIn("if ", source)

    def test_orders_can_share_one_strategy(self):
        shared = PercentageDiscount(10)
        self.assertIs(make_order("A", shared).discount, make_order("B", shared).discount)

    def test_invalid_strategy_values_rejected(self):
        with self.assertRaises(ValueError):
            PercentageDiscount(150)
        with self.assertRaises(ValueError):
            BulkDiscount(-1, 20)


if __name__ == "__main__":
    unittest.main()
