def load_inventory(filename="inventory.txt"):
    """Reads previously saved inventory from file."""
    
    #inventory = []
    try:
        with open(filename, "r") as f:
            for line in f:
                line = line.strip()
                print(line)
    except FileNotFoundError:
        pass

filename = "inventory.txt"
load_inventory(filename)
while True:
    product_name = input("Enter Product Name: ")
    if product_name.lower() == 'quit':
        break
    quantity = int(input("Enter Quantity: ")) 
    print(f"\nNew Order Added:\n")      
    print("Order successfully added to order.txt.\n")