# Banking System Project

## Overview

This banking application allows users to create accounts, manage transactions (deposit and withdraw), and check balances through a user-friendly graphical interface built with PyQt5. The application interacts with a MySQL database to store and retrieve user information.

## Features

- **Account Creation**: Users can create an account by providing their name, PIN, and initial deposit amount.
- **Transaction Management**: Users can deposit and withdraw funds, as well as check their current account balance.
- **User Verification**: Users must verify their identity using their name and PIN to access transaction functionalities.

- **Graphical User Interface (GUI)**:
  - **banking.ui**: User interface for account creation.
  - **transaction.ui**: User interface for handling transactions.

## Requirements

- Python 3.x
- PyQt5
- mysql-connector-python

```bash
pip install PyQt5 mysql-connector-python
```

- MySQL server

## Set up the MySQL database:

- Create a database named "BankingSystem".
  Run the SQL commands from "BankingSystem.sql".

## Usage

1. Run the application:

```bash
python Bank_gui.py
```

2. Create Account: Fill in your details and click "Create Account."
3. Perform Transactions: Enter your name and PIN, then choose to deposit, withdraw, or check your balance.

## Key Changes:

- UI Creation: Developed banking.ui for account setup and transaction.ui for managing transactions.
- Functionality: Implemented features for account creation, transaction handling, and user verification.
