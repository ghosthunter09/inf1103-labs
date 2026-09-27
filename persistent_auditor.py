def load_inventory(filename="inventory.txt"):
    """Reads previously saved inventory from file."""
    inventory = []
    try:
        with open(filename, "r") as f:
            for line in f:
                line = line.strip()
                if line:
                    parts = line.split(",")
                    if len(parts) == 3:
                        inventory.append({
                            "id": parts[0].strip(),
                            "name": parts[1].strip(),
                            "quantity": int(parts[2].strip())
                        })
    except FileNotFoundError:
        pass
    return inventory

def display_current_inventory(inventory):
    """Displays current loaded inventory."""
    if not inventory:
        print("No existing inventory found.\n")
    else:
        for item in inventory:
            print(f"{item['id']}, {item['name']}, {item['quantity']}")
        print()

inventory = load_inventory()
display_current_inventory(inventory)
while True:
    product_name = input("Enter Product Name: ")
    if product_name.lower() == 'quit':
        break
    quantity = int(input("Enter Quantity: ")) 
    next_id = 1001 + len(inventory)
    new_inventory = {
        "id": str(next_id),
        "name": product_name,
        "quantity": quantity}
    inventory.append(new_inventory)
    print(f"\nNew Order Added:\n")
    print(f"{new_inventory['id']},{new_inventory['name']},{new_inventory['quantity']}\n")
    print("Order successfully added to order.txt.\n")