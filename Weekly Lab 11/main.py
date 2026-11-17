import json
from supplier import Supplier
from product import Product
from order import Order
from Inventory import Inventory
from can_be_shipped import CanBeShipped
from product_factory import ProductFactory
from product_loader import load_products
from input_helpers import get_positive_float, get_non_negative_int
from discount_strategy import (DiscountStrategy, NoDiscount, PercentageDiscount,
                               BulkDiscount, StudentDiscount)


def load_inventory(filename: str = "inventory.json") -> Inventory:
    inventory = Inventory()
    try:
        with open(filename, "r") as f:
            data = json.load(f)
        for item_data in data:
            try:
                inventory.add_product(ProductFactory.from_dict(item_data))
            except (KeyError, ValueError) as error:  # missing field, unknown type or broken rule
                print(f"Skipping invalid product entry ({error}).")
    except FileNotFoundError:
        print("No previous inventory found. Starting with empty inventory.")
    except json.JSONDecodeError:
        print("Saved inventory file is corrupted. Starting with empty inventory.")
    return inventory


def save_inventory(inventory: Inventory, filename: str = "inventory.json") -> None:
    data_to_save = [product.to_dict() for product in inventory.products]
    with open(filename, "w") as f:
        json.dump(data_to_save, f, indent=4)


def show_product_details(product: Product) -> None:
    """LSP substitutability test function."""
    product.display_information()
    print(f"Fulfilment: {product.get_fulfilment_info()}")


def prompt_new_product(default_supplier: Supplier) -> Product | None:
    print("\nProduct Type")
    print("1. Physical Product")
    print("2. Digital Product")
    type_choice = input("Choose type: ").strip()

    if type_choice not in ("1", "2"):
        print("\nInvalid product type.")
        return None

    product_id = input("Product ID: ").strip()
    name = input("Product Name: ").strip()
    price = get_positive_float("Price: ")
    stock = get_non_negative_int("Stock Quantity: ")

    # Product creation goes through the factory; main.py never names a concrete class.
    if type_choice == "1":
        weight = get_positive_float("Weight (kg): ")
        return ProductFactory.create("physical", product_id, name, price, stock,
                                     default_supplier, weight=weight)

    download_size = get_positive_float("Download Size (MB): ")
    return ProductFactory.create("digital", product_id, name, price, stock,
                                 default_supplier, download_size=download_size)


def choose_discount() -> DiscountStrategy:
    """Let the user pick a discount strategy for a custom order."""
    print("\nDiscount: 1. None  2. 10% off  3. 20 off totals of 200+  4. Student (5%)")
    choice = input("Choose discount (default 1): ").strip()
    strategies = {
        "2": PercentageDiscount(10),
        "3": BulkDiscount(200, 20),
        "4": StudentDiscount(),
    }
    return strategies.get(choice, NoDiscount())


def show_menu() -> None:
    print("\n---------- MENU ----------")
    print("1. Display All Products (Polymorphic)")
    print("2. Add Product")
    print("3. Update Stock")
    print("4. Find Product")
    print("5. Test Order (Composition Demo)")
    print("6. Save Inventory")
    print("7. Load Products from CSV")
    print("8. Exit")
    print("--------------------------")


