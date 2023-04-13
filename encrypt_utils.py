from cryptography.fernet import Fernet

# Generate a 256-bit key and save it in a file in the /keys directory.
# The key is saved as a sequence of 32 bytes encoded in base64.
def generateKey(path):
    key = Fernet.generate_key()
    with open(path, 'wb') as key_file:
        key_file.write(key)

# Import a key from a string and save it in a file in the /keys directory.
# The file must be formatted in base64 and contain a sequence of 32 bytes.
def importKey(path, string):
    with open(path, 'w') as key_file:
        key_file.write(string)

# Encrypt a byte array using a key from a file.
def encrypt(keyPath, bytes):
    with open(keyPath, 'rb') as key_file:
        key = key_file.read()
    f = Fernet(key)
    return f.encrypt(bytes)

# Decrypt a byte array using a key from a file.
def decrypt(keyPath, bytes):
    with open(keyPath, 'rb') as key_file:
        key = key_file.read()
    f = Fernet(key)
    return f.decrypt(bytes)