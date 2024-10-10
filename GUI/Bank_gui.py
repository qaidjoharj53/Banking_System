import sys
from PyQt5 import QtWidgets, uic
import mysql.connector
from decimal import Decimal

pswd=input("Enter your Password: ")
database_name=input("Enter your Database name: ")

# Database connection setup
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password=pswd,
    database=database_name
)
banking_ui = 'Banking_System\\GUI\\banking.ui'
transaction_ui = 'Banking_System\\GUI\\transaction.ui'

class BankingUI(QtWidgets.QMainWindow):
    def __init__(self):
        super(BankingUI, self).__init__()
        uic.loadUi(banking_ui, self)
        
        # Access elements in banking.ui
        self.name_input = self.findChild(QtWidgets.QLineEdit, "lineEdit")
        self.pin_input = self.findChild(QtWidgets.QLineEdit, "lineEdit_2")
        self.deposit_input = self.findChild(QtWidgets.QLineEdit, "lineEdit_3")
        self.textBrowser = self.findChild(QtWidgets.QTextBrowser, "textBrowser")
        self.openAccountButton = self.findChild(QtWidgets.QPushButton, "pushButton")
        
        # New elements for transaction choice
        self.yesButton = self.findChild(QtWidgets.QPushButton, "pushButton_2")
        self.noButton = self.findChild(QtWidgets.QPushButton, "pushButton_3")
        self.label_4 = self.findChild(QtWidgets.QLabel, "label_4")  # Optional label
        
        # Connect buttons to their respective functions
        self.openAccountButton.clicked.connect(self.create_account)
        self.yesButton.clicked.connect(self.move_to_transactions)
        self.noButton.clicked.connect(self.close_banking)

        # Initially hide transaction buttons and label
        self.yesButton.setVisible(False)
        self.noButton.setVisible(False)
        self.label_4.setVisible(False)
    
    def create_account(self):
        name = self.name_input.text()
        pin = self.pin_input.text()
        deposit = self.deposit_input.text()
        
        if not name or not pin or not deposit:
            self.textBrowser.setText("All fields are required!")
            return
        
        try:
            deposit = float(deposit)
            
            # Check if the name and pin already exist in the database
            with db.cursor() as cursor:
                query = "SELECT * FROM customers WHERE name = %s AND pin = %s"
                cursor.execute(query, (name, pin))
                result = cursor.fetchone()
                
                if result:
                    # User already exists, redirect to transaction UI
                    self.textBrowser.setText(f"Welcome back, {name}! Redirecting to transaction page.")
                    self.move_to_transactions()  # Move to transaction UI
                    return
                
                # User does not exist, create new account
                insert_query = "INSERT INTO customers (name, pin, balance) VALUES (%s, %s, %s)"
                cursor.execute(insert_query, (name, pin, deposit))
                db.commit()
                self.textBrowser.setText(f"Account for {name} created successfully!")
                
                # Show transaction options after account is created
                self.label_4.setVisible(True)
                self.yesButton.setVisible(True)
                self.noButton.setVisible(True)
                
        except mysql.connector.Error as err:
            self.textBrowser.setText(f"Error: {str(err)}")
        except ValueError:
            self.textBrowser.setText("Invalid deposit amount!")

    def move_to_transactions(self):
        self.transaction_window = TransactionUI()
        self.transaction_window.show()
        self.close()  # Close the banking UI window after moving to transactions
    
    def close_banking(self):
        self.close()  # Close the banking UI window and stop the program

