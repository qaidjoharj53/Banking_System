import sys
import mysql.connector
from PyQt5 import QtWidgets, uic

# Establish a connection to the MySQL database
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="krAdarsh@4",
    database="BankingSystem"
)

# Create a cursor object to interact with the database
cursor = connection.cursor()

# Define the table structure for the customers
cursor.execute("""
    CREATE TABLE IF NOT EXISTS customers (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255),
        pin VARCHAR(255),
        balance DECIMAL(10, 2)
    )
""")
connection.commit()

def add_customer(name, pin, balance):
    cursor.execute("INSERT INTO customers (name, pin, balance) VALUES (%s, %s, %s)", (name.upper(), pin, balance))
    connection.commit()

def get_customer_data(name, pin):
    cursor.execute("SELECT id, balance FROM customers WHERE name = %s AND pin = %s", (name.upper(), pin))
    result = cursor.fetchone()
    return result  # Returns (id, balance) or None if not found

def update_customer_balance(customer_id, new_balance):
    cursor.execute("UPDATE customers SET balance = %s WHERE id = %s", (new_balance, customer_id))
    connection.commit()

class BankingSystem(QtWidgets.QMainWindow):
    def __init__(self):
        super(BankingSystem, self).__init__()
        uic.loadUi("banking.ui", self)  # Load the .ui file

        # Connect buttons to methods
        self.pushButton.clicked.connect(self.open_account)
        self.pushButton_2.clicked.connect(self.withdraw_money)
        self.pushButton_3.clicked.connect(self.deposit_money)
        self.pushButton_4.clicked.connect(self.check_balance)

    def open_account(self):
        name = self.lineEdit.text()
        pin = self.lineEdit_2.text()
        deposit = float(self.lineEdit_3.text())
        
        if name and pin and deposit >= 0:
            add_customer(name, pin, deposit)
            self.textBrowser.setPlainText(f"Account created successfully for {name} with initial deposit of {deposit:.2f} Rs.")
        else:
            self.textBrowser.setPlainText("Please enter valid details.")

    def withdraw_money(self):
        name = self.lineEdit.text()
        pin = self.lineEdit_2.text()
        withdrawal_amount = float(self.lineEdit4.text())

        customer = get_customer_data(name, pin)
        if customer:
            id, balance = customer
            if balance >= withdrawal_amount:
                new_balance = balance - withdrawal_amount
                update_customer_balance(id, new_balance)
                self.textBrowser_2.setPlainText(f"Withdrawal successful! New balance: {new_balance:.2f} Rs.")
            else:
                self.textBrowser_2.setPlainText("Insufficient balance.")
        else:
            self.textBrowser_2.setPlainText("Invalid name or pin.")

    def deposit_money(self):
        name = self.lineEdit.text()
        pin = self.lineEdit_2.text()
        deposit_amount = float(self.lineEdit4.text())

        customer = get_customer_data(name, pin)
        if customer:
            id, balance = customer
            new_balance = balance + deposit_amount
            update_customer_balance(id, new_balance)
            self.textBrowser_2.setPlainText(f"Deposit successful! New balance: {new_balance:.2f} Rs.")
        else:
            self.textBrowser_2.setPlainText("Invalid name or pin.")

    def check_balance(self):
        name = self.lineEdit.text()
        pin = self.lineEdit_2.text()

        customer = get_customer_data(name, pin)
        if customer:
            id, balance = customer
            self.textBrowser_2.setPlainText(f"Your current balance: {balance:.2f} Rs.")
        else:
            self.textBrowser_2.setPlainText("Invalid name or pin.")

# Run the application
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = BankingSystem()
    window.show()
    sys.exit(app.exec_())

# Close the cursor and connection when done
cursor.close()
connection.close()
