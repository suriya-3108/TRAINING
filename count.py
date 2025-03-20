def count_words_in_file(filename):
    try:
        with open(filename, 'r') as file:
            text = file.read()
            words = text.split()
            word_count = len(words)
            return word_count
    except FileNotFoundError:
        print(f"The file '{filename}' was not found.")
        return None

# Get the file name from the user
filename = input("Enter the file name (including extension, if any): ")

# Count the words in the file
word_count = count_words_in_file(filename)

if word_count is not None:
    print(f"The file '{filename}' contains {word_count} words.")