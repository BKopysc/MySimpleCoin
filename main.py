from colorama import init, Fore, Back
import os
from identity_manager import IdentityManager
from p2pnode import P2PNode
from time import sleep


init(autoreset=True)
identity_manager = IdentityManager()
current_wallet = None

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def display_wallet_info():
    print(Fore.GREEN + "\n$$$$$$$$$$$$$$$$$$$$$$$$$")
    print(Fore.GREEN + "Wallet Information:")
    print(Fore.LIGHTCYAN_EX+ f"Created at: {current_wallet['created_at']}")
    print(Fore.LIGHTCYAN_EX + f"Owner: {current_wallet['owner_name']}")
    print(Fore.LIGHTCYAN_EX + f"Private Key: {current_wallet['private_key']}")
    print(Fore.LIGHTCYAN_EX + f"Public address: {current_wallet['public_address']}")
    print(Fore.GREEN + "$$$$$$$$$$$$$$$$$$$$$$$$$")

def title():
    print(Fore.YELLOW + "\nWelcome to SimpleCoin")

def main_menu():
    print("\n1. Create a new wallet")
    print("2. Load an existing .cryptowallet file")
    print(Fore.RED + "3. Quit")

def wallet_menu():
    print("\n-----------")
    print("1. Create new node")
    print("2. Connect to a node")
    print("3. Show wallet information")
    print(Fore.RED + "4. Quit")
    print("-----------\n")

def create_wallet():
    username = get_input("Enter your username")
    global current_wallet
    current_wallet = identity_manager.create_wallet(username)
    print(Fore.GREEN + "\n$$ Wallet created")

def load_wallet():
    filepath = get_input("Enter file path", nl=False)
    wallet_data = identity_manager.open_wallet(filepath)
    if(wallet_data == None ):
        return False
    global current_wallet
    current_wallet = wallet_data
    print(Fore.GREEN + "\n$$ Wallet loaded")
    return True

def get_input(option="Select an option", nl=True, clr=False):
    if(nl):
        print(" ")
    if(clr == False):
        input_str = Fore.CYAN + ">>> " + option + ": "
    else:
        input_str = option

    return input(input_str)

def node_callback(event, node, connected_node, data):
    print("Event: " + event)
    print("Node: " + node)
    print("Connected Node: " + connected_node)
    print("Data: " + str(data))

def create_node():
    ip = get_input("Enter IP address", nl=False)
    port = get_input("Enter port", nl=False)
    node = P2PNode(ip, int(port), seed_node_info = {"ip": "127.0.0.1", "port": 6000},
        private_key = current_wallet["private_key"],
        id = current_wallet["public_address"], callback=node_callback)
    
    while(True):
        text = Fore.WHITE + "@ Press 'q' to quit\n@ Press 't' to Show Transactions\n@ Press 'a' to Add Transaction\n@ Press 'm' to Mine Transaction ID\n@ Press 'p' to PING"
        net_com = get_input(text, nl=False, clr=True)
        print(Back.RESET)
        if(net_com == "q"):
            print(Back.BLUE + "@ exiting node....")
            print(Back.RESET)
            break
        elif(net_com == "t"):
            print(Back.BLUE + "@ Showing transactions....")
            trans = node.get_transactions()
            print(Back.BLACK + str(trans))
            print(Back.RESET)
        elif(net_com == "a"):
            print(Back.BLUE + "@ Adding transaction....")
            tran_input = get_input("Enter sender", nl=False)
            tran_input2 = get_input("Enter receiver", nl=False)
            tran_input3 = get_input("Enter amount", nl=True)
            node.add_transaction(tran_input, tran_input2, float(tran_input3))
            print(Back.RESET)
        elif(net_com == "m"):
            print(Back.BLUE + "@ Mining")
            mine_input = get_input("Enter transaction ID", nl=True)
            print(Back.BLUE + "!@ Mining started...")
            node.mine_transaction(mine_input)
            print(Back.RESET)
        elif(net_com == "p"):
            print(Back.BLUE + "@ PING....")
            node.send_ping()
            print(Back.RESET)
        else:
            print(Back.RED + "@ Wrong command!")
            print(Back.RESET)
            continue
    node.stop()
    sleep(8)

def connect_to_node():
    print("Connect!")




#--------------- MAIN LOOP --------------------#

title()

while True: #==== MAIN MENU ====#
    main_menu() #1,2,3,4
    choice = get_input()

    if choice == "1": #----- CREATE WALLET -----#
        create_wallet()
    elif choice == "2": #----- LOAD WALLET -----#
        state = load_wallet()
        if(state == False):
            continue
    elif choice == "3": #----- QUIT -----#
        quit()
    else:
        print(Back.RED + "Invalid choice. Please select a valid option.\n")
        continue

    while True: #==== WALLET MENU ====#
        wallet_menu() #1,2,3,44
        choice = get_input(nl=False)

        if choice == "1": #----- CREATE NEW NODE -----#
            create_node()
        elif choice == "2": #----- CONNECT TO NEW NODE ---- #
            connect_to_node()
        elif choice == "3": #----- DISPLAY WALLET INFO -----#
            display_wallet_info()
        elif choice == "4": #----- QUIT -----#
            quit()
        else:
            print(Back.RED + "Invalid choice. Please select a valid option.")
            continue
