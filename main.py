import os
import user
import file_handler

print("Hello!\nWelcome to Messenger")
while True:
    msg1 = input("Do you have an account?(y/n) ")  # msg == message
    if msg1.lower() == 'y':
        """
        Login
        """
        username = input("please enter a username: ")
        count = 0
        if user.User.check_username(username):
            while count < 3:
                password = input("please enter a password: ")
                create_user = user.User(username, password)
                if create_user.check_password():
                    print("Welcome back, " + username)
                    log_in = create_user.signIn()
                    break
                elif not create_user.check_password():
                    count += 1
                    continue
            if count == 3:
                print("Your account has been locked!")
        elif not user.User.check_username(username):
            print("This username do not exist!")
        msg3 = input("")

    elif msg1.lower() == 'n':
        msg2 = input("Do you want to create a new account in this messenger?(y/n) ")
        if msg2.lower() == 'y':
            """
            Sign Up
            """
            print("(username must have length of more than 5 and include letter and digit)")
            username = input("please enter a username: ")
            open_file = file_handler.FileHandler('Data/users.csv')
            read_file = open_file.read_file()
            for row in read_file:
                while row['username'] == username.lower():
                    username = input("Username Exists, Try Again: ")
            print(
                "(password must have length of more than 7 and include uppercase, lowercase, digit and one of @#$!% )")
            password = input("please enter a password: ")
            confirm_pass = input("Confirm password: ")
            create_user = user.User(username.lower(), password)
            sign_up = create_user.signUp(confirm_pass)
            if create_user.pattern_user():
                if create_user.pattern_pass():
                    print("Password is valid.")
                    print(create_user.check_pass())
                else:
                    while True:
                        if not create_user.pattern_pass():
                            print("Password invalid !!")
                            password = input("please enter a password: ")
                            confirm_pass = input("Confirm password: ")
                            create_user = user.User(username, password)
                            sign_up = create_user.signUp(confirm_pass)
                        else:
                            break
                    print("Password is valid.")
                    print(create_user.check_pass())
            else:
                while True:
                    if not create_user.pattern_user():
                        print("Username invalid !!")
                        username = input("please enter a username: ")
                        create_user = user.User(username, password)
                        sign_up = create_user.signUp(confirm_pass)
                    else:
                        break
                if create_user.pattern_pass():
                    print("Password is valid.")
                    print(create_user.check_pass())
                else:
                    while True:
                        if not create_user.pattern_pass():
                            print("Password invalid !!")
                            password = input("please enter a password: ")
                            confirm_pass = input("Confirm password: ")
                            create_user = user.User(username, password)
                            sign_up = create_user.signUp(confirm_pass)
                        else:
                            break
                    print("Password is valid.")
                    print(create_user.check_pass())
            hashed_password = create_user.hash_password()
            add_user = open_file.write_file({'username': username, 'password': hashed_password})
            dirName = f'/Users/mahshad/Desktop/maktab/python/python-project/Data/{username}'
            if not os.path.exists(dirName):
                os.makedirs(dirName)
                print("Directory ", dirName, " Created ")
            else:
                print("Directory ", dirName, " already exists")
            create_inbox = file_handler.FileHandler.write_new_file(dirName, 'Inbox')
            create_draft = file_handler.FileHandler.write_new_file(dirName, 'Draft')
            create_sent = file_handler.FileHandler.write_new_file(dirName, 'Sent')

        elif msg2.lower() == 'n':
            print("Ok! Good luck")
            break
    else:
        print("Wrong answer!")
        continue
