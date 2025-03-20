# Ask the user for the filename
file_path = input("Enter the file name (e.g., example.txt): ")

# Ask the user for the word to find and the replacement word
word_to_find = input("Enter the word to find: ")
replacement_word = input("Enter the word to replace it with: ")

# Open the file and read its content
with open(file_path, "r") as file:
    content = file.read()  # Read the entire file content

# Replace the word in the content
modified_content = content.replace(word_to_find, replacement_word)

# Write the modified content back to the file
with open(file_path, "w") as file:
    file.write(modified_content)

print(f"All occurrences of '{word_to_find}' have been replaced with '{replacement_word}' in '{file_path}'.")
