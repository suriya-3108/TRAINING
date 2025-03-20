def is_prime(num):
    """Check if a number is prime."""
    if num <= 1:
        return False
    if num == 2:
        return True
    if num % 2 == 0:
        return False
    for i in range(3, int(num**0.5) + 1, 2):
        if num % i == 0:
            return False
    return True

def print_primes(input_number):
    """Print all prime numbers up to n."""
    for num in range(2, input_number + 1):
        if is_prime(num):
            print(num, end=" ")

# Input
input_number= int(input("Enter a number : "))

# Output
print(f"Prime numbers up to { input_number } are:")
print_primes(input_number)