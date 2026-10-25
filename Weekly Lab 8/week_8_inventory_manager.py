import json

class Product:
    """
    Represents an individual product in the inventory.
    Demonstrates encapsulation and Single Responsibility Principle (SRP).
    """
    def __init__(self, product_id, name, price, stock):
        self._product_id = str(product_id)
        self.name = str(name)
        self._price = float(price)
        self.stock = int(stock)

    @property
    def product_id(self):
        return self._product_id

    @property
    def price(self):
        return self._price
        
    def update_stock(self, new_stock):
        """Updates the stock quantity for this product."""
        if new_stock >= 0:
            self.stock = int(new_stock)
        else:
            print("Stock quantity cannot be negative.")

    def display_information(self):
        """Prints product information formatted."""
        print(f"ID: {self._product_id} | Name: {self.name} | Price: ${self._price:.2f} | Stock: {self.stock}")

    def to_dict(self):
        """Converts Product object into dictionary format for JSON saving."""
        return {
            "id": self._product_id,
            "name": self.name,
            "price": self._price,
            "stock": self.stock
        }

    @classmethod
    def from_dict(cls, data):
        """Creates a Product instance from dictionary data."""
        return cls(
            product_id=data["id"],
            name=data["name"],
            price=data["price"],
            stock=data["stock"]
        )


# --- File Persistence Helpers ---

def load_inventory(filename="inventory.json"):
    """Reads previously saved inventory from JSON file if it exists."""
    try:
        with open(filename, "r") as f:
            inventory = json.load(f)
            print("\ninventory.json found.")
            print("Inventory loaded successfully.")
            return inventory
    except FileNotFoundError:
        return {}

def save_inventory(inventory, filename="inventory.json"):
    """Saves inventory data from Inventory object to JSON file."""
    data_to_save = [product.to_dict() for product in inventory.products]
    with open(filename, "w") as f:
        json.dump(data_to_save, f, indent=4)


# --- UI and Main Flow ---

def show_menu():
    print("\n---------- MENU ----------")
    print("1. Display All Products")
    print("2. Add Product")
    print("3. Update Stock")
    print("4. Search Product")
    print("5. Save Inventory")
    print("6. Exit")
    print("--------------------------")


def main():
    filename = "inventory.json"

    inventory = load_inventory(filename)

    if not inventory.search_product("P001"):
        product1 = Product("P001", "Laptop", 1200.00, 15)
        inventory.add_product(product1)

    if not inventory.search_product("P002"):
        product2 = Product("P002", "Mouse", 25.50, 40)
        inventory.add_product(product2)
    
    print("=" * 45)
    print("INVENTORY MANAGEMENT SYSTEM")
    print("=" * 45)

    while True:
        show_menu()
        choice = input("\nEnter option: ").strip()
            
        if choice == "1":
            inventory.display_all()

        elif choice == "2":
            print("\nAdd New Product")
            product_id = input("Product ID: ").strip()
            name = input("Product Name: ").strip()
            price = float(input("Price: "))
            stock = int(input("Stock Quantity: "))
            
            # Create product object and add to inventory
            new_product = Product(product_id, name, price, stock)
            inventory.add_product(new_product)
            print("\nProduct added successfully!")

        elif choice == "3":
            print("\nUpdate Stock")
            product_id = input("Enter Product ID: ").strip()
            product = inventory.search_product(product_id)
            if product:
                print("\nProduct Found:")
                print(f"Name: {product.name}")
                print(f"Current Stock: {product.stock}")
                
                new_stock = int(input("\nNew Stock Quantity: "))
                product.update_stock(new_stock)
                print("\nStock updated successfully!")
            else:
                print("\nProduct not found.")

        elif choice == "4":
            print("\nSearch Product")
            product_id = input("Enter Product ID: ").strip()
            product = inventory.search_product(product_id)
            if product:
                print("\nProduct Found")
                print("-" * 40)
                product.display_information()
                print("-" * 40)
            else:
                print("\nProduct not found.")

        elif choice == "5":
            print("\nSaving inventory...")
            save_inventory(inventory, filename)
            print("Inventory saved successfully to inventory.json.")

        elif choice == "6":
            print("\nThank you for using Inventory Management System.")
            print("Program terminated.")
            break

if __name__ == "__main__":
    main()