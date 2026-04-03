import json
import os
import sys
from pathlib import Path
from time import time

this_folder = os.path.dirname(__file__)
sys.path.append(os.path.join(this_folder, ".."))

from encrypt_decrypt_files import process as encrypt_decrypt

from utils import compute_average_runtimes, print_markdown_table


def main():
    keypairs_file = Path(__file__).parent / "_keypairs.json"        # changed to work in devcontainer
    with open(keypairs_file, "r") as file:
        keypairs = json.load(file)

    encrypted_runtimes = []
    decrypted_runtimes = []

    try:
        for keypair in keypairs:
            size, N, e, d = keypair
            n_bytes = (N.bit_length() + 7) // 8
            plain_bytes = (N.bit_length() - 1) // 8  # ensure m < N

            print(f'Running encryption and decryption for {size} bytes')

            message_file = Path(__file__).parent / "1Nephi.txt"             # changed to work in devcontainer
            message = message_file.read_bytes()

            # Encrypt
            start = time()
            encrypted = encrypt_decrypt(n_bytes, plain_bytes, N, e, message)
            runtime = time() - start

            encrypted_runtimes.append((size, runtime))

            # Decrypt
            start = time()
            decrypted = encrypt_decrypt(n_bytes, plain_bytes, N, d, encrypted)
            runtime = time() - start

            decrypted_runtimes.append((size, runtime))

            if decrypted != message:
                print("WARNING: decrypted message was not equal to original message")

    except KeyboardInterrupt:
        print("Cancelling")

    enc_ave_runtimes = compute_average_runtimes(encrypted_runtimes)
    dec_ave_runtimes = compute_average_runtimes(decrypted_runtimes)

    print()

    print('**Encryption**')
    print_markdown_table(enc_ave_runtimes, ["Size ", "Time (sec)"])

    runtimes_file = Path(__file__).parent / '_encryption_runtimes.json'
    runtimes_file.write_text(json.dumps(encrypted_runtimes, indent=4))
    print()
    print(runtimes_file.name, "written")

    print('**Decryption**')
    print_markdown_table(dec_ave_runtimes, ["Size ", "Time (sec)"])

    runtimes_file = Path(__file__).parent / '_decryption_runtimes.json'
    runtimes_file.write_text(json.dumps(decrypted_runtimes, indent=4))
    print()
    print(runtimes_file.name, "written")


if __name__ == "__main__":
    sys.setrecursionlimit(2048 * 2)

    main()
