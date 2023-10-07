import mysql.connector as c
con = c.connect(host = "localhost", user = "root", password = "password@123")
cur = con.cursor()

cur.execute("use BankingSystem")


print("=====================================")

deposition = 0
withdrawal = 0
balance = 0
counter_1 = 1
counter_2 = 5
i = 0

# This statement below helps the program to run continuously.
while True:
    # os.system("cls")
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
        # The line below will take the no:of customers from the user.
        NOC = eval(input("Number of Customers : "))
 
        i = i + NOC
        # The if condition will restrict the number of new account to 5.


        # The while loop will run according to the no:of customers.
        while counter_1 <= i:
            # These few lines will take information from customer and then append them to the list.
            name = input("Input Fullname : ")
            pin = str(input("Please input a pin of your choice : "))
            balance = 0
            deposition = eval(input("Please input a value to deposit to start an account : "))
            balance = balance + deposition

            cur.execute(f"insert CustomerDetails(customer_name,account_pin,balance_amount) values('{name}','{pin}',{deposition});")
            con.commit()

            print("\nYour name is added to customers system")
            print("Your pin is added to customer system")
            print("Your balance is added to customer system")
            print("----New account created successfully !----")
            print("\n")
            print("Your name is avalilable on the customers list now : ")
            cur.execute("select customer_name,balance_amount from CustomerDetails;")
            data = cur.fetchall()
            for i in data:
                print("->Customer =", i[0], "\n", "->Balance =", i[1], "-/Rs")
            print("\n")
            print("Note! Please remember the Name and Pin")
            print("========================================")
            # This statement below helps the user to go back to the start of the program (main menu).
        mainMenu = input("Please press enter key to go back to main menu to perform another function or exit ...")
    elif choiceNumber == "2":
        j = 0
        print("Choice number 2 is selected by the customer")
        try:
            cur.execute(f"select balance_amount from CustomerDetails where customer_name = '{name}' and account_pin='{pin}';")
            amount = cur.fetchone()
            balance = 0
            for i in amount:
                balance += i
                print("Your Current Balance: ", end=" ")
                print(i, end=" ")
                print("-/Rs")
            # This statement below takes the depositionn from the customer.
            deposition = eval(input("Enter the value you want to withdraw : "))
            balance = balance - deposition
            cur.execute(
                f"update CustomerDetails set balance_amount = {balance} where customer_name = '{name}'and account_pin = '{pin}';")
            con.commit()
            print("----Deposition successful!----")
            cur.execute(
                f"select balance_amount from CustomerDetails where customer_name = '{name}' and account_pin='{pin}';")
            adamount = cur.fetchone()
            for i in adamount:
                print("Your Current Balance: ", end=" ")
                print(i, end=" ")
                print("-/Rs")
                # This statement below helps the user to go back to the start of the program (main menu).
        except:
            print("The name doesn't exist")

        mainMenu = input("Please press enter key to go back to main menu to perform another function or exit ...")
    elif choiceNumber == "3":
        print("Choice number 3 is selected by the customer")
        n = 0
        # The while loop below would work when the pin or the username is wrong.
        name = input("Please input name : ")
        pin = input("Please input pin : ")
        try:
            cur.execute(f"select balance_amount from CustomerDetails where customer_name = '{name}' and account_pin='{pin}';")
            amount = cur.fetchone()
            balance=0
            for i in amount:
                balance+=i
                print("Your Current Balance: ", end=" ")
                print(i, end=" ")
                print("-/Rs")
            # This statement below takes the depositionn from the customer.
            deposition = eval(input("Enter the value you want to deposit : "))
            balance = balance + deposition
            cur.execute(f"update CustomerDetails set balance_amount = {balance} where customer_name = '{name}'and account_pin = '{pin}';")
            con.commit()
            print("----Deposition successful!----")
            cur.execute(f"select balance_amount from CustomerDetails where customer_name = '{name}' and account_pin='{pin}';")
            adamount = cur.fetchone()
            for i in adamount:
                print("Your Current Balance: ", end=" ")
                print(i, end=" ")
                print("-/Rs")
                # This statement below helps the user to go back to the start of the program (main menu).
        except:
            print("The name doesn't exist")
        mainMenu = input("Please press enter key to go back to main menu to perform another function or exit ...")
    elif choiceNumber == "4":
        print("Choice number 4 is selected by the customer")
        k = 0
        print("Customer name list and balances mentioned below : ")
        print("\n")

        cur.execute("select customer_name,balance_amount from CustomerDetails;")
        data = cur.fetchall()
        for i in data:
            print("->Customer =",i[0],"\n","->Balance =",i[1],"-/Rs")
        mainMenu = input("Please press enter key to go back to main menu to perform another fuction or exit ...")
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
