def get_valid_input():
    while True:
        user_input = input("Enter stock quantity (or type 'quit' to exit): ")
        if user_input.lower() == 'quit':
            return 'quit'
        if user_input.isdigit():
            return int(user_input)
        print("Error: Invalid input. Please enter a positive whole number.")
        return None

def process_delivery(current_total, new_value):
    return current_total + new_value

def calculate_tax(amount):
    return amount * 0.10

def generate_report(total_units, failed_attempts):
    print("\n--- Summary Report ---")
    print(f"Total Deliveries Processed: {total_units}")
    print(f"Number of Failed/Rejected Entries: {failed_attempts}")


total_inventory = 0
failed_entries = 0

while True:
    val = get_valid_input()
    if val == 'quit':
            break
    elif val is None:
        failed_entries += 1
    else:
        total_inventory = process_delivery(total_inventory, val)
        tax = calculate_tax(val)
        print(f"Added {val} units (Tax: {tax:.2f}). Current total: {total_inventory}")

generate_report(total_inventory, failed_entries)