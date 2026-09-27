def load_inventory(filename):
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

def save_inventory(inventory, filename):
    with open(filename, "w") as f:
        for item in inventory:
            f.write(f"{item['id']},{item['name']},{item['quantity']}\n")

def display_current_inventory(inventory):
    print("Current Orders:\n")
    if not inventory:
        print("No existing inventory found.\n")
    else:
        for item in inventory:
            print(f"{item['id']}, {item['name']}, {item['quantity']}")
        print()

def get_valid_input():
    while True:
        user_input = input("Enter a positive whole number: ")
        if user_input.isdigit():
            return int(user_input)
        print("Error: Invalid input. Please enter a positive whole number.")

filename="inventory.txt"
inventory = load_inventory(filename)
display_current_inventory(inventory)

while True:
    product_name = input("Enter Product Name: ")
    if product_name.lower() == 'quit':
        break
    quantity = get_valid_input()
    next_id = 1001 + len(inventory)
    new_inventory = {
        "id": str(next_id),
        "name": product_name,
        "quantity": quantity}
    inventory.append(new_inventory)
    print(f"\nNew Order Added:\n")
    print(f"{new_inventory['id']},{new_inventory['name']},{new_inventory['quantity']}\n")
    save_inventory(inventory, filename)
    print(f"Order successfully saved to orders.txt")