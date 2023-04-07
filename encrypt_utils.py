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

# Encrypt a file using a key from a file.
# The encrypted file is saved in the same directory as the original file
# The file is saved with the extension .encrypted.
def encryptFile(filePath, keyPath):
    with open(keyPath, 'rb') as key_file:
        key = key_file.read()
    f = Fernet(key)
    with open(filePath, 'rb') as file:
        original = file.read()
    encrypted = f.encrypt(original)
    with open(filePath + ".encrypted", 'wb') as encrypted_file:
        encrypted_file.write(encrypted)

# Decrypt a file using a key from a file.
# The decrypted file is saved in the same directory as the original file
# The .encrypted extension is removed from the file.
def decryptFile(filePath, keyPath):
    with open(keyPath, 'rb') as key_file:
        key = key_file.read()
    f = Fernet(key)
    with open(filePath, 'rb') as encrypted_file:
        encrypted = encrypted_file.read()
    decrypted = f.decrypt(encrypted)
    filePath = filePath.replace(".encrypted", "")
    with open(filePath, 'wb') as decrypted_file:
        decrypted_file.write(decrypted)