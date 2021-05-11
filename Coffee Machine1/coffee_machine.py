water = 400
milk = 540
beans = 120
cups = 9
dollar = 550
work = ""

while True:
    # main function of the coffee machine.
    def machine():
        ask()
        global work
        if work == "buy":
            buy()
        if work == "fill":
            fill()
        if work == "take":
            take()
        if work == 'remaining':
            intro()

    # prints the available amount.
    def intro():
        global water, milk, beans, cups, dollar
        print(f"""
    The coffee machine has:
    {water} of water
    {milk} of milk
    {beans} of coffee beans
    {cups} of disposable cups
    {dollar} of money
    """)

    # asks for action.
    def ask():
        global work
        work = input("Write action (buy, fill, take, remaining, exit):")

    # function for buyer.
    def buy():
        choice = input("What do you want to buy? 1 - espresso, 2 - latte, 3 - cappuccino, back - to main menu:")
        if choice == '1':
            espresso()
        elif choice == "2":
            latte()
        elif choice == "3":
            cappuccino()
        elif choice == "back":
            ask()
        return

    # subtracts the amount used for espresso
    def espresso():
        global water, milk, beans, cups, dollar
        if water < 250:
            print("Sorry, not enough water!")
        elif beans < 16:
            print("Sorry, not enough coffee beans!")
        elif cups < 1:
            print("Sorry, not enough cups!")
        else:
            print("I have enough resources, making you a coffee!")
            water = water - 250
            beans -= 16
            dollar += 4
            cups -= 1

        return

    # subtracts the amount used for latte.
    def latte():
        global water, milk, beans, cups, dollar
        if water < 350:
            print("Sorry, not enough water!")
        elif milk < 75:
            print("Sorry, not enough milk!")
        elif beans < 20:
            print("Sorry, not enough coffee beans!")
        elif cups < 1:
            print("Sorry, not enough cups!")
        else:
            print("I have enough resources, making you a coffee!")
            water -= 350
            milk -= 75
            beans -= 20
            dollar += 7
            cups -= 1

        return

    # subtracts the amount used for cappuccino
    def cappuccino():
        global water, milk, beans, cups, dollar
        if water < 200:
            print("Sorry, not enough water!")
        elif milk < 100:
            print("Sorry, not enough milk!")
        elif beans < 12:
            print("Sorry, not enough coffee beans!")
        elif cups < 1:
            print("Sorry, not enough cups!")
        else:
            print("I have enough resources, making you a coffee!")
            water -= 200
            milk -= 100
            beans -= 12
            dollar += 6
            cups -= 1
        return

    # function for the refill man.
    def fill():
        fill_water = int(input("Write how many ml of water do you want to add:"))
        fill_milk = int(input("Write how many ml of milk do you want to add:"))
        fill_beans = int(input("Write how many grams of coffee beans do you want to add:"))
        fill_cups = int(input("Write how many disposable cups of coffee do you want to add:"))

        global water, milk, beans, cups
        water += fill_water
        milk += fill_milk
        beans += fill_beans
        cups += fill_cups
        return

    # function for the money collector.
    def take():
        global dollar
        print(f"I gave you ${dollar}")
        dollar -= dollar
        return


    machine()
    if work == "exit":
        break