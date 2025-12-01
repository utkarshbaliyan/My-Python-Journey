from cryptography.fernet import Fernet
import os

# --- Key Management Functions ---


def write_key():
    """Generates a key and saves it to a file named 'key.key'."""
    key = Fernet.generate_key()
    with open("key.key", "wb") as key_file:
        key_file.write(key)


def load_key():
    """Loads the key from the current directory's 'key.key' file."""
    try:
        with open("key.key", "rb") as file:
            return file.read()
    except FileNotFoundError:
        # This should not happen if the key check below works
        print("Error: key.key not found. Please ensure it exists and try again.")
        exit()


# --- INITIAL SETUP: Create Key if it doesn't exist ---
# This is the fix for the FileNotFoundError.
# It ensures 'key.key' is created ONLY ONCE when the script runs for the first time.
if not os.path.exists("key.key"):
    print("--- FIRST TIME SETUP: Generating new encryption key (key.key) ---")
    write_key()

# Load the key and initialize Fernet
key = load_key()
fer = Fernet(key)

# --- Core Application Functions ---


def view():
    """Reads and decrypts existing passwords from 'passwords.txt'."""
    try:
        with open("passwords.txt", "r") as f:
            print("\n--- Saved Passwords ---")
            for line in f.readlines():
                data = line.rstrip()
                # Handle case where file might be empty or line is blank
                if not data:
                    continue

                try:
                    user, passw = data.split("|")
                    # Decrypt the password and decode it back to a string
                    decrypted_pass = fer.decrypt(passw.encode()).decode()
                    print(f"Account: {user} | Password: {decrypted_pass}")
                except Exception as e:
                    # Catch errors like incorrect formatting or corrupted data
                    print(
                        f"Error reading line: {line.rstrip()} (Check key or file format)"
                    )
            print("-----------------------\n")
    except FileNotFoundError:
        print("\nNote: 'passwords.txt' not found. Add a password to create it.\n")


def add():
    """Prompts the user for a new account and encrypts/saves the password."""
    name = input("Account Name: ")
    pwd = input("Password: ")

    # Encrypt the password and encode the result to a string before writing
    encrypted_pwd = fer.encrypt(pwd.encode()).decode()

    # 'a' mode appends to the file. Creates file if it doesn't exist.
    with open("passwords.txt", "a") as f:
        f.write(f"{name}|{encrypted_pwd}\n")

    print(f"Password for {name} added successfully.\n")


# --- Main Loop ---

if __name__ == "__main__":
    while True:
        mode = input(
            "Would you like to add a new password or view existing ones (view, add), press q to quit? "
        ).lower()
        if mode == "q":
            break

        if mode == "view":
            view()
        elif mode == "add":
            add()
        else:
            print("Invalid mode.")
            continue
