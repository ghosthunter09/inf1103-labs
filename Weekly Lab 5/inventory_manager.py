import json

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
    """Saves inventory data to inventory.json."""
    with open(filename, "w") as f:
        json.dump(inventory, f, indent=4)

def display_all(inventory):
    print("\nCurrent Inventory")
    print("-" * 40)
    for item in inventory.values():
        print(f"ID: {item['id']} | Name: {item['name']} | Price: ${item['price']:.2f} | Stock: {item['stock']}")
    print("-" * 40)

def add_product(inventory):
    print("\nAdd New Product")
    product_id = input("Product ID: ").strip()
    name = input("Product Name: ").strip()
    price = float(input("Price: "))
    stock = int(input("Stock Quantity: "))
    
    inventory[product_id] = {
        "id": product_id,
        "name": name,
        "price": price,
        "stock": stock
    }
    print("\nProduct added successfully!")

def update_stock(inventory):
    print("\nUpdate Stock")
    product_id = input("Enter Product ID: ").strip()
    if product_id in inventory:
        item = inventory[product_id]
        print("\nProduct Found:")
        print(f"Name: {item['name']}")
        print(f"Current Stock: {item['stock']}")
        
        new_stock = int(input("\nNew Stock Quantity: "))
        item['stock'] = new_stock
        print("\nStock updated successfully!")
    else:
        print("\nProduct not found.")

def search_product(inventory):
    print("\nSearch Product")
    product_id = input("Enter Product ID: ").strip()
    if product_id in inventory:
        item = inventory[product_id]
        print("\nProduct Found")
        print("-" * 40)
        print(f"ID: {item['id']}")
        print(f"Name: {item['name']}")
        print(f"Price: ${item['price']:.2f}")
        print(f"Stock: {item['stock']}")
        print("-" * 40)
    else:
        print("\nProduct not found.")

def show_menu():
    print("\n---------- MENU ----------")
    print("1. Display All Products")
    print("2. Add Product")
    print("3. Update Stock")
    print("4. Search Product")
    print("5. Save Inventory")
    print("6. Exit")
    print("--------------------------")

filename = "inventory.json"
    
print("=" * 45)
print("INVENTORY MANAGEMENT SYSTEM")
print("=" * 45)
    
inventory = load_inventory(filename)

show_menu()

while True:
    choice = input("\nEnter option: ").strip()
        
    if choice == "1":
        display_all(inventory)
    elif choice == "2":
        add_product(inventory)
    elif choice == "3":
        update_stock(inventory)
    elif choice == "4":
        search_product(inventory)
    elif choice == "5":
        print("\nSaving inventory...")
        save_inventory(inventory, filename)
        print("Inventory saved successfully to inventory.json.")
    elif choice == "6":
        print("\nSaving inventory before exit...")
        save_inventory(inventory, filename)
        print("Inventory saved successfully.")
        print("\nThank you for using Inventory Management System.")
        print("Program terminated.")
        break