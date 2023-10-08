import tkinter as tk
from tkinter import messagebox
import pickle

# Load existing customer data from a file or create empty lists
try:
    with open("bank_data.pkl", "rb") as file:
        customerData = pickle.load(file)
except FileNotFoundError:
    customerData = []


def save_customer_data():
    with open("bank_data.pkl", "wb") as file:
        pickle.dump(customerData, file)


def open_account():
    name = name_entry.get()
    pin = pin_entry.get()
    initial_balance = float(balance_entry.get())

    customerData.append({"Name": name, "PIN": pin, "Balance": initial_balance})
    save_customer_data()
    messagebox.showinfo("Success", "Account created successfully!")


def withdraw():
    name = name_entry.get()
    pin = pin_entry.get()
    amount = float(amount_entry.get())

    for customer in customerData:
        if customer["Name"] == name and customer["PIN"] == pin:
            if customer["Balance"] >= amount:
                customer["Balance"] -= amount
                save_customer_data()
                messagebox.showinfo("Success", f"Withdrew {amount} successfully!")
                break
            else:
                messagebox.showerror("Error", "Insufficient balance!")
                break
    else:
        messagebox.showerror("Error", "Invalid name or PIN!")


def deposit():
    name = name_entry.get()
    pin = pin_entry.get()
    amount = float(amount_entry.get())

    for customer in customerData:
        if customer["Name"] == name and customer["PIN"] == pin:
            customer["Balance"] += amount
            save_customer_data()
            messagebox.showinfo("Success", f"Deposited {amount} successfully!")
            break
    else:
        messagebox.showerror("Error", "Invalid name or PIN!")


def show_balance():
    name = name_entry.get()
    pin = pin_entry.get()

    for customer in customerData:
        if customer["Name"] == name and customer["PIN"] == pin:
            messagebox.showinfo("Balance", f"Your balance is {customer['Balance']} Rs.")
            break
    else:
        messagebox.showerror("Error", "Invalid name or PIN!")


# Create the main window
root = tk.Tk()
root.title("Banking System")

# Create and pack the user interface elements
name_label = tk.Label(root, text="Name:")
name_label.pack()
name_entry = tk.Entry(root)
name_entry.pack()

pin_label = tk.Label(root, text="PIN:")
pin_label.pack()
pin_entry = tk.Entry(root, show="*")
pin_entry.pack()

balance_label = tk.Label(root, text="Initial Balance:")
balance_label.pack()
balance_entry = tk.Entry(root)
balance_entry.pack()

open_account_button = tk.Button(root, text="Open Account", command=open_account)
open_account_button.pack()

amount_label = tk.Label(root, text="Amount:")
amount_label.pack()
amount_entry = tk.Entry(root)
amount_entry.pack()

withdraw_button = tk.Button(root, text="Withdraw", command=withdraw)
withdraw_button.pack()

deposit_button = tk.Button(root, text="Deposit", command=deposit)
deposit_button.pack()

balance_button = tk.Button(root, text="Check Balance", command=show_balance)
balance_button.pack()

root.mainloop()
