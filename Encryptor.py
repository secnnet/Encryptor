import pathlib
import secrets
import os
import base64
import getpass

import cryptography
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt


def generate_salt(size=16):
    """Generate the salt used for key derivation, 
    `size` is the length of the salt to generate"""
    return secrets.token_bytes(size)


def derive_key(salt, password, n=2**14, r=8, p=1, key_length=32):
    """Derive the key from the `password` using the passed `salt` and Scrypt key derivation function"""
    kdf = Scrypt(salt=salt, length=key_length, n=n, r=r, p=p)
    return kdf.derive(password.encode())


def load_salt():
    # load the salt from the file "salt.salt" and return its contents
    return open("salt.salt", "rb").read()


def generate_key(password, salt_size=16, load_existing_salt=False, save_salt=True,
                 n=2**14, r=8, p=1, key_length=32):
    """Generates a key from a `password` and the salt.
    If `load_existing_salt` is True, it'll load the salt from a file
    in the current directory called "salt.salt".
    If `save_salt` is True, then it will generate a new salt
    and save it to "salt.salt" """
    if load_existing_salt:
        # load the existing salt from a file
        salt = load_salt()
    elif save_salt:
        # generate a new salt and save it to a file
        salt = generate_salt(salt_size)
        with open("salt.salt", "wb") as salt_file:
            salt_file.write(salt)
    # derive the key from the salt and the password using Scrypt key derivation function
    derived_key = derive_key(salt, password, n, r, p, key_length)
    # encode the key using Base 64 and return it
    return base64.urlsafe_b64encode(derived_key)


def encrypt(filename, key):
    """Given a filename (str) and key (bytes), it encrypts the file and write it"""
    # Initialize a Fernet object with the key
    f = Fernet(key)
    # Open the input file and output file using buffered streams
    with open(filename, "rb") as infile, open(f"{filename}.enc", "wb") as outfile:
        # Encrypt the file contents in chunks
        while True:
            chunk = infile.read(8192)
            if not chunk:
                break
            outfile.write(f.encrypt(chunk))


def encrypt_folder(foldername, key):
    # Encrypt all files in the specified folder and its subfolders
    for child in pathlib.Path(foldername).glob("*"):
        if child.is_file():
            print(f"[*] Encrypting {child}")
            # encrypt the file
            encrypt(child, key)
        elif child.is_dir():
            # if it's a folder, encrypt all its contents recursively
            encrypt_folder(child, key)


def decrypt(filename, key):
    """Given a filename (str) and key (bytes), it decrypts the file and write it"""
    # Initialize a Fernet object with the key
    f = Fernet(key)
    # Open the input file and output file using buffered streams
    with open(filename, "rb") as infile, open(f"{filename[:-4]}", "wb") as outfile:
        # Decrypt the file contents
