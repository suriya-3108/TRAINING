# Function to sort lines in a file and save to another file
def sort_file(input_file, output_file):
    try:
        # Read lines from the input file
        with open(input_file, 'r') as file:
            lines = file.readlines()

        # Sort the lines alphabetically
        lines.sort()

        # Write the sorted lines to the output file
        with open(output_file, 'w') as file:
            file.writelines(lines)

        print(f"File '{input_file}' has been sorted and saved to '{output_file}'.")
    except FileNotFoundError:
        print(f"Error: The file '{input_file}' does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Get file names from the user
input_file = input("Enter the input file name : ")
output_file = input("Enter the output file name : ")

# Calling the function 
sort_file(input_file, output_file)