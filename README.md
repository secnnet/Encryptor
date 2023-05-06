# Encryptor

This is a Python script that provides functions to encrypt and decrypt files and folders using the Fernet encryption algorithm. The script relies on the Scrypt key derivation function to derive the encryption key from a user-specified password and a randomly generated salt.

## Usage

To use this script, you will need Python 3 installed on your system, along with the cryptography library. You can install the cryptography library using pip:

pip install cryptography

Once you have installed the necessary dependencies, you can run the script from the command line using the following commands:

python file_encrypt.py --encrypt <filename> <password>
python file_encrypt.py --encrypt-folder <foldername> <password>
python file_encrypt.py --decrypt <filename> <password>

The --encrypt command will encrypt a single file, the --encrypt-folder command will encrypt all files in a folder and its subfolders, and the --decrypt command will decrypt a single file.

## Requirements

This script requires Python 3 and the cryptography library. The script has been tested on Python 3.6 and higher.

## License

This script is released under the [MIT License](LICENSE.md). See LICENSE for more details.