def main() -> None:
    filename = "inventory.json"
    inventory = load_inventory(filename)

    default_supplier = Supplier("S01", "Global Logistics Co.", "support@globallogistics.com")

    # Seed baseline products if not present
    if not inventory.find_product("P001"):
        inventory.add_product(ProductFactory.create("physical", "P001", "Laptop", 1200.00, 15, default_supplier, weight=2.2))
    if not inventory.find_product("P002"):
        inventory.add_product(ProductFactory.create("physical", "P002", "Mouse", 25.50, 40, default_supplier, weight=0.1))
    if not inventory.find_product("P003"):
        inventory.add_product(ProductFactory.create("digital", "P003", "Photo Editor", 49.99, 100, default_supplier, download_size=350.0))

    print("=" * 45)
    print("INVENTORY MANAGEMENT SYSTEM (LAB 9)")
    print("=" * 45)

    while True:
        show_menu()
        choice = input("\nEnter option: ").strip()

        if choice == "1":
            inventory.display_all_products()

        elif choice == "2":
            try:
                new_product = prompt_new_product(default_supplier)
                if new_product:
                    inventory.add_product(new_product)
                    print("\nProduct added successfully!")
            except ValueError as error:
                print(f"\nInvalid input ({error}). Product not added.")

        elif choice == "3":
            product_id = input("Enter Product ID: ").strip()
            product = inventory.find_product(product_id)
            if product:
                try:
                    new_stock = int(input(f"Current Stock: {product.stock}\nNew Stock: "))
                    product.update_stock(new_stock)
                    print("Stock updated successfully!")
                except ValueError as error:
                    # int() failure or Product's own validation (negative stock)
                    print(f"Invalid quantity: {error}")
            else:
                print("Product not found.")

        elif choice == "4":
            product_id = input("Enter Product ID: ").strip()
            product = inventory.find_product(product_id)
            if product:
                print("\nProduct Found:")
                show_product_details(product)
                if isinstance(product, CanBeShipped):
                    print(f"Shipping Cost: ${product.calculate_shipping_cost():.2f}")
            else:
                print("Product not found.")

        elif choice == "5":
            print("\n" + "=" * 45)
            print("ORDER MANAGEMENT (COMPOSITION DEMO)")
            print("=" * 45)

            if not inventory.products:
                print("Inventory is currently empty. Please load or add products first.")
                continue

            print("1. Run Standard ORD-101 Demo (uses loaded inventory)")
            print("2. Create a New Custom Order")
            order_choice = input("Select an option (1-2): ").strip()

            if order_choice == "1":
                order_101 = Order("ORD-101", BulkDiscount(200, 20))   # strategy given at creation
                order_102 = Order("ORD-102")

                selected_products = inventory.products[:3]
                quantities = [2, 5, 3]

                for product, qty in zip(selected_products, quantities):
                    order_101.add_order_line(product, qty)

                # Add the same first product to a second order
                shared_product = selected_products[0]
                order_102.add_order_line(shared_product, 1)

                print("\n[ORD-101 Created]")
                order_101.display_order()

                print("\n[ORD-102 Created with Same Product]")
                order_102.display_order()

                # Verify distinct OrderLine objects sharing the same Product object
                line1 = order_101.order_lines[0]
                line2 = order_102.order_lines[0]
                print(f"\nSeparate OrderLine objects? {line1 is not line2}")
                print(f"Same Product object?        {line1.product is line2.product}")

                # Remove an order line through Order method
                order_101.remove_order_line(shared_product.product_id)
                print(f"\n[ORD-101 After Removing {shared_product.name}]")
                order_101.display_order()

            elif order_choice == "2":
                # --- Create a Brand-New Order from Inventory ---
                new_order_id = input("\nEnter New Order ID: ").strip()
                if not new_order_id:
                    new_order_id = "ORD-NEW"

                custom_order = Order(new_order_id, choose_discount())

                while True:
                    print("\nAvailable Products in Saved Inventory:")
                    for p in inventory.products:
                        print(f"  [{p.product_id}] {p.name} - ${p.price:.2f} (Stock: {p.stock})")

                    prod_id = input("\nEnter Product ID to add (or type 'done' to finish): ").strip()
                    if prod_id.lower() == "done":
                        break

                    # Retrieve reference from inventory (Aggregation)
                    product = inventory.find_product(prod_id)
                    if not product:
                        print("Product ID not found in inventory. Please choose an ID from the list.")
                        continue

                    try:
                        qty = int(input(f"Enter quantity for '{product.name}': "))
                        if qty <= 0:
                            print("Quantity must be greater than 0.")
                            continue
                    except ValueError:
                        print("Invalid input. Please enter a whole number.")
                        continue

                    # Order creates and manages its own OrderLine internally (Composition)
                    custom_order.add_order_line(product, qty)
                    print(f"Added {qty} x {product.name} to {custom_order.order_id}.")

                if custom_order.order_lines:
                    print(f"\n[{custom_order.order_id} Summary]")
                    custom_order.display_order()
                else:
                    print("\nNo items were added to the order.")

            else:
                print("Invalid choice. Returning to main menu.")

        elif choice == "6":
            save_inventory(inventory, filename)
            print("Inventory saved to inventory.json.")

        elif choice == "7":
            path = input("CSV file path (default products.csv): ").strip() or "products.csv"
            load_products(path, inventory, default_supplier)

        elif choice == "8":
            print("Terminating program. Goodbye!")
            break

        else:
            print("Invalid option. Please choose 1-8.")


if __name__ == "__main__":
    main()