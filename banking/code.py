from random import randint


class Account:
    """Represents a single bank account."""

    def __init__(self, name: str, phone: int, initial_deposit: int = 0):
        self.account_number = randint(10000, 999999)
        self.name = name
        self.phone = phone
        self.balance = initial_deposit

    def display_details(self):
        print(f"\n--- Account Details ---")
        print(f"Number:  {self.account_number}")
        print(f"Holder:  {self.name}")
        print(f"Phone:   {self.phone}")
        print(f"Balance: ₹{self.balance}")
        print("-" * 23)

    def deposit(self, amount: int):
        if amount > 0:
            self.balance += amount
            print(f"Successfully deposited ₹{amount}.")
        else:
            print("Deposit amount must be positive.")

    def withdraw(self, amount: int) -> bool:
        if amount > self.balance:
            print("Error: Insufficient balance.")
            return False
        if amount <= 0:
            print("Error: Amount must be positive.")
            return False

        self.balance -= amount
        print(f"Successfully withdrew ₹{amount}.")
        return True


class BankSystem:
    """Manages multiple bank accounts and system operations."""

    def __init__(self):
        # Using a dictionary for O(1) lookup: {account_number: AccountObject}
        self.accounts = {}

    def get_int_input(self, prompt: str) -> int:
        """Helper to ensure we get a valid integer from the user."""
        while True:
            try:
                return int(input(prompt))
            except ValueError:
                print("Invalid input. Please enter a number.")

    def create_account(self):
        name = input("Enter name: ")
        phone = self.get_int_input("Enter phone number: ")
        initial_balance = self.get_int_input("Enter initial deposit: ")

        new_acc = Account(name, phone, initial_balance)
        self.accounts[new_acc.account_number] = new_acc
        print(
            f"\nAccount created successfully! Your Account Number is: {new_acc.account_number}"
        )

    def transfer(self):
        sender_no = self.get_int_input("Enter sender account number: ")
        receiver_no = self.get_int_input("Enter receiver account number: ")

        sender = self.accounts.get(sender_no)
        receiver = self.accounts.get(receiver_no)

        if not sender or not receiver:
            print("Error: One or both account numbers are invalid.")
            return

        amount = self.get_int_input(
            f"Enter amount to transfer (Available: ₹{sender.balance}): "
        )
        if sender.withdraw(amount):
            receiver.deposit(amount)
            print("Transfer complete.")

    def run(self):
        """Main menu loop."""
        menu = {
            "1": ("Create Account", self.create_account),
            "2": (
                "Show All Accounts",
                lambda: [acc.display_details() for acc in self.accounts.values()],
            ),
            "3": ("Deposit", lambda: self.perform_transaction("deposit")),
            "4": ("Withdraw", lambda: self.perform_transaction("withdraw")),
            "5": ("Transfer", self.transfer),
            "6": ("Exit", exit),
        }

        while True:
            print("\n--- Banking System Menu ---")
            for key, (label, _) in menu.items():
                print(f"{key}. {label}")

            choice = input("Enter choice: ")

            if choice in menu:
                if choice in ["2", "3", "4", "5"] and not self.accounts:
                    print("No accounts found. Please create one first.")
                else:
                    menu[choice][1]()
            else:
                print("Invalid choice, try again.")

    def perform_transaction(self, action: str):
        acc_no = self.get_int_input(f"Enter account number for {action}: ")
        acc = self.accounts.get(acc_no)
        if acc:
            amount = self.get_int_input(f"Enter amount to {action}: ")
            if action == "deposit":
                acc.deposit(amount)
            else:
                acc.withdraw(amount)
        else:
            print("Account not found.")


if __name__ == "__main__":
    system = BankSystem()
    system.run()
