import argparse
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.hazmat.primitives import padding
from getpass import getpass  # For securely handling passwords in interactive mode

# Function to derive a key from the provided password and salt using the Scrypt KDF
def derive_key(password: str, salt: bytes) -> bytes:
    try:
        kdf = Scrypt(salt=salt, length=32, n=2**14, r=8, p=1, backend=default_backend())
        return kdf.derive(password.encode())
    except Exception as e:
        raise ValueError(f"Error deriving key: {e}")

# Function to read file content
def read_file(file_path: str) -> bytes:
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Error: File '{file_path}' not found.")
    try:
        with open(file_path, 'rb') as file:
            return file.read()
    except Exception as e:
        raise IOError(f"Error reading file '{file_path}': {e}")

# Function to write data to file
def write_file(file_path: str, data: bytes):
    try:
        with open(file_path, 'wb') as file:
            file.write(data)
    except Exception as e:
        raise IOError(f"Error writing to file '{file_path}': {e}")

# Function to encrypt file
def encrypt_file(password: str, input_file: str, output_file: str):
    try:
        data = read_file(input_file)

        # Padding the data to match the block size of AES
        padder = padding.PKCS7(algorithms.AES.block_size).padder()
        padded_data = padder.update(data) + padder.finalize()

        # Generating a random salt and IV
        salt = os.urandom(16)
        iv = os.urandom(16)

        # Deriving the key
        key = derive_key(password, salt)

        # Initializing the AES cipher in CBC mode
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        encryptor = cipher.encryptor()

        # Encrypting the padded data
        encrypted_data = encryptor.update(padded_data) + encryptor.finalize()

        # Writing the salt, IV, and encrypted data to the output file
        write_file(output_file, salt + iv + encrypted_data)
        print(f"File successfully encrypted: {input_file} -> {output_file}")
    except Exception as e:
        print(f"Encryption error: {e}")

# Function to decrypt file
def decrypt_file(password: str, input_file: str, output_file: str):
    try:
        encrypted_data = read_file(input_file)

        # Extracting the salt, IV, and ciphertext
        salt = encrypted_data[:16]
        iv = encrypted_data[16:32]
        ciphertext = encrypted_data[32:]

        # Deriving the key using the same salt
        key = derive_key(password, salt)

        # Initializing the AES cipher in CBC mode
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()

        # Decrypting the ciphertext
        decrypted_padded_data = decryptor.update(ciphertext) + decryptor.finalize()

        # Unpadding the decrypted data
        unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
        decrypted_data = unpadder.update(decrypted_padded_data) + unpadder.finalize()

        # Writing the decrypted data to the output file
        write_file(output_file, decrypted_data)
        print(f"File successfully decrypted: {input_file} -> {output_file}")
    except Exception as e:
        print(f"Decryption error: {e}")

# Function to handle interactive mode when no arguments are provided
def interactive_mode():
    try:
        # Ask the user for the mode (encrypt or decrypt)
        mode = input("Select mode (encrypt/decrypt): ").strip().lower()
        if mode not in ['encrypt', 'decrypt']:
            raise ValueError("Invalid mode selected.")

        # Securely ask for the password using getpass for privacy
        password = getpass("Enter password: ")

        # Ask for the input and output file paths
        input_file = input("Enter input file path: ").strip()
        output_file = input("Enter output file path: ").strip()

        # Check if the input file exists
        if not os.path.exists(input_file):
            raise FileNotFoundError(f"Error: File '{input_file}' not found.")

        # Perform encryption or decryption based on the mode
        if mode == 'encrypt':
            encrypt_file(password, input_file, output_file)
        elif mode == 'decrypt':
            decrypt_file(password, input_file, output_file)
    except Exception as e:
        print(f"Interactive mode error: {e}")

# Main function to handle both CLI arguments and interactive mode
def main():
    parser = argparse.ArgumentParser(description='Encrypt and decrypt files using AES encryption.')
    
    # Optional CLI arguments for mode, password, input file, and output file
    parser.add_argument('mode', choices=['encrypt', 'decrypt'], nargs='?', help="Mode: 'encrypt' for encryption, 'decrypt' for decryption")
    parser.add_argument('password', nargs='?', help="Password for encryption or decryption")
    parser.add_argument('input_file', nargs='?', help="Path to the input file")
    parser.add_argument('output_file', nargs='?', help="Path to the output file")

    args = parser.parse_args()

    # If no arguments are provided, switch to interactive mode
    if not (args.mode and args.password and args.input_file and args.output_file):
        print("No arguments provided, switching to interactive mode.")
        interactive_mode()
    else:
        # Check if input file exists before proceeding
        if not os.path.exists(args.input_file):
            print(f"Error: File '{args.input_file}' not found.")
            return

        # Perform encryption or decryption based on the provided mode
        if args.mode == 'encrypt':
            encrypt_file(args.password, args.input_file, args.output_file)
        elif args.mode == 'decrypt':
            decrypt_file(args.password, args.input_file, args.output_file)

# Entry point for the script
if __name__ == "__main__":
    main()
