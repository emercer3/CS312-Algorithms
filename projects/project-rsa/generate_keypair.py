import sys
from time import time
from prime_number_generation import generate_large_prime

# When trying to find a relatively prime e for (p-1) * (q-1)
# use this list of 25 primes
# If none of these work, throw an exception (and let the instructors know!)
primes = [
    2,
    3,
    5,
    7,
    11,
    13,
    17,
    19,
    23,
    29,
    31,
    37,
    41,
    43,
    47,
    53,
    59,
    61,
    67,
    71,
    73,
    79,
    83,
    89,
    97,
]


def euclid(a: int, b: int):             # O(n)
    if b == 0:
        return a
    return euclid(b, a%b)   # O(n)


def extended_euclids(a: int, b: int) -> tuple[int, int ,int]: # O(n^2)
    """
    this takes to numbers and finds the GCD
    """
    if b == 0:
        return (1, 0, a)                    # O(1)
    x, y, z = extended_euclids(b, a%b)    
    return (y, (x-(a//b)*y), z)             # O(n^2)


def generate_key_pairs(n_bits) -> tuple[int, int, int]:             # O(n^3)
    """
    Generate RSA public and private key pairs.
    Randomly creates a p and q (two large n-bit primes)
    Computes N = p*q
    Computes e and d such that e*d = 1 mod (p-1)(q-1)
    Return N, e, and d
    """
    p = generate_large_prime(n_bits)                    # O(n^3)
    q = generate_large_prime(n_bits)                    # O(n^3)

    N = p*q                                             # O(n^2)

    for e in primes:
        x, d, z = extended_euclids(((p-1)*(q-1)), e)    # O(n^2)
        if z == 1:
            d = d%((p-1)*(q-1))                         # O(n^2)
            return (N, e, d)                            # O(1)



def main(n_bits: int, filename_stem: str):
    start = time()
    N, e, d = generate_key_pairs(n_bits)
    print(f'{time() - start} seconds elapsed')

    public_file = filename_stem + '.public.txt'
    with open(public_file, 'w') as file:
        file.writelines([
            str(N),
            '\n',
            str(e)
        ])
    print(public_file, 'written')

    private_file = filename_stem + '.private.txt'
    with open(private_file, 'w') as file:
        file.writelines([
            str(N),
            '\n',
            str(d)
        ])
    print(private_file, 'written')


if __name__ == '__main__':
    main(int(sys.argv[1]), sys.argv[2])
