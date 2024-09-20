# AES File Encryption & Decryption Script

This Python script is used for encrypting and decrypting files using the **AES** algorithm with **CBC** (Cipher Block Chaining) mode. The script supports usage through the **CLI (Command Line Interface)** with arguments, or it can be run in **interactive mode**, where the user is prompted for inputs directly.

Untuk Instruksi Menggunakan Bahasa Indonesia, Klik [disini](README_ID.md).

## Features
- **File Encryption**: Encrypt files using AES and a key derived from a password.
- **File Decryption**: Decrypt files that were previously encrypted using this script.
- **CLI Mode**: Can be executed directly with arguments from the command line.
- **Interactive Mode**: If no arguments are provided, the script will prompt for user input interactively in the terminal.
- **Security**: Uses AES-256 encryption with **Scrypt** for secure key derivation and `getpass` for securely entering passwords (not shown on the terminal).

## Technologies and Libraries Used

- **Python**: Version 3.7 or newer
- **Cryptography Library**: Used for encryption and decryption.

  You can install it by running:
  
  ```bash
  pip install cryptography
  ```

## Prerequisites

Make sure Python version 3.7 or newer is installed on your system. If not, you can download and install Python from the [official Python website](https://www.python.org/downloads/).

## Installation

1. Clone the repository or download this script to your computer.
2. Install the dependencies by running the following command:

   ```bash
   pip install cryptography
   ```

## Usage

### 1. Using Arguments (CLI Mode)

You can use this script by providing arguments directly through the command line. Here is the format of the arguments:

- **Encrypt a File**:

  ```bash
  python encrypt-decrypt.py encrypt <password> <input_file> <output_file>
  ```

  Example:

  ```bash
  python encrypt-decrypt.py encrypt mypassword file_input.txt file_encrypted.enc
  ```

- **Decrypt a File**:

  ```bash
  python encrypt-decrypt.py decrypt <password> <input_file> <output_file>
  ```

  Example:

  ```bash
  python encrypt-decrypt.py decrypt mypassword file_encrypted.enc file_decrypted.txt
  ```

### 2. Without Arguments (Interactive Mode)

If you run the script without any arguments, it will enter interactive mode and prompt you to enter the required information, such as mode (encryption or decryption), password, input file, and output file.

- Run the script without arguments:

  ```bash
  python encrypt-decrypt.py
  ```

- You will be prompted to enter the following:
  - **Mode**: Choose `encrypt` or `decrypt`.
  - **Password**: Enter the password you want to use for encryption or decryption.
  - **Input File**: Path to the file you want to encrypt or decrypt.
  - **Output File**: Path to save the encrypted or decrypted file.

Example:

```
Select mode (encrypt/decrypt): encrypt
Enter password: ********
Enter input file path: file_input.txt
Enter output file path: file_encrypted.enc
File successfully encrypted: file_input.txt -> file_encrypted.enc
```

## Code Structure

- **derive_key(password, salt)**: Function to generate an AES key from the provided password using the **Scrypt** algorithm.
- **encrypt_file(password, input_file, output_file)**: Function to encrypt a file using AES-256.
- **decrypt_file(password, input_file, output_file)**: Function to decrypt a file that has been encrypted.
- **interactive_mode()**: Function to run the script in interactive mode if no arguments are provided.
- **main()**: Main function that processes CLI arguments or calls `interactive_mode()` if no arguments are provided.

## Error Handling

This script handles various errors such as:

- **FileNotFoundError**: If the input file is not found.
- **IOError**: If there is an error reading from or writing to a file.
- **ValueError**: If there is an error in generating the key or an invalid mode is selected.

If an error occurs, a clear message will be displayed in the terminal, helping users understand what went wrong.

## License

This script is free to use and distribute for non-commercial purposes. Feel free to modify and use it according to your needs.
