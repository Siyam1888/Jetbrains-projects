from random import choice
from string import digits
import sqlite3


# **********************   SQL QUERY FUNCTIONS START HERE *********************************

conn = sqlite3.connect('card.s3db')
cur = conn.cursor()

# if __name__ == '__main__':
#     # cur.execute("DROP TABLE card")
#     cur.execute("""CREATE TABLE card (
#             id INTEGER,
#             number TEXT,
#             pin TEXT,
#             balance INTEGER DEFAULT 0
#         );
#     """)
#     conn.commit()


# adds new card numbers and pins
def insert_data(card_no, pin):
    with conn:
        cur.execute("INSERT INTO card (number, pin) VALUES(:card_no, :pin)",
                    {'card_no': card_no, 'pin': pin})


# fetches the pin number of the given card number
def get_pin(card_no):
    cur.execute('SELECT pin FROM card WHERE number = :card_no', {'card_no': card_no})
    return cur.fetchone()


# fetches the current balance of a user
def get_balance(card_no):
    cur.execute('SELECT balance FROM card WHERE number = :card_no', {'card_no': str(card_no)})
    return cur.fetchone()


def update_balance(card_no, amount, operation):
    current_balance = get_balance(card_no)[0]
    with conn:
        if operation == 'add':
            cur.execute("UPDATE card SET balance = balance + :amount WHERE number = :card_no",
                        {'card_no': card_no, 'amount': amount})
        elif operation == 'subtract' and current_balance >= amount:
            cur.execute("UPDATE card SET balance = balance - :amount WHERE number = :card_no",
                        {'card_no': card_no, 'amount': amount})


# deletes an account
def remove_card(card_no):
    with conn:
        cur.execute("DELETE FROM card WHERE number = :card_no", {'card_no': card_no})


def all_card_nums():
    card_nums = cur.execute("SELECT number FROM card")
    card_nums = card_nums.fetchall()
    nums = list()
    for element in card_nums:
        nums.append(element[0])

    return nums

# **********************   SQL QUERY FUNCTIONS END HERE *********************************


# Generates random number of given digits
def number_generator(n_digits):
    code = list()
    for i in range(n_digits):
        code.append(choice(digits))

    return ''.join(code)


# generates the last value according to the luhn algorithm
def checksum(number):
    # converting the number to a list for editing it according to the algorithm
    edited = list(number)
    total = 0
    last_digit = 0
    # iterating over the odd digits
    for i in range(0, len(edited), 2):
        edited[i] = str(int(edited[i]) * 2)
        if int(edited[i]) > 9:
            edited[i] = str(int(edited[i]) - 9)
    # finding the sum of digits
    for digit in edited:
        total += int(digit)

    # finding the value of the last digit
    while total % 10 != 0:
        total += 1
        last_digit += 1

    return str(last_digit)


# checks if a card number is valid or not according to luhn algorithm
def luhn(number):
    last_digit = number[-1]
    num_except_last_digit = number[:-1]
    luhn_last_digit = checksum(num_except_last_digit)
    return last_digit == luhn_last_digit


# checks for previous account numbers and generates new account number
def account_number(identifier_list=None):
    # if list is not given, an empty list will be used
    if identifier_list is None:
        identifier_list = list()

    issuer_identification = '400000' # constant IIN = 400000
    account_identifier = number_generator(9) # random account identifier

    # checking uniqueness of account identifier
    if account_identifier in identifier_list:
        account_identifier = number_generator(9)

    # adding the identifier to the list and generating the account number
    identifier_list.append(account_identifier)
    without_checksum = issuer_identification + account_identifier
    card_number = without_checksum + checksum(without_checksum)

    return card_number


# creates a new account
def create_account():
    # if card_dict is None:
    #     card_dict = dict()
    print('Your card has been created')
    card_number = account_number()
    pin = number_generator(4)
    # card_dict[card_number] = pin
    insert_data(card_number, pin) # inserts the new data to the database
    print('Your card number:')
    print(card_number)
    print('Your card PIN:')
    print(pin)


# logs the user in if the number and pin are verified
def login():
    global logged_in, card_no
    card_num = input('Enter your card number:\n')
    pin = input('Enter your PIN: \n')

    card_no = card_num

    # gets the pin from database and verifies it
    try:
        if get_pin(card_num)[0] == pin:
            print('You have successfully logged in')
            logged_in = True
            return card_num
        else:
            print('Wrong card number or PIN!')
    except TypeError:
        print('Wrong card number or PIN!')


# prints the current balance of a logged in user
def balance(card_no):
    balance = get_balance(card_no)[0]
    return balance


# logs out a logged in user
def logout():
    global logged_in
    print('You have successfully logged out')
    logged_in = False


# adds money to a account
def add_income(card_no):
    amount = input("Enter income: \n")
    amount = int(amount)
    update_balance(card_no, amount, 'add')
    print("Income was added!")


# transfers money from one account to another
def transfer(sender_card_no):
    all_cards = all_card_nums()
    print("Transfer")
    receiver_card_no = input("Card Number: \n")
    if luhn(receiver_card_no):
        if receiver_card_no in all_cards:
            if receiver_card_no != sender_card_no:
                transfer_amount = input("Enter how much money you want to transfer:")
                transfer_amount = int(transfer_amount)
                if balance(sender_card_no) >= transfer_amount:
                    # deducts the amount from the sender account # adds the amount to the receiver account
                    update_balance(card_no, transfer_amount, 'subtract')
                    update_balance(receiver_card_no, transfer_amount, 'add')
                    print("Success!")
                else:
                    print("Not enough money!")
            else:
                print("You can't transfer money to the same account!")
        else:
            print("Such a card does not exist.")
    else:
        print("Probably you made mistake in the card number. Please try again!")


def close_account(card_no):
    if card_no in all_card_nums():
        remove_card(card_no)
        print("The account has been closed!")


def logged_in_facilities(card_no):
    global logged_in, going_on
    option = input("""
1. Balance
2. Add income
3. Do transfer
4. Close account
5. Log out
0. Exit \n""")
    if option == '1':
        print(f'Balance: {balance}')
    elif option == '2':
        add_income(card_no)
        # logged_in = False
    elif option == '3':
        transfer(card_no)
    elif option == '4':
        close_account(card_no)
    elif option == '5':
        logout()
    elif option == '0':
        print('Bye!')
        logged_in = False
        going_on = False
    return logged_in


card_no = None
logged_in = False
going_on = True
while going_on:
    option = input("""
1. Create an account
2. Log into account
0. Exit \n""")
    if option == '1':
        create_account()
    elif option == '2':
        login()
        while logged_in:
            logged_in_facilities(card_no)

    elif option == '0':
        print('Bye!')
        break



        










