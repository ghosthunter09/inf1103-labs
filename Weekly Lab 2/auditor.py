total_inventory = 0
failed_entries = 0

while True:
    user_input = input("Enter stock quantity (or type 'quit' to exit): ").strip()

    if user_input.lower() == 'quit':
        break

    elif not user_input.isdigit():
        print("Error: Invalid input. Please enter a positive whole number.")
        failed_entries += 1
        continue
    
    else:
        quantity = int(user_input)
        total_inventory += quantity
        print(f"Added {quantity} units. Current total: {total_inventory}")
        
    
        if total_inventory > 500:
            print("\nALERT: Overstock limit exceeded! Total inventory exceeds 500 units.")
            break

print("\n--- Summary Report ---")
print(f"Total Units Processed: {total_inventory}")
print(f"Number of Failed/Rejected Entries: {failed_entries}")