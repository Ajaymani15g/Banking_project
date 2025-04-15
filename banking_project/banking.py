import json
import random
import os

DATA_FILE = 'accounts.json'

class BankAccount:
    def __init__(self, account_number, holder_name, pin, balance=0.0):
        self.account_number = account_number
        self.holder_name = holder_name
        self.pin = pin
        self.balance = balance

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            print(f"₹{amount:.2f} deposited. New balance: ₹{self.balance:.2f}")
        else:
            print("Amount must be positive.")

    def withdraw(self, amount):
        if amount <= 0:
            print("Amount must be positive.")
        elif amount > self.balance:
            print("Insufficient funds.")
        else:
            self.balance -= amount
            print(f"₹{amount:.2f} withdrawn. New balance: ₹{self.balance:.2f}")

    def check_balance(self):
        print(f"Account balance: ₹{self.balance:.2f}")

    def to_dict(self):
        return {
            'account_number': self.account_number,
            'holder_name': self.holder_name,
            'pin': self.pin,
            'balance': self.balance
        }

    @staticmethod
    def from_dict(data):
        return BankAccount(
            data['account_number'],
            data['holder_name'],
            data['pin'],
            data['balance']
        )

def load_accounts():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, 'r') as f:
        data = json.load(f)
        return {acc_num: BankAccount.from_dict(acc) for acc_num, acc in data.items()}

def save_accounts(accounts):
    data = {acc_num: acc.to_dict() for acc_num, acc in accounts.items()}
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

def create_account(accounts):
    name = input("Enter your name: ")
    pin = input("Set a 4-digit PIN: ")
    account_number = str(random.randint(10000000, 99999999))
    while account_number in accounts:
        account_number = str(random.randint(10000000, 99999999))
    account = BankAccount(account_number, name, pin)
    accounts[account_number] = account
    save_accounts(accounts)
    print(f"Account created! Your account number is {account_number}")

def login(accounts):
    acc_num = input("Enter your account number: ")
    pin = input("Enter your 4-digit PIN: ")
    account = accounts.get(acc_num)
    if account and account.pin == pin:
        print(f"Welcome back, {account.holder_name}!")
        return account
    else:
        print("Invalid account number or PIN.")
        return None

def admin_view(accounts):
    print("\nAll Accounts (Admin View):")
    for acc in accounts.values():
        print(f"Acc#: {acc.account_number} | Name: {acc.holder_name} | Balance: ₹{acc.balance:.2f}")
    print()

def main():
    accounts = load_accounts()
    while True:
        print("\n====== Python Bank ======")
        print("1. Create Account")
        print("2. Login to Account")
        print("3. Admin View (for demo)")
        print("4. Exit")

        choice = input("Choose an option: ")

        if choice == '1':
            create_account(accounts)
        elif choice == '2':
            user = login(accounts)
            if user:
                while True:
                    print("\n--- Account Menu ---")
                    print("1. Deposit")
                    print("2. Withdraw")
                    print("3. Check Balance")
                    print("4. Logout")
                    action = input("Select option: ")

                    if action == '1':
                        amt = float(input("Enter amount to deposit: ₹"))
                        user.deposit(amt)
                        save_accounts(accounts)
                    elif action == '2':
                        amt = float(input("Enter amount to withdraw: ₹"))
                        user.withdraw(amt)
                        save_accounts(accounts)
                    elif action == '3':
                        user.check_balance()
                    elif action == '4':
                        print("Logging out...")
                        break
                    else:
                        print("Invalid option.")
        elif choice == '3':
            admin_view(accounts)
        elif choice == '4':
            print("Thanks for banking with us!")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
