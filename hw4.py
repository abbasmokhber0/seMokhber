import csv
import os
from datetime import datetime

# Define the path to the products.csv file
PRODUCTS_FILE = 'products.csv'

# Define the path to the user data file
USER_DATA_FILE = 'user_data.txt'

class User:
    def __init__(self, username, password, address, wallet, age):
        self.username = username
        self.password = password
        self.address = address
        self.wallet = wallet
        self.age = age

    def login(self):
        if os.path.exists(USER_DATA_FILE):
            with open(USER_DATA_FILE, 'r') as file:
                for line in file:
                    user_data = line.strip().split(',')
                    if user_data[0] == self.username and user_data[1] == self.password:
                        print("Welcome!")
                        return True
            print("No user found.")
        else:
            print("No user data found. Please sign up first.")
        return False

    def signup(self):
        if not os.path.exists(USER_DATA_FILE):
            open(USER_DATA_FILE, 'w').close()
        with open(USER_DATA_FILE, 'a') as file:
            file.write(f"{self.username},{self.password},{self.address},{self.wallet},{self.age}\n")
        print("Signup successful!")

    def charge_wallet(self, amount):
        self.wallet += amount
        with open(USER_DATA_FILE, 'r') as file:
            lines = file.readlines()
        with open(USER_DATA_FILE, 'w') as file:
            for line in lines:
                user_data = line.strip().split(',')
                if user_data[0] == self.username:
                    file.write(f"{self.username},{self.password},{self.address},{self.wallet},{self.age}\n")
                else:
                    file.write(line)
        print(f"Wallet charged with {amount}. New balance: {self.wallet}")

class Product:
    def __init__(self, product_id, name, product_type, price, is_available, rating):
        self.product_id = product_id
        self.name = name
        self.product_type = product_type
        self.price = price
        self.is_available = is_available.lower() == 'true'
        self.rating = rating

    def display_product_info(self):
        print(f"ID: {self.product_id}")
        print(f"Name: {self.name}")
        print(f"Type: {self.product_type}")
        print(f"Price: {self.price}")
        print(f"Availability: {'Available' if self.is_available else 'Not Available'}")
        print(f"Rating: {self.rating}")

    def purchase(self, user):
        if user.wallet < self.price:
            print("Insufficient funds in your wallet.")
        else:
            print("Payment successful!")
            user.wallet -= self.price
            with open(USER_DATA_FILE, 'r') as file:
                lines = file.readlines()
            with open(USER_DATA_FILE, 'w') as file:
                for line in lines:
                    user_data = line.strip().split(',')
                    if user_data[0] == user.username:
                        file.write(f"{user.username},{user.password},{user.address},{user.wallet},{user.age}\n")
                    else:
                        file.write(line)
            print("Product purchased successfully!")
            self.display_product_info()

def main():
    # Load products from the CSV file
    products = []
    with open(PRODUCTS_FILE, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row
        for row in reader:
            product_id, name, product_type, price, is_available, rating = row
            product = Product(int(product_id), name, product_type, float(price), is_available, float(rating))
            products.append(product)

    # User authentication
    while True:
        print("Welcome to the Product Management System!")
        print("1. Login")
        print("2. Signup")
        choice = input("Enter your choice (1 or 2): ")

        if choice == '1':
            username = input("Enter your username: ")
            password = input("Enter your password: ")
            user = User(username, password, '', 0, 0)
            if user.login():
                break
        elif choice == '2':
            username = input("Enter a username: ")
            password = input("Enter a password: ")
            address = input("Enter your address: ")
            wallet = float(input("Enter your wallet balance: "))
            age = int(input("Enter your age: "))
            user = User(username, password, address, wallet, age)
            user.signup()
            break
        else:
            print("Invalid choice. Please try again.")

    # Product management
    while True:
        print("\nProduct Management Menu:")
        print("1. View product information")
        print("2. Purchase a product")
        print("3. Charge wallet")
        print("4. Exit")
        choice = input("Enter your choice (1-4): ")

        if choice == '1':
            try:
                product_id = int(input("Enter the product ID: "))
            except ValueError:
                print("Please enter a valid product ID (a number).")
                continue

            found = False
            for product in products:
                if product.product_id == product_id:
                    if not product.is_available:
                        print("Product is not available.")
                    else:
                        product.display_product_info()
                    found = True
                    break
            if not found:
                print("Product not found.")
        elif choice == '2':
            product_id = int(input("Enter the product ID: "))
            found = False
            for product in products:
                if product.product_id == product_id:
                    if not product.is_available:
                        print("Product is not available.")
                    else:
                        product.purchase(user)
                    found = True
                    break
            if not found:
                print("Product not found.")
        elif choice == '3':
            amount = float(input("Enter the amount to charge your wallet: "))
            user.charge_wallet(amount)
        elif choice == '4':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