class TransactionUI(QtWidgets.QMainWindow):
    def __init__(self):
        super(TransactionUI, self).__init__()
        uic.loadUi(transaction_ui, self)
        
        # Access elements in transaction.ui
        self.name_input = self.findChild(QtWidgets.QLineEdit, "lineEdit")
        self.pin_input = self.findChild(QtWidgets.QLineEdit, "lineEdit_2")
        self.verify_button = self.findChild(QtWidgets.QPushButton, "pushButton")
        self.textBrowser = self.findChild(QtWidgets.QTextBrowser, "textBrowser")
        
        self.amount_input = self.findChild(QtWidgets.QLineEdit, "lineEdit_4")
        self.withdraw_button = self.findChild(QtWidgets.QPushButton, "pushButton_2")
        self.deposit_button = self.findChild(QtWidgets.QPushButton, "pushButton_3")
        self.check_balance_button = self.findChild(QtWidgets.QPushButton, "pushButton_4")
        self.textBrowser_2 = self.findChild(QtWidgets.QTextBrowser, "textBrowser_2")
        
        # Disable transaction buttons until user is verified
        self.withdraw_button.setEnabled(False)
        self.deposit_button.setEnabled(False)
        self.check_balance_button.setEnabled(False)
        
        # Connect buttons to functions
        self.verify_button.clicked.connect(self.verify_user)
        self.withdraw_button.clicked.connect(self.withdraw_amount)
        self.deposit_button.clicked.connect(self.deposit_amount)
        self.check_balance_button.clicked.connect(self.check_balance)
    
    def verify_user(self):
        name = self.name_input.text()
        pin = self.pin_input.text()
        
        if not name or not pin:
            self.textBrowser.setText("Name and PIN are required!")
            return
        
        with db.cursor() as cursor:
            query = "SELECT balance FROM customers WHERE name = %s AND pin = %s"
            cursor.execute(query, (name, pin))
            result = cursor.fetchone()
            
            if result:
                self.textBrowser.setText(f"User verified: {name}")
                self.withdraw_button.setEnabled(True)
                self.deposit_button.setEnabled(True)
                self.check_balance_button.setEnabled(True)
            else:
                self.textBrowser.setText("Verification failed! No matching records.")

    def withdraw_amount(self):
        name = self.name_input.text()
        pin = self.pin_input.text()
        amount = self.amount_input.text()

        if not amount:
            self.textBrowser_2.setText("Please enter an amount to withdraw.")
            return

        try:
            # Convert amount to Decimal instead of float
            amount = Decimal(amount)
            cursor = db.cursor()
            query = "SELECT balance FROM customers WHERE name = %s AND pin = %s"
            cursor.execute(query, (name, pin))
            result = cursor.fetchone()

            if result and result[0] >= amount:
                new_balance = result[0] - amount  # Now this will work since both are Decimal
                update_query = "UPDATE customers SET balance = %s WHERE name = %s AND pin = %s"
                cursor.execute(update_query, (new_balance, name, pin))
                db.commit()
                self.textBrowser_2.setText(f"Withdrawal successful! New balance: {new_balance}")
            else:
                self.textBrowser_2.setText("Insufficient balance or user not found.")

            cursor.close()
        except ValueError:
            self.textBrowser_2.setText("Invalid amount!")

    def deposit_amount(self):
        name = self.name_input.text()
        pin = self.pin_input.text()
        amount = self.amount_input.text()

        if not amount:
            self.textBrowser_2.setText("Please enter an amount to deposit.")
            return

        try:
            # Convert amount to Decimal instead of float
            amount = Decimal(amount)
            cursor = db.cursor()
            query = "SELECT balance FROM customers WHERE name = %s AND pin = %s"
            cursor.execute(query, (name, pin))
            result = cursor.fetchone()

            if result:
                # Make sure result[0] is also Decimal before addition
                new_balance = result[0] + amount
                update_query = "UPDATE customers SET balance = %s WHERE name = %s AND pin = %s"
                cursor.execute(update_query, (new_balance, name, pin))
                db.commit()
                self.textBrowser_2.setText(f"Deposit successful! New balance: {new_balance}")

            cursor.close()
        except ValueError:
            self.textBrowser_2.setText("Invalid amount!")

    def check_balance(self):
        name = self.name_input.text()
        pin = self.pin_input.text()
        
        with db.cursor() as cursor:
            query = "SELECT balance FROM customers WHERE name = %s AND pin = %s"
            cursor.execute(query, (name, pin))
            result = cursor.fetchone()
            
            if result:
                self.textBrowser_2.setText(f"Current balance: {result[0]}")
            else:
                self.textBrowser_2.setText("User not found.")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    
    # Create the banking window
    banking_window = BankingUI()
    banking_window.show()
    
    # Run the application
    sys.exit(app.exec_())
