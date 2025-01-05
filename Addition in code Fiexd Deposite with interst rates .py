import os
from datetime import datetime
import getpass

ACCOUNTS_FILE = 'accounts.txt'
TRANSACTIONS_FILE = 'transactions.txt'
FD_FILE = 'fixed_deposits.txt'

def create_account():
    initial_deposit = float(input("Enter your initial deposit: "))
    
    if initial_deposit >= 25000:
        account_number = input("Enter your desired account number: ")
    else:
        print("You must deposit at least 25,000 RUS to choose your own account number.")
        account_number = generate_account_number()  # Generate a default account number
    
    name = input("Enter your name: ")
    password = getpass.getpass("Enter a password: ")  # Masked password input
    balance = initial_deposit
    
    with open(ACCOUNTS_FILE, 'a') as f:
        f.write(f"{account_number},{name},{password},{balance}\n")
    
    print(f"Your account number: {account_number} (Save this for login)")
    print("Account created successfully! (Account details saved to accounts.txt)")

def generate_account_number():
    if not os.path.exists(ACCOUNTS_FILE):
        return "123456"  # Starting account number
    with open(ACCOUNTS_FILE, 'r') as f:
        lines = f.readlines()
        last_account_number = int(lines[-1].split(',')[0])
        return str(last_account_number + 1)

def login():
    account_number = input("Enter your account number: ")
    password = getpass.getpass("Enter your password: ")  # Masked password input
    
    with open(ACCOUNTS_FILE, 'r') as f:
        for line in f:
            acc_num, name, pwd, balance = line.strip().split(',')
            if acc_num == account_number and pwd == password:
                print("Login successful!")
                fd_balance = get_fd_balance(account_number)
                print(f"Your Savings Balance: {balance}")
                print(f"Your Fixed Deposit Balance: {fd_balance}")
                return account_number, float(balance)
    
    print("Invalid account number or password.")
    return None, None

def get_fd_balance(account_number):
    total_fd = 0.0
    if os.path.exists(FD_FILE):
        with open(FD_FILE, 'r') as f:
            for line in f:
                acc_num, amount, duration, date, interest = line.strip().split(',')
                if acc_num == account_number:
                    total_fd += float(amount)
    return total_fd

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

def forget_password():
    account_number = input("Enter your account number: ")
    name = input("Enter your registered name: ")

    found = False
    with open(ACCOUNTS_FILE, 'r') as f:
        lines = f.readlines()

    with open(ACCOUNTS_FILE, 'w') as f:
        for line in lines:
            acc_num, acc_name, pwd, balance = line.strip().split(',')
            if acc_num == account_number and acc_name == name:
                found = True
                print("Account verified!")
                new_password = getpass.getpass("Enter your new password: ")
                f.write(f"{acc_num},{acc_name},{new_password},{balance}\n")
                print("Password reset successfully!")
            else:
                f.write(line)

    if not found:
        print("Account verification failed. Please check your details.")

def open_fixed_deposit(account_number, balance):
    amount = float(input("Enter amount for fixed deposit: "))
    if amount > balance:
        print("Insufficient balance to open fixed deposit.")
        return balance

    # Get the duration of the FD
    duration = int(input("Enter duration of fixed deposit in months: "))
    
    # Determine the interest rate based on the duration
    if 6 <= duration < 12:
        interest_rate = 4  # 4% interest rate for 6-12 months
    elif 12 <= duration <= 15:
        interest_rate = 7  # 7% interest rate for 12-15 months
    elif duration > 15:
        interest_rate = 8  # 8% interest rate for more than 15 months
    else:
        print("The minimum duration for a fixed deposit is 6 months.")
        return balance
    
    balance -= amount
    log_transaction(account_number, "Fixed Deposit Opened", amount)

    # Calculate interest on the amount
    interest = (amount * interest_rate) / 100
    print(f"Fixed Deposit of {amount} RUS opened for {duration} months at an interest rate of {interest_rate}%.")
    print(f"Interest earned: {interest} RUS")
    
    with open(FD_FILE, 'a') as f:
        f.write(f"{account_number},{amount},{duration},{interest},{datetime.now().strftime('%Y-%m-%d')}\n")

    print(f"Remaining balance after FD: {balance}")
    return balance

def close_fixed_deposit(account_number, balance):
    found = False
    with open(FD_FILE, 'r') as f:
        lines = f.readlines()

    with open(FD_FILE, 'w') as f:
        for line in lines:
            acc_num, amount, duration, date, interest = line.strip().split(',')
            if acc_num == account_number and not found:
                found = True
                balance += float(amount)
                log_transaction(account_number, "Fixed Deposit Closed", float(amount))
                print(f"Fixed Deposit of {amount} RUS closed. Added to balance. Current balance: {balance}")
            else:
                f.write(line)

    if not found:
        print("No fixed deposit found for this account.")

    return balance

def main():
    while True:
        print("\nWelcome to the Banking System!")
        print("1. Create Account")
        print("2. Login")
        print("3. Forget Password")
        print("4. Exit")
        choice = input("Enter your choice: ")
        
        if choice == '1':
            create_account()
        elif choice == '2':
            account_number, balance = login()
            if account_number:
                while True:
                    print("\n1. Deposit")
                    print("2. Withdraw")
                    print("3. Open Fixed Deposit")
                    print("4. Close Fixed Deposit")
                    print("5. Logout")
                    transaction_choice = input("Enter your choice: ")
                    
                    if transaction_choice == '1':
                        balance = deposit(account_number, balance)
                    elif transaction_choice == '2':
                        balance = withdraw(account_number, balance)
                    elif transaction_choice == '3':
                        balance = open_fixed_deposit(account_number, balance)
                    elif transaction_choice == '4':
                        balance = close_fixed_deposit(account_number, balance)
                    elif transaction_choice == '5':
                        print("Logged out successfully.")
                        break
                    else:
                        print("Invalid choice. Please try again.")
        elif choice == '3':
            forget_password()
        elif choice == '4':
            print("Thank you for using the Banking System. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
