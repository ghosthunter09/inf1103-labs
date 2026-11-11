import json
from supplier import Supplier
from product import Product
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from order import Order
from inventory import Inventory
from can_be_shipped import CanBeShipped

PRODUCT_TYPES = {
    PhysicalProduct.PRODUCT_TYPE: PhysicalProduct,
    DigitalProduct.PRODUCT_TYPE: DigitalProduct,
}


def product_from_dict(data: dict) -> Product:
    product_class = PRODUCT_TYPES.get(data.get("type"))
    if product_class is None:
        raise ValueError(f"Unknown product type: {data.get('type')!r}")
    return product_class.from_dict(data)


def load_inventory(filename: str = "inventory.json") -> Inventory:
    inventory = Inventory()
    try:
        with open(filename, "r") as f:
            data = json.load(f)
        for item_data in data:
            try:
                inventory.add_product(product_from_dict(item_data))
            except (KeyError, ValueError) as error:
                print(f"Skipping invalid product entry ({error}).")
    except FileNotFoundError:
        print("No previous inventory found. Starting with empty inventory.")
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
    price = float(input("Price: "))
    stock = int(input("Stock Quantity: "))

    if type_choice == "1":
        weight = float(input("Weight (kg): "))
        return PhysicalProduct(product_id, name, price, stock, default_supplier, weight)

    download_size = float(input("Download Size (MB): "))
    return DigitalProduct(product_id, name, price, stock, default_supplier, download_size)


def show_menu() -> None:
    print("\n---------- MENU ----------")
    print("1. Display All Products (Polymorphic)")
    print("2. Add Product")
    print("3. Update Stock")
    print("4. Find Product")
    print("5. Test Order (Composition Demo)")
    print("6. Save Inventory")
    print("7. Exit")
    print("--------------------------")


def main() -> None:
    filename = "inventory.json"
    inventory = load_inventory(filename)

    default_supplier = Supplier("S01", "Global Logistics Co.", "support@globallogistics.com")

    # Seed baseline products if not present
    if not inventory.find_product("P001"):
        inventory.add_product(PhysicalProduct("P001", "Laptop", 1200.00, 15, default_supplier, 2.2))
    if not inventory.find_product("P002"):
        inventory.add_product(PhysicalProduct("P002", "Mouse", 25.50, 40, default_supplier, 0.1))
    if not inventory.find_product("P003"):
        inventory.add_product(DigitalProduct("P003", "Photo Editor", 49.99, 100, default_supplier, 350.0))

    print("=" * 45)
    print("INVENTORY MANAGEMENT SYSTEM (LAB 8)")
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
            except ValueError:
                print("\nInvalid input. Product not added.")

        elif choice == "3":
            product_id = input("Enter Product ID: ").strip()
            product = inventory.find_product(product_id)
            if product:
                try:
                    new_stock = int(input(f"Current Stock: {product.stock}\nNew Stock: "))
                    product.update_stock(new_stock)
                    print("Stock updated successfully!")
                except ValueError:
                    print("Invalid quantity entered.")
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
            # Composition demo
            order = Order("ORD-101")
            p1 = inventory.find_product("P001")
            p2 = inventory.find_product("P002")
            if p1:
                order.add_order_line(p1, 2)
            if p2:
                order.add_order_line(p2, 5)
            order.display_order()

        elif choice == "6":
            save_inventory(inventory, filename)
            print("Inventory saved to inventory.json.")

        elif choice == "7":
            print("Terminating program. Goodbye!")
            break


if __name__ == "__main__":
    main()