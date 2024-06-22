class Person:
    def __init__(self, username, password, address, wallet, age):
        self.username = username
        self.password = password
        self.address = address
        self.wallet = wallet
        self.age = age

    def charge_wallet(self, amount):
        self.wallet += amount


def login():
    username = input("Enter your username: ")
    password = input("Enter your password: ")

    with open("users.txt", "r") as file:
        for line in file:
            user_data = line.strip().split(",")
            if user_data[0] == username and user_data[1] == password:
                return Person(*user_data)

    return None


def signup():
    username = input("Enter a username: ")
    password = input("Enter a password: ")
    address = input("Enter your address: ")
    wallet = float(input("Enter your wallet amount: "))
    age = int(input("Enter your age: "))

    person = Person(username, password, address, wallet, age)

    with open("users.txt", "a") as file:
        file.write(f"{person.username},{person.password},{person.address},{person.wallet},{person.age}\n")

    return person


def main():
    print("Welcome to the App!")

    while True:
        choice = input("Do you want to login or sign up? (login/signup): ")

        if choice.lower() == "login":
            person = login()
            if person:
                print("Welcome,", person.username)
                break
            else:
                print("No user found.")
        elif choice.lower() == "signup":
            person = signup()
            print("Sign up successful!")
            print("Welcome,", person.username)
            break
        else:
            print("Invalid choice. Please enter 'login' or 'signup'.")

    while True:
        charge_choice = input("Do you want to charge your wallet? (yes/no): ")

        if charge_choice.lower() == "yes":
            amount = float(input("Enter the amount to charge: "))
            person.charge_wallet(amount)
            print("Wallet charged successfully. Current wallet balance:", person.wallet)
        elif charge_choice.lower() == "no":
            break
        else:
            print("Invalid choice. Please enter 'yes' or 'no'.")


if __name__ == "__main__":
    main()