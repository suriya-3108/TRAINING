import os

def remove_empty_lines(file_path):
    # Edge Case 1: Check if the file exists
    if not os.path.exists(file_path):
        print(f"Error: The file '{file_path}' does not exist.")
        return  # Exit the function if the file is missing

    # Edge Case 2: Check if the file is empty
    if os.path.getsize(file_path) == 0:
        print(f"The file '{file_path}' is empty. No action taken.")
        return  # Exit the function if the file is empty

    # Read the file and store all lines
    with open(file_path, 'r') as file:
        original_lines = file.readlines()

    # Filter out empty lines
    non_empty_lines = [line for line in original_lines if line.strip()]

    # Edge Case 3: Check if the file already has no empty lines
    if len(original_lines) == len(non_empty_lines):
        print(f"The file '{file_path}' already has no empty lines. No action taken.")
        return  # Exit the function if no empty lines are found

    # Write the non-empty lines back to the file
    with open(file_path, 'w') as file:
        file.writelines(non_empty_lines)

    print(f"Empty lines removed from '{file_path}'.")

# Get the file path from the user
file_path = input("Enter the file name: ").strip()

# Call the function to remove empty lines
remove_empty_lines(file_path)