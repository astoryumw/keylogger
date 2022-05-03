from cryptography.fernet import Fernet

def load_key():
    return open("key.key","rb").read()

def decrypt():
    key = load_key()
    # print(f.readline())
    f = Fernet(key)
    # print(key)
    with open("encryptedLog.txt","rb") as file:
        encrypted_data = file.read()
    # print(encrypted_data)
    # print(type(encrypted_data))
    decrypted_data = f.decrypt(encrypted_data)
    print(decrypted_data)
    with open("decryptedLog.txt", "wb") as file:
        file.write(decrypted_data)

decrypt()