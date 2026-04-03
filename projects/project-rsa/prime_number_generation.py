import sys
from time import time
import random


# You will need to implement this function and change the return value.
def mod_exp(x: int, y: int, N: int) -> int:                                 # O(n^3)
    """
    x^y mod(N)
    """
    if y == 0:                  # 0(1)
        return 1                # 0(1)
    z = mod_exp(x, y//2, N)     # 0(n^3)
    if y%2 == 0:                # 0(1)
        return (z*z) % N        # 0(n^2)
    else:
        return (x*z*z) % N      # 0(n^2)

        
def fermat(N: int, k: int) -> bool:                                         # O(n^3)
    """
    Returns True if N is prime
    """
    for i in range(1, k + 1):           # O(1)
        a = random.randint(2, N-1)      # O(1)
        if mod_exp(a, N-1, N) != 1:     # O(n^3)
            return False                # O(1)
    return True                         # O(1)


def miller_rabin(N: int, k: int) -> bool:                                   # O(n^3)
    """
    Returns True if N is prime
    """
    for i in range(1, k+1):                 # O(1)
        a = random.randint(2, N-1)      # O(1)
        n = N-1                         # O(1)
        while n != 1:                   # O(1)
            result = mod_exp(a, n, N)   # O(n^3)
            if result == N-1:           # O(1)
                break
            elif result == 1:           # O(1)
                if n%2 != 0:            # O(1)
                    break
            elif result != 1:           # O(1)
                return False            # O(1)
            n = n//2                    # O()
    return True                             # O(1)


def generate_large_prime(n_bits: int) -> int:                               # O(n^3)
    """Generate a random prime number with the specified bit length"""
    while (1):
        prime = random.getrandbits(n_bits)  # unsure
        if fermat(prime, 20):               # O(n^3)
            return prime                    # O(1)
        
    #return 4  # https://xkcd.com/221/


def main(n_bits: int):
    start = time()
    large_prime = generate_large_prime(n_bits)
    print(large_prime)
    print(f'Generation took {time() - start} seconds')


if __name__ == '__main__':
    main(int(sys.argv[1]))
