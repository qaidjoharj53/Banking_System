import mysql.connector

# Establish a connection to the MySQL database
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="<Your Password>",
    database="<Your Database>"
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

# Commit changes to the database
connection.commit()
i = 0
counter_1 = 1
counter_2 = 1
# Function to add a new customer to the database
def add_customer(name, pin, balance):
    cursor.execute("INSERT INTO customers (name, pin, balance) VALUES (%s, %s, %s)", (name.upper(), pin, balance))
    connection.commit()

# Function to retrieve customer data by name and pin
def get_customer_data(name, pin):
    cursor.execute("SELECT id, balance FROM customers WHERE name = %s AND pin = %s", (name.upper(), pin))
    result = cursor.fetchone()
    return result  # Returns (id, balance) or None if not found

# Function to update customer balance by id
def update_customer_balance(customer_id, new_balance):
    cursor.execute("UPDATE customers SET balance = %s WHERE id = %s", (new_balance, customer_id))
    connection.commit()

def displaystud():
    sql = "SELECT * FROM customers"
    cursor.execute(sql)
    customers = cursor.fetchall()

    for customer in customers:
        print(f"Customer ID: {customer[0]}")
        print(f"Name: {customer[1]}")
        print(f"Balance: {customer[3]} -/Rs")
        print("\n")
    return customers

  
while True:
    print("=====================================")
    print(" ----Welcome to Times Bank----       ")
    print("*************************************")
    print("=<< 1. Open a new account         >>=")
    print("=<< 2. Withdraw Money             >>=")
    print("=<< 3. Deposit Money              >>=")
    print("=<< 4. Check Customers & Balance  >>=")
    print("=<< 5. Exit/Quit                  >>=")
    print("*************************************")
    # The below statement takes the choice number from the user.
    choiceNumber = input("Select your choice number from the above menu : ")      
    if choiceNumber == "1":
        print("Choice number 1 is selected by the customer")
        NOC = eval(input("Number of Customers : "))
        i = i + NOC
        customerNames = []
        if i > 5:
            print("\n")
            print("Customer registration exceed reached or Customer registration too low")
            i = i - NOC
        else:
            while counter_1 <= i:
                name = input("Input Fullname : ")
                pin = str(input("Please input a pin of your choice : "))
                balance = 0
                deposition = eval(input("Please input a value to deposit to start an account : "))
                balance = balance + deposition

                # Add the new customer to the database
                add_customer(name, pin, balance)

                print("\nName=", end=" ")
                print(name)
                print("Pin=", end=" ")
                print(pin)
                print("Balance=", end=" ")
                print(balance, end=" ")
                print("-/Rs")
                counter_1 = counter_1 + 1
                counter_2 = counter_2 + 1
                print("\nYour name is added to the customer system")
                print("Your pin is added to the customer system")
                print("Your balance is added to the customer system")
                print("----New account created successfully !----")
                print("\n")
                print("Your name is available on the customer's list now : ")
                customerNames.append(name)
                print(customerNames)
                print("\n")
                print("Note! Please remember the Name and Pin")
                print("========================================")
        mainMenu = input("Please press enter key to go back to the main menu to perform another function or exit ...")        
    elif choiceNumber == "2":
        print("Choice number 2 is selected by the customer")
        n = 0
        # The while loop below would work when the pin or the username is wrong.
        while n < 1:
            k = -1
            name = input("Please input name : ")
            pin = input("Please input pin : ")
            # The while loop below will keep the function running to find the correct user.
            if get_customer_data(name, pin):
                        n = n + 1
                        id, balance = get_customer_data(name, pin)
                        # These statements below would show the customer balance and update list values according to
                        # the withdrawl made.
                        print("Your Current Balance: ", end=" ")
                        print(balance, end=" ")
                        print("-/Rs")
                        # This statement below takes the withdrawl from the customer.
                        deposition = eval(input("Enter the value you want to withdraw : "))
                        temp = balance - deposition
                        if(temp<0):
                            print("Balance too low..")
                            break
                        else:
                            balance = temp
                            update_customer_balance(id, balance)
                        print("\n")
                        print("----Withdrawl successful!----")
                        print("Your New Balance: ", balance, end=" ")
                        print("-/Rs\n\n")
            if n < 1:
                print("Your name and pin does not match!\n")
                break
            # This statement below helps the user to go back to the start of the program (main menu).
        mainMenu = input("Please press enter key to go back to main menu to perform another function or exit ...")
    elif choiceNumber == "3":
        
        print("Choice number 3 is selected by the customer")
        n = 0
        # The while loop below would work when the pin or the username is wrong.
        while n < 1:
            k = -1
            name = input("Please input name : ")
            pin = input("Please input pin : ")
            # The while loop below will keep the function running to find the correct user.
            if get_customer_data(name, pin):
                        n = n + 1
                        id, balance = get_customer_data(name, pin)
                        # These statements below would show the customer balance and update list values according to
                        # the deposition made.
                        print("Your Current Balance: ", end=" ")
                        print(balance, end=" ")
                        print("-/Rs")
                        #balance = (customerBalances[k])
                        # This statement below takes the depositionn from the customer.
                        deposition = eval(input("Enter the value you want to deposit : "))
                        balance = balance + deposition
                        update_customer_balance(id, balance)
                        print("\n")
                        print("----Deposition successful!----")
                        print("Your New Balance: ", balance, end=" ")
                        print("-/Rs\n\n")
            if n < 1:
                print("Your name and pin does not match!\n")
                break
            # This statement below helps the user to go back to the start of the program (main menu).
        mainMenu = input("Please press enter key to go back to main menu to perform another function or exit ...")
    elif choiceNumber == "4":
        j = 0
        print("Choice number 4 is selected by the customer")
        # This while loop will prevent the user using the account if the username or pin is wrong.
        while j < 1:
            name = input("Please input name : ")
            pin = input("Please input pin : ")
            # This while loop will keep the function running when variable k is smaller than length of the
            if get_customer_data(name, pin):
                j = j + 1
                id, balance = get_customer_data(name, pin)
                # These few statement would show the balance taken from the list.
                print("Your Current Balance:", end=" ")
                print(balance, end=" ")
                print("-/Rs\n")
            if j < 1:
                # The if condition above would work when the pin or the name is wrong.
                print("Your name and pin does not match!\n")
            # This statement below helps the user to go back to the start of the program (main menu).
        mainMenu = input("Please press enter key to go back to main menu to perform another function or exit ...")    
    elif choiceNumber == "5":
        # These statements would be just showed to the customer.
        print("Choice number 5 is selected by the customer")
        print("Thank you for using our banking system!")
        print("\n")
        print("Come again")
        print("Bye bye")
        break
    else:
        # This else function above would work when a wrong function is chosen.
        print("Invalid option selected by the customer")
        print("Please Try again!")
        # This statement below helps the user to go back to the start of the program (main menu).
        mainMenu = input("Please press enter key to go back to main menu to perform another function or exit ...")

# Close the cursor and connection when done
cursor.close()
connection.close()