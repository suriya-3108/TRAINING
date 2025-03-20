import time
import math

def is_prime(num):
    """Check if a number is prime."""
    if num < 2:
        return False
    for i in range(2, int(math.sqrt(num)) + 1):
        if num % i == 0:
            return False
    return True

def find_second_largest_prime(input_number):
    """Find the second largest prime number <= n."""
    primes = []
    for num in range(input_number, 1, -1):  # Start from n and go downwards
        if is_prime(num):
            primes.append(num)
            if len(primes) == 2:  # Stop once we find the second largest prime
                break
    return primes[1] if len(primes) >= 2 else None

def main():
    input_number = int(input("Enter a number (n): "))
    
    start_time = time.time()  # Start timing
    second_largest_prime = find_second_largest_prime(input_number)
    end_time = time.time()  # End timing
    
    if second_largest_prime:
        print(f"The second largest prime number <= {input_number} is: {second_largest_prime}")
    else:
        print(f"There is no second largest prime number <= {input_number}.")
    
    time_taken = end_time - start_time
    print(f"Time taken: {time_taken:.6f} seconds")

if __name__ == "__main__":
    main()