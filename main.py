import user
import file_handler

while True:
    print("Hello!\nWelcome to Messenger")
    msg1 = input("Do you have an account?(y/n) ")  # msg == message
    if msg1.lower() == 'y':
        open_file = file_handler.FileHandler('Data/users.csv')
        read_file = open_file.read_file()
        username = input("please enter a username: ")
        password = input("please enter a password: ")
        for row in read_file:
            if row['username'] == username and row['password'] == password:
                print("You are now logged in!")
            else:
                print("Incorrect data! please try again...")
        log_in = user.SignIn(username, password)
    elif msg1.lower() == 'n':
        username = input("please enter a username: ")
        open_file = file_handler.FileHandler('Data/users.csv')
        read_file = open_file.read_file()
        for row['username'] in read_file:
            while row['username'] == username:
                username = input("Username Exists, Try Again: ")
        password = input("please enter a password: ")
    else:
        print("wrong answer!")
        continue
