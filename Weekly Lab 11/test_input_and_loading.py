import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

import contextlib
import io
import tempfile
from unittest.mock import patch

from supplier import Supplier
from Inventory import Inventory
from input_helpers import get_positive_float
from product_loader import load_products

CSV_TEXT = """product_type,product_id,name,price,stock_quantity
physical,P001,Desk Lamp,25.00,10
digital,D001,Photo Editor,49.90,100
service,S001,Installation,30.00,5
physical,P002,Office Chair,abc,3
physical,P003,Monitor Stand,39.50,7
"""


def run_loader(path: str):
    inv = Inventory()
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        load_products(path, inv, Supplier("S1", "Sup", "s@x.com"))
    return inv, out.getvalue().splitlines()


class TestGetPositiveFloat(unittest.TestCase):
    def test_reasks_until_valid(self):
        out = io.StringIO()
        with patch("builtins.input", side_effect=["abc", "-5", "12.50"]), contextlib.redirect_stdout(out):
            result = get_positive_float("Price: ")
        self.assertEqual(result, 12.5)
        self.assertEqual(out.getvalue().splitlines(), [
            "Please enter a valid number, e.g. 12.50",
            "Please enter a number greater than zero.",
        ])

    def test_zero_rejected(self):
        with patch("builtins.input", side_effect=["0", "3"]), contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(get_positive_float(""), 3.0)


class TestLoadProducts(unittest.TestCase):
    def test_missing_file_handled(self):
        inv, lines = run_loader("definitely_missing_products.csv")
        self.assertEqual(lines, ["Products file not found: definitely_missing_products.csv",
                                 "Load attempt finished."])
        self.assertEqual(inv.products, [])

    def test_bad_rows_skipped_valid_rows_load(self):
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "products.csv")
            with open(path, "w", newline="") as f:
                f.write(CSV_TEXT)
            inv, lines = run_loader(path)
        self.assertEqual([p.product_id for p in inv.products], ["P001", "D001", "P003"])
        self.assertEqual(len(lines), 4)
        self.assertIn("Unknown product type: service", lines[0])
        self.assertIn("could not convert string to float", lines[1])
        self.assertEqual(lines[2:], ["3 products loaded.", "Load attempt finished."])

    def test_wrong_column_count_and_rule_violation_skipped(self):
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "p.csv")
            with open(path, "w", newline="") as f:
                f.write("h\nphysical,P1,Only,3\nphysical,P2,Neg,-5,1\nphysical,P3,Ok,5,1\n")
            inv, lines = run_loader(path)
        self.assertEqual([p.product_id for p in inv.products], ["P3"])
        self.assertIn("1 products loaded.", lines)


if __name__ == "__main__":
    unittest.main()
