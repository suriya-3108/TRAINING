def is_prime(num):
    """Check if a number is prime."""
    if num < 2:
        return False
    for i in range(2, int(num**0.5) + 1):
        if num % i == 0:
            return False
    return True

def largest_prime(input_number):
    """Find the largest prime number less than or equal to n."""
    for i in range(input_number, 1, -1):
        if is_prime(i):
            return i
    return None

# Input
input_number = int(input("Enter a number: "))

# Get the largest prime number
result = largest_prime(input_number)

# Output
if result:
    print(f"The largest prime number less than or equal to {input_number} is: {result}")
else:
    print(f"There is no prime number less than or equal to {input_number}.")