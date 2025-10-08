#!/usr/bin/env python3
"""
Random Numbers Analysis Script
This script generates random numbers, sorts them manually, and calculates averages for even and odd numbers.
Author: Data Quality Engineer
Date: October 8, 2025
"""

# Import the random module to generate random numbers
import random

def bubble_sort(numbers):
    """
    Manually sort a list of numbers using bubble sort algorithm (without using built-in sort())
    
    Args:
        numbers (list): List of numbers to be sorted
    
    Returns:
        list: Sorted list in ascending order
    """
    # Create a copy of the list to avoid modifying the original
    sorted_numbers = numbers.copy()
    
    # Get the length of the list for iteration
    n = len(sorted_numbers)
    
    # Outer loop for number of passes
    for i in range(n):
        # Inner loop for comparing adjacent elements
        for j in range(0, n - i - 1):
            # Compare adjacent elements and swap if they're in wrong order
            if sorted_numbers[j] > sorted_numbers[j + 1]:
                # Swap elements using tuple unpacking
                sorted_numbers[j], sorted_numbers[j + 1] = sorted_numbers[j + 1], sorted_numbers[j]
    
    return sorted_numbers

def calculate_even_odd_averages(numbers):
    """
    Calculate separate averages for even and odd numbers in the list
    
    Args:
        numbers (list): List of numbers to analyze
    
    Returns:
        tuple: (even_average, odd_average)
    """
    # Initialize lists to store even and odd numbers separately
    even_numbers = []
    odd_numbers = []
    
    # Iterate through all numbers and categorize them as even or odd
    for number in numbers:
        # Check if number is even (divisible by 2 with no remainder)
        if number % 2 == 0:
            even_numbers.append(number)
        else:
            # If not even, then it's odd
            odd_numbers.append(number)
    
    # Calculate average for even numbers if any exist
    if len(even_numbers) > 0:
        even_average = sum(even_numbers) / len(even_numbers)
    else:
        even_average = 0  # Default to 0 if no even numbers found
    
    # Calculate average for odd numbers if any exist
    if len(odd_numbers) > 0:
        odd_average = sum(odd_numbers) / len(odd_numbers)
    else:
        odd_average = 0  # Default to 0 if no odd numbers found
    
    return even_average, odd_average

def main():
    """
    Main function that orchestrates the entire process
    """
    # Print header for the program
    print("=" * 60)
    print("Random Numbers Analysis Program")
    print("=" * 60)
    
    # Set seed for reproducible results (optional, can be removed for true randomness)
    random.seed(42)
    
    # Generate a list of 100 random numbers between 0 and 1000 (inclusive)
    print("Generating 100 random numbers between 0 and 1000...")
    random_numbers = []
    
    # Loop to generate 100 random numbers
    for i in range(100):
        # Generate random integer between 0 and 1000 (inclusive)
        random_number = random.randint(0, 1000)
        random_numbers.append(random_number)
    
    # Display the first 10 numbers as a sample
    print(f"Sample of generated numbers (first 10): {random_numbers[:10]}")
    print(f"Total numbers generated: {len(random_numbers)}")
    print()
    
    # Sort the list manually using bubble sort (without using built-in sort())
    print("Sorting numbers manually using bubble sort algorithm...")
    sorted_numbers = bubble_sort(random_numbers)
    
    # Display the first 10 and last 10 sorted numbers
    print(f"Sorted numbers (first 10): {sorted_numbers[:10]}")
    print(f"Sorted numbers (last 10): {sorted_numbers[-10:]}")
    print()
    
    # Calculate averages for even and odd numbers
    print("Calculating averages for even and odd numbers...")
    even_avg, odd_avg = calculate_even_odd_averages(sorted_numbers)
    
    # Count even and odd numbers for additional information
    even_count = sum(1 for num in sorted_numbers if num % 2 == 0)
    odd_count = sum(1 for num in sorted_numbers if num % 2 == 1)
    
    # Print the results in a formatted manner
    print("=" * 60)
    print("ANALYSIS RESULTS")
    print("=" * 60)
    print(f"Total numbers analyzed: {len(sorted_numbers)}")
    print(f"Range: {min(sorted_numbers)} to {max(sorted_numbers)}")
    print()
    print(f"Even numbers count: {even_count}")
    print(f"Average of even numbers: {even_avg:.2f}")
    print()
    print(f"Odd numbers count: {odd_count}")
    print(f"Average of odd numbers: {odd_avg:.2f}")
    print()
    print(f"Overall average: {sum(sorted_numbers) / len(sorted_numbers):.2f}")
    print("=" * 60)

# Execute the main function only if this script is run directly (not imported)
if __name__ == "__main__":
    main()