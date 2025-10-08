import random
import string

def generate_random_dicts():
    """
    Generate a list of random dictionaries with letter keys and numeric values.
    
    Returns:
        list: List of dictionaries with random letter keys and values 0-100
    """
    # Generate random number of dictionaries between 2 and 10
    num_dicts = random.randint(2, 10)
    print(f"Generating {num_dicts} random dictionaries...")
    
    # Initialize empty list to store dictionaries
    dict_list = []
    
    # Create each dictionary
    for i in range(num_dicts):
        # Generate random number of keys for current dictionary (1 to 10 keys)
        num_keys = random.randint(1, 10)
        
        # Initialize empty dictionary for current iteration
        current_dict = {}
        
        # Generate random keys and values for current dictionary
        for _ in range(num_keys):
            # Select random lowercase letter as key
            key = random.choice(string.ascii_lowercase)
            # Generate random value between 0 and 100
            value = random.randint(0, 100)
            # Add key-value pair to current dictionary
            current_dict[key] = value
        
        # Add completed dictionary to the list
        dict_list.append(current_dict)
        print(f"Dict {i+1}: {current_dict}")
    
    return dict_list

def merge_dictionaries(dict_list):
    """
    Merge a list of dictionaries following specific rules:
    - For duplicate keys: take max value and rename key with dict number
    - For unique keys: keep as-is
    
    Args:
        dict_list (list): List of dictionaries to merge
        
    Returns:
        dict: Merged dictionary with renamed keys for conflicts
    """
    print("\nMerging dictionaries...")
    
    # Dictionary to track all key-value pairs and their source dict indices
    key_tracker = {}
    
    # Iterate through each dictionary with its index
    for dict_index, current_dict in enumerate(dict_list):
        # Process each key-value pair in current dictionary
        for key, value in current_dict.items():
            # Check if key already exists in tracker
            if key in key_tracker:
                # Key exists, compare values and update if current value is larger
                stored_value, stored_dict_index = key_tracker[key]
                if value > stored_value:
                    # Current value is larger, update tracker with new value and dict index
                    key_tracker[key] = (value, dict_index)
                    print(f"Key '{key}': Updated max value {value} from dict {dict_index + 1}")
                else:
                    print(f"Key '{key}': Keeping existing max value {stored_value} from dict {stored_dict_index + 1}")
            else:
                # Key doesn't exist, add it to tracker
                key_tracker[key] = (value, dict_index)
                print(f"Key '{key}': First occurrence with value {value} from dict {dict_index + 1}")
    
    # Create final merged dictionary
    merged_dict = {}
    
    # Process each key in the tracker
    for key, (value, dict_index) in key_tracker.items():
        # Count how many dictionaries contain this key
        key_count = sum(1 for d in dict_list if key in d)
        
        # If key appears in multiple dictionaries, rename it with dict number
        if key_count > 1:
            # Rename key with dict number (1-indexed for user readability)
            new_key = f"{key}_{dict_index + 1}"
            merged_dict[new_key] = value
            print(f"Renamed key '{key}' to '{new_key}' (conflict resolved)")
        else:
            # Key is unique, keep original name
            merged_dict[key] = value
            print(f"Key '{key}' kept as-is (unique)")
    
    return merged_dict

def main():
    """
    Main function to demonstrate the dictionary generation and merging process.
    """
    print("=== Dictionary Generator and Merger ===\n")
    
    # Step 1: Generate random list of dictionaries
    random_dicts = generate_random_dicts()
    
    # Display the generated dictionaries
    print(f"\nGenerated list of dictionaries:")
    print(random_dicts)
    
    # Step 2: Merge the dictionaries according to the specified rules
    result_dict = merge_dictionaries(random_dicts)
    
    # Display the final merged dictionary
    print(f"\nFinal merged dictionary:")
    print(result_dict)
    
    return random_dicts, result_dict

# Execute the main function when script is run directly
if __name__ == "__main__":
    # Set random seed for reproducible results during testing (optional)
    # random.seed(42)  # Uncomment for consistent results
    
    # Run the main program
    original_dicts, merged_result = main()