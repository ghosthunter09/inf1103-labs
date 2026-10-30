import json
from abc import ABC, abstractmethod

class CanBeShipped(ABC):
    """
    Interface-style contract: any class that can be shipped must be able
    to calculate its shipping cost. No attributes or implementation here.
    """
 
    @abstractmethod
    def calculate_shipping_cost(self):
        """Return the cost of shipping this object."""
        pass

class Product(ABC):
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

    @abstractmethod
    def get_fulfilment_info(self):
        """Returns a message describing how this product is fulfilled."""
        pass

    def to_dict(self):
        """Converts Product object into dictionary format for JSON saving."""
        return {
            "id": self._product_id,
            "name": self.name,
            "price": self._price,
            "stock": self.stock
        }
    
class PhysicalProduct(Product, CanBeShipped):
    """
    A product that is stored and shipped.
    Inherits from Product (single class inheritance) and signs the
    CanBeShipped interface contract.
    """
    PRODUCT_TYPE = "physical"
    BASE_SHIPPING_FEE = 5.00   # flat fee in dollars
    RATE_PER_KG = 2.50         # dollars per kilogram
 
    def __init__(self, product_id, name, price, stock, weight):
        super().__init__(product_id, name, price, stock)
        self.weight = float(weight)  # kilograms
 
    def display_information(self):
        """Overrides Product.display_information, reusing the parent's output."""
        super().display_information()
        print(f" | Weight: {self.weight:.2f} kg")
 
    def get_fulfilment_info(self):
        return "This product requires physical shipping."
 
    def calculate_shipping_cost(self):
        """Simple rule: flat base fee plus a rate per kilogram."""
        return self.BASE_SHIPPING_FEE + self.RATE_PER_KG * self.weight
 
    def to_dict(self):
        data = super().to_dict()
        data["type"] = self.PRODUCT_TYPE
        data["weight"] = self.weight
        return data
 
    @classmethod
    def from_dict(cls, data):
        return cls(data["id"], data["name"], data["price"],
                   data["stock"], data["weight"])

class DigitalProduct(Product):
    """A product delivered digitally via download."""
    PRODUCT_TYPE = "digital"
 
    def __init__(self, product_id, name, price, stock, download_size):
        super().__init__(product_id, name, price, stock)
        self.download_size = float(download_size)  # megabytes
 
    def display_information(self):
        """Overrides Product.display_information, reusing the parent's output."""
        super().display_information()
        print(f" | Download Size: {self.download_size:.2f} MB")
 
    def get_fulfilment_info(self):
        return "This product is delivered digitally via download."
 
    def to_dict(self):
        data = super().to_dict()
        data["type"] = self.PRODUCT_TYPE
        data["download_size"] = self.download_size
        return data
 
    @classmethod
    def from_dict(cls, data):
        return cls(data["id"], data["name"], data["price"],
                   data["stock"], data["download_size"])

# Maps the saved "type" identifier to the class that rebuilds it.
# A new product type only needs one new entry here (OCP-friendly).
PRODUCT_TYPES = {
    PhysicalProduct.PRODUCT_TYPE: PhysicalProduct,
    DigitalProduct.PRODUCT_TYPE: DigitalProduct,
}
 
 
def product_from_dict(data):
    """Creates the correct Product subclass based on the saved 'type'."""
    product_class = PRODUCT_TYPES.get(data.get("type"))
    if product_class is None:
        raise ValueError(f"Unknown product type: {data.get('type')!r}")
    return product_class.from_dict(data)

class Inventory:
    """
    Manages a collection of Product objects stored in a list.
    Applies the Single Responsibility Principle (SRP).
    """
    def __init__(self):
        self.products = []  # Collection stored as a list

    def add_product(self, product):
        """Adds a Product instance to the inventory list."""
        self.products.append(product)

    def search_product(self, product_id):
        """Searches for a product by ID in the list and returns the Product object or None."""
        for product in self.products:
            # Check against the product's ID
            if product.product_id == str(product_id):
                return product
        return None

    def display_all(self):
        """Displays all products currently in the inventory list."""
        print("\nCurrent Inventory")
        print("-" * 40)
        if not self.products:
            print("No products currently in inventory.")
        else:
            for product in self.products:
                product.display_information()
        print("-" * 40)


# --- File Persistence Helpers ---

def load_inventory(filename="inventory.json"):
    """Reads saved inventory from JSON file and returns an Inventory object."""
    inventory = Inventory()
    try:
        with open(filename, "r") as f:
            data = json.load(f)
            for item_data in data:
                product = product_from_dict(item_data)
                inventory.add_product(product)
            print("\ninventory.json found.")
            print("Inventory loaded successfully.")
    except FileNotFoundError:
        print("\nNo previous inventory found. Starting with empty inventory.")
    return inventory


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
                print("-" * 70)
                product.display_information()
                print(f"Fulfilment: {product.get_fulfilment_info()}")
                if isinstance(product, CanBeShipped):
                    print(f"Shipping Cost: ${product.calculate_shipping_cost():.2f}")
                print("-" * 70)
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