import os
from datetime import datetime

ACCOUNTS_FILE = 'accounts.txt'
TRANSACTIONS_FILE = 'transactions.txt'

def create_account():
    name = input("Enter your name: ")
    initial_deposit = float(input("Enter your initial deposit: "))
    password = input("Enter a password: ")
    
    account_number = generate_account_number()
    balance = initial_deposit
    
    with open(ACCOUNTS_FILE, 'a') as f:
        f.write(f"{account_number},{name},{password},{balance}\n")
    
    print(f"Your account number: {account_number} (Save this for login)")
    print("Account created successfully! (Account details saved to accounts.txt)")

def generate_account_number():
    if not os.path.exists(ACCOUNTS_FILE):
        return 123456  # Starting account number
    with open(ACCOUNTS_FILE, 'r') as f:
        lines = f.readlines()
        last_account_number = int(lines[-1].split(',')[0])
        return last_account_number + 1

def login():
    account_number = input("Enter your account number: ")
    password = input("Enter your password: ")
    
    with open(ACCOUNTS_FILE, 'r') as f:
        for line in f:
            acc_num, name, pwd, balance = line.strip().split(',')
            if acc_num == account_number and pwd == password:
                print("Login successful!")
                return account_number, float(balance)
    
    print("Invalid account number or password.")
    return None, None

def deposit(account_number, balance):
    amount = float(input("Enter amount to deposit: "))
    balance += amount
    log_transaction(account_number, "Deposit", amount)
    print(f"Deposit successful! Current balance: {balance}")
    return balance

def withdraw(account_number, balance):
    amount = float(input("Enter amount to withdraw: "))
    if amount > balance:
        print("Insufficient balance!")
    else:
        balance -= amount
        log_transaction(account_number, "Withdrawal", amount)
        print(f"Withdrawal successful! Current balance: {balance}")
    return balance

def log_transaction(account_number, transaction_type, amount):
    date = datetime.now().strftime("%Y-%m-%d")
    with open(TRANSACTIONS_FILE, 'a') as f:
        f.write(f"{account_number},{transaction_type},{amount},{date}\n")

def main():
    while True:
        print("\nWelcome to the Banking System!")
        print("1. Create Account")
        print("2. Login")
        print("3. Exit")
        choice = input("Enter your choice: ")
        
        if choice == '1':
            create_account()
        elif choice == '2':
            account_number, balance = login()
            if account_number:
                while True:
                    print("\n1. Deposit")
                    print("2. Withdraw")
                    print("3. Logout")
                    transaction_choice = input("Enter your choice: ")
                    
                    if transaction_choice == '1':
                        balance = deposit(account_number, balance)
                    elif transaction_choice == '2':
                        balance = withdraw(account_number, balance)
                    elif transaction_choice == '3':
                        print("Logged out successfully.")
                        break
                    else:
                        print("Invalid choice. Please try again.")
        elif choice == '3':
            print("Thank you for using the Banking System. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()