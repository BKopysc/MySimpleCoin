from colorama import init, Fore
import os
from identity_manager import IdentityManager



init(autoreset=True)
identity_manager = IdentityManager()
current_wallet = None

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def display_wallet_info():
    print("\n$$$$$$$$$$$$$$$$$$$$$$$$$")
    print("Wallet Information:")
    print(f"Created at: {current_wallet['created_at']}")
    print(f"Owner: {current_wallet['owner_name']}")
    print(f"Private Key: {current_wallet['private_key']}")
    print(f"Public address: {current_wallet['public_address']}")
    print("$$$$$$$$$$$$$$$$$$$$$$$$$")

def main_menu():
    print("\nWelcome to SimpleCoin")
    print("1. Create a new wallet")
    print("2. Load an existing .cryptowallet file")
    print("3. Quit")

def wallet_menu():
    print("\n-----------")
    print("1. Create new node")
    print("2. Connect to a node")
    print("3. Show wallet information")
    print("4. Quit")
    print("-----------\n")

def create_wallet():
    username = input(">>> Enter your username: ")
    global current_wallet
    current_wallet = identity_manager.create_wallet(username)
    print("\n$$ Wallet created")

def load_wallet():
    filepath = input(">>> Enter filepath: ")
    wallet_data = identity_manager.open_wallet(filepath)
    if(wallet_data == None ):
        return False
    global current_wallet
    current_wallet = wallet_data
    print("\n$$ Wallet loaded")
    return True

def create_node():
    print("Create!")

def connect_to_node():
    print("Connect!")



# Main program loop
while True:
    main_menu()
    choice = input("\n>>> Select an option: ")

    if choice == "1":
        create_wallet()
    elif choice == "2":
        state = load_wallet()
        if(state == False):
            continue
    elif choice == "3":
        quit()
    else:
        continue

    while True:
        wallet_menu()
        choice = input("\n>>> Select an option: ")

        if choice == "1":
            create_node()
        elif choice == "2":
            connect_to_node()
        elif choice == "3":
            display_wallet_info()
        elif choice == "4":
            quit()
        else:
            print("Invalid choice. Please select a valid option.")
