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
        password = input("please enter a password: ")
        log_in = user.SignIn(username, password)
        print(log_in.check_user())
    elif msg1.lower() == 'n':
        msg2 = input("Do you want to create a new account in this messenger?(y/n)")
        if msg2.lower() == 'y':
            """
            Sign Up
            """
            print("(username must have length of more than 5 and include letter and digit)")
            username = input("please enter a username: ")
            open_file = file_handler.FileHandler('Data/users.csv')
            read_file = open_file.read_file()
            for row in read_file:
                while row['username'] == username:
                    username = input("Username Exists, Try Again: ")
            print("(password must have length of more than 7 and include uppercase, lowercase, digit and one of @#$!% )")
            password = input("please enter a password: ")
            confirm_pass = input("Confirm password: ")
            create_user = user.SignUp(username, password, confirm_pass)
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
                            create_user = user.SignUp(username, password, confirm_pass)
                        else:
                            break
                    print("Password is valid.")
                    print(create_user.check_pass())
            else:
                while True:
                    if not create_user.pattern_user():
                        print("Username invalid !!")
                        username = input("please enter a username: ")
                        create_user = user.SignUp(username, password, confirm_pass)
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
                            create_user = user.SignUp(username, password, confirm_pass)
                        else:
                            break
                    print("Password is valid.")
                    print(create_user.check_pass())

        elif msg2.lower() == 'n':
            print("Ok! Good luck")
            break
    else:
        print("Wrong answer!")
        continue
