#Prompt the user for input
user_input = input("enter the text: ")

#Prompt the user for the file name
file_name = input("Enter the name of the file (e.g., myfile.txt): ")

#Open the file in write mode
with open(file_name, "w") as file:
    file.write(user_input + "\n")

print(f"Text has been written to {file_name}")
