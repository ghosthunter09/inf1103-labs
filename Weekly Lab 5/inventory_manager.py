import json

# Required functions (keeping exact function names)
def display_all(inventory):
    print("\nCurrent Inventory")
    print("-" * 40)
    for item in inventory.values():
        print(f"ID: {item['id']} | Name: {item['name']} | Price: ${item['price']:.2f} | Stock: {item['stock']}")
    print("-" * 40)

def add_product(inventory):
    print("\nAdd New Product")
    product_id = input("Product ID: ")
    name = input("Product Name: ")
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
    product_id = input("Enter Product ID: ")
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
    product_id = input("Enter Product ID: ")
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


    # Initial inventory dictionary with at least 3 items
inventory = {
    "P001": {"id": "P001", "name": "Laptop", "price": 1200.00, "stock": 15},
    "P002": {"id": "P002", "name": "Mouse", "price": 25.50, "stock": 40},
    "P003": {"id": "P003", "name": "Keyboard", "price": 45.00, "stock": 25}
}
    
display_all(inventory)