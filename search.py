def search_text_in_file(filename, search_text):
    try:
        with open(filename, 'r') as file:
            found = False
            occurrences = []
            
            for line_number, line in enumerate(file, start=1):
                count = line.lower().count(search_text.lower())
                if count > 0:
                    found = True
                    occurrences.append((line_number, count))
            
            if found:
                print(f"Text '{search_text}' found in the file.")
                for line_number, count in occurrences:
                    print(f"Line {line_number}: {count} occurrence(s)")
            else:
                print(f"Text '{search_text}' not found in the file.")
    
    except FileNotFoundError:
        print(f"File '{filename}' not found.")

# Example usage
filename = input("Enter the filename: ")
search_text = input("Enter the text to search for: ")
search_text_in_file(filename, search_text)
