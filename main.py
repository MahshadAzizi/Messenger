import os
import user
import file_handler
import logging
import datetime
import message_management

print("Hello!\nWelcome to Messenger")
logging.basicConfig(filename='users_info.log', level=logging.INFO,
                    format='%(levelname)s*%(asctime)s -%(name)s -%(message)s', datefmt='%d-%b-%y %H:%M:%S')
while True:
    msg1 = input("Do you have an account?(y/n) ")  # msg == message
    if msg1.lower() == 'y':
        """
        Login
        """
        username = input("please enter a username: ")
        count = 0
        if user.User.check_username(username):
            if user.User.check_locked_user(username):
                if user.User.check_locked_time_user(username):
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
                        locked_user = user.User.locked_user(username)
                        print("Your account has been locked! Please try again 1 hour later")
                        logging.warning('user locked: {}'.format(username))
                        continue
                    dirName = f'Data/{username}'
                    now = datetime.datetime.now()
                    now_srt = now.strftime("%Y-%m-%d %H:%M:%S")
                    read_file = file_handler.FileHandler(dirName, 'Inbox')
                    read_inbox = read_file.read_file()
                    read_message = message_management.Inbox(dirName, 'Inbox')
                    number_unread_message = read_message.number_of_unread_messages()
                    print(f'you have {number_unread_message} new message(s)!')
                    while True:
                        msg3 = input("If you want to check\n1)Inbox\n2)Draft\n3)Sent \n4)send a message\n"
                                     "If you want to sign out in any step press 'Q': ")

                        if msg3 == '1':
                            check_messages = message_management.Message(dirName, 'Inbox')
                            number_message = check_messages.total_message()
                            show_inbox = check_messages.show_all_message()
                            tag_read = read_message.tag_read_message()
                            msg8 = input("Which one do you prefer \n1)reply message\n2)delete message: ")
                            if msg8 == '1':
                                msg4 = input("Which message do you want to reply?(for no one press 0): ")  # input id number of
                                # message
                                if msg4 == '0':
                                    continue
                                else:
                                    reply_message = message_management.Inbox(dirName, 'Inbox')
                                    reply_message2 = reply_message.reply_message(msg4)
                                    if reply_message2:
                                        text = input("Enter your text: ")
                                        msg6 = input("Are you sure to send message?(y/n): ")
                                        if msg6.lower() == 'y':
                                            dirUser = f'Data/{reply_message2}'
                                            check_id = user.User.check_id(dirUser, 'Inbox')
                                            open_inbox = file_handler.FileHandler(dirUser, 'Inbox')
                                            send_message = open_inbox.write_file(
                                                {'id': check_id, 'username': username, 'message': text, 'time': now_srt,
                                                 'readMessage': ''})
                                            check_id_2 = user.User.check_id(dirName, 'Sent')
                                            open_sent = file_handler.FileHandler(dirName, 'Sent')
                                            sent_message = open_sent.write_file(
                                                {'id': check_id_2, 'username': reply_message2, 'message': text,
                                                 'time': now_srt})
                                            logging.info('user {} send message to {} !'.format(username, reply_message2))
                                            print("Message sent successfully!")
                                        elif msg6.lower() == 'n':
                                            check_id = user.User.check_id(dirName, 'Draft')
                                            open_draft = file_handler.FileHandler(dirName, 'Draft')
                                            draft_message = open_draft.write_file(
                                                {'id': check_id, 'username': reply_message2, 'message': text,
                                                 'time': now_srt})
                                        else:
                                            print("Wrong answer!")
                                            continue
                                    elif not reply_message2:
                                        print("This id do not exist!")
                            elif msg8 == '2':
                                msg9 = input("Which message do you want to delete?(for no one press 0):")
                                if msg9 == '0':
                                    continue
                                else:
                                    check_id_user = user.User.check_id_user(dirName, 'Inbox', msg9)
                                    if check_id_user:
                                        delete_message = message_management.Message(dirName, 'Inbox')
                                        delete_message_2 = delete_message.delete_message(msg9)
                                        print("delete message successfully!")
                                    elif not check_id_user:
                                        logging.error('This id do not exist: {}'.format(username))
                                        print("This id do not exist!")
                            else:
                                logging.error('Wrong answer! user: {}'.format(username))
                                print("Wrong answer!")
                                continue
                        elif msg3 == '2':
                            check_messages = message_management.Message(dirName, 'Draft')
                            number_message = check_messages.total_message()
                            show_draft = check_messages.show_all_message()
                            msg5 = input("Which one do you prefer\n1)send message\n2)delete message:  ")
                            if msg5 == '1':
                                msg4 = input("Which message do you want to reply?(for no one press 0): ")  # input id number of
                                # message
                                if msg4 == '0':
                                    continue
                                else:
                                    reply_message = message_management.Inbox(dirName, 'Draft')
                                    reply_message2 = reply_message.reply_message(msg4)
                                    if reply_message2:
                                        text = input("Enter your text: ")
                                        msg6 = input("Are you sure to send message?(y/n): ")
                                        if msg6.lower() == 'y':
                                            dirUser = f'Data/{reply_message2}'
                                            check_id = user.User.check_id(dirUser, 'Inbox')
                                            open_inbox = file_handler.FileHandler(dirUser, 'Inbox')
                                            send_message = open_inbox.write_file(
                                                {'id': check_id, 'username': username, 'message': text, 'time': now_srt,
                                                 'readMessage': ''})
                                            check_id_2 = user.User.check_id(dirName, 'Sent')
                                            open_sent = file_handler.FileHandler(dirName, 'Sent')
                                            sent_message = open_sent.write_file(
                                                {'id': check_id_2, 'username': reply_message2, 'message': text,
                                                 'time': now_srt})

                                            open_draft = file_handler.FileHandler(dirName, 'Draft')
                                            delete_message_draft = open_draft.delete_row(msg4)

                                            logging.info('user {} send message to {} !'.format(username, reply_message2))
                                            print("Message sent successfully!")
                                        elif msg6.lower() == 'n':
                                            check_id = user.User.check_id(dirName, 'Draft')
                                            open_draft = file_handler.FileHandler(dirName, 'Draft')
                                            draft_message = open_draft.write_file(
                                                {'id': check_id, 'username': reply_message2, 'message': text,
                                                 'time': now_srt})
                                        else:
                                            logging.error('Wrong answer! user: {}'.format(username))
                                            print("Wrong answer!")
                                            continue
                                    elif not reply_message2:
                                        print("This id do not exist!")
                            elif msg5 == '2':
                                msg4 = input("Which message do you want to delete?(for no one press 0): ")
                                if msg4 == '0':
                                    continue
                                else:
                                    check_id_user = user.User.check_id_user(dirName, 'Draft', msg4)
                                    if check_id_user:
                                        delete_message = message_management.Message(dirName, 'Draft')
                                        delete_message_2 = delete_message.delete_message(msg4)
                                        print("delete message successfully!")
                                    elif not check_id_user:
                                        logging.error('this id do not exist: {}'.format(username))
                                        print("This id do not exist!")
                            else:
                                print("Wrong answer! ")
                                continue
                        elif msg3 == '3':
                            check_messages = message_management.Message(dirName, 'Sent')
                            number_message = check_messages.total_message()
                            show_sent = check_messages.show_all_message()
                            msg10 = input("Do you want to delete a message?(y/n) ")
                            if msg10.lower() == 'y':
                                msg4 = input("Which message do you want to delete?(for no one press 0): ")
                                if msg4 == '0':
                                    continue
                                else:
                                    check_id_user = user.User.check_id_user(dirName, 'Sent', msg4)
                                    if check_id_user:
                                        delete_message = message_management.Message(dirName, 'Sent')
                                        delete_message_2 = delete_message.delete_message(msg4)
                                        print("delete message successfully!")
                                    elif not check_id_user:
                                        logging.error('this id do not exist: {}'.format(username))
                                        print("This id do not exist!")
                            elif msg10.lower() == 'n':
                                continue
                            else:
                                logging.error('Wrong answer! user: {}'.format(username))
                                print("Wrong answer!")
                                continue
                        elif msg3 == '4':
                            username_2 = input("Enter the username of the person you want to text: ")
                            if user.User.check_username(username_2):
                                text = input("Enter your text: ")
                                msg6 = input("Are you sure to send message?(y/n): ")
                                if msg6.lower() == 'y':
                                    dirUser = f'Data/{username_2}'
                                    check_id = user.User.check_id(dirUser, 'Inbox')
                                    open_inbox = file_handler.FileHandler(dirUser, 'Inbox')
                                    send_message = open_inbox.write_file(
                                        {'id': check_id, 'username': username, 'message': text, 'time': now_srt,
                                         'readMessage': ''})
                                    check_id_2 = user.User.check_id(dirName, 'Sent')
                                    open_sent = file_handler.FileHandler(dirName, 'Sent')
                                    sent_message = open_sent.write_file(
                                        {'id': check_id_2, 'username': username_2, 'message': text, 'time': now_srt})

                                    logging.info('user {} send message to {} !'.format(username, username_2))
                                    print("Message sent successfully!")
                                elif msg6.lower() == 'n':
                                    check_id = user.User.check_id(dirName, 'Draft')
                                    open_draft = file_handler.FileHandler(dirName, 'Draft')
                                    draft_message = open_draft.write_file(
                                        {'id': check_id, 'username': username_2, 'message': text, 'time': now_srt})
                                else:
                                    logging.error('Wrong answer! user: {}'.format(username))
                                    print("Wrong answer!")
                                    continue

                            elif not user.User.check_username(username_2):
                                print("This username do not exist!")

                        elif msg3.upper() == 'Q':
                            logging.info('user log out: {}'.format(username))
                            break
                        else:
                            logging.error('Wrong answer! user: {}'.format(username))
                            print("Wrong answer!")
                            continue
                elif not user.User.check_locked_time_user(username):
                    print("your account is still locked! Please try later")
                    break
            elif not user.User.check_locked_user(username):
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
                    locked_user = user.User.locked_user(username)
                    print("Your account has been locked! Please try again 1 hour later")
                    logging.warning('user locked: {}'.format(username))
                    continue
                dirName = f'Data/{username}'
                now = datetime.datetime.now()
                now_srt = now.strftime("%Y-%m-%d %H:%M:%S")
                read_file = file_handler.FileHandler(dirName, 'Inbox')
                read_inbox = read_file.read_file()
                read_message = message_management.Inbox(dirName, 'Inbox')
                number_unread_message = read_message.number_of_unread_messages()
                print(f'you have {number_unread_message} new message(s)!')
                while True:
                    msg3 = input("If you want to check\n1)Inbox\n2)Draft\n3)Sent \n4)send a message\n"
                                 "If you want to sign out in any step press 'Q': ")

                    if msg3 == '1':
                        check_messages = message_management.Message(dirName, 'Inbox')
                        number_message = check_messages.total_message()
                        show_inbox = check_messages.show_all_message()
                        tag_read = read_message.tag_read_message()
                        msg8 = input("Which one do you prefer \n1)reply message\n2)delete message: ")
                        if msg8 == '1':
                            msg4 = input(
                                "Which message do you want to reply?(for no one press 0): ")  # input id number of
                            # message
                            if msg4 == '0':
                                continue
                            else:
                                reply_message = message_management.Inbox(dirName, 'Inbox')
                                reply_message2 = reply_message.reply_message(msg4)
                                if reply_message2:
                                    text = input("Enter your text: ")
                                    msg6 = input("Are you sure to send message?(y/n): ")
                                    if msg6.lower() == 'y':
                                        dirUser = f'Data/{reply_message2}'
                                        check_id = user.User.check_id(dirUser, 'Inbox')
                                        open_inbox = file_handler.FileHandler(dirUser, 'Inbox')
                                        send_message = open_inbox.write_file(
                                            {'id': check_id, 'username': username, 'message': text, 'time': now_srt,
                                             'readMessage': ''})
                                        check_id_2 = user.User.check_id(dirName, 'Sent')
                                        open_sent = file_handler.FileHandler(dirName, 'Sent')
                                        sent_message = open_sent.write_file(
                                            {'id': check_id_2, 'username': reply_message2, 'message': text,
                                             'time': now_srt})
                                        logging.info('user {} send message to {} !'.format(username, reply_message2))
                                        print("Message sent successfully!")
                                    elif msg6.lower() == 'n':
                                        check_id = user.User.check_id(dirName, 'Draft')
                                        open_draft = file_handler.FileHandler(dirName, 'Draft')
                                        draft_message = open_draft.write_file(
                                            {'id': check_id, 'username': reply_message2, 'message': text,
                                             'time': now_srt})
                                    else:
                                        print("Wrong answer!")
                                        continue
                                elif not reply_message2:
                                    print("This id do not exist!")
                        elif msg8 == '2':
                            msg9 = input("Which message do you want to delete?(for no one press 0):")
                            if msg9 == '0':
                                continue
                            else:
                                check_id_user = user.User.check_id_user(dirName, 'Inbox', msg9)
                                if check_id_user:
                                    delete_message = message_management.Message(dirName, 'Inbox')
                                    delete_message_2 = delete_message.delete_message(msg9)
                                    print("delete message successfully!")
                                elif not check_id_user:
                                    logging.error('this id do not exist: {}'.format(username))
                                    print("This id do not exist!")
                        else:
                            logging.error('Wrong answer! user: {}'.format(username))
                            print("Wrong answer!")
                            continue
                    elif msg3 == '2':
                        check_messages = message_management.Message(dirName, 'Draft')
                        number_message = check_messages.total_message()
                        show_draft = check_messages.show_all_message()
                        msg5 = input("Which one do you prefer\n1)send message\n2)delete message:  ")
                        if msg5 == '1':
                            msg4 = input(
                                "Which message do you want to reply?(for no one press 0): ")  # input id number of
                            # message
                            if msg4 == '0':
                                continue
                            else:
                                reply_message = message_management.Inbox(dirName, 'Draft')
                                reply_message2 = reply_message.reply_message(msg4)
                                if reply_message2:
                                    text = input("Enter your text: ")
                                    msg6 = input("Are you sure to send message?(y/n): ")
                                    if msg6.lower() == 'y':
                                        dirUser = f'Data/{reply_message2}'
                                        check_id = user.User.check_id(dirUser, 'Inbox')
                                        open_inbox = file_handler.FileHandler(dirUser, 'Inbox')
                                        send_message = open_inbox.write_file(
                                            {'id': check_id, 'username': username, 'message': text, 'time': now_srt,
                                             'readMessage': ''})
                                        check_id_2 = user.User.check_id(dirName, 'Sent')
                                        open_sent = file_handler.FileHandler(dirName, 'Sent')
                                        sent_message = open_sent.write_file(
                                            {'id': check_id_2, 'username': reply_message2, 'message': text,
                                             'time': now_srt})

                                        open_draft = file_handler.FileHandler(dirName, 'Draft')
                                        delete_message_draft = open_draft.delete_row(msg4)

                                        logging.info('user {} send message to {} !'.format(username, reply_message2))
                                        print("Message sent successfully!")
                                    elif msg6.lower() == 'n':
                                        check_id = user.User.check_id(dirName, 'Draft')
                                        open_draft = file_handler.FileHandler(dirName, 'Draft')
                                        draft_message = open_draft.write_file(
                                            {'id': check_id, 'username': reply_message2, 'message': text,
                                             'time': now_srt})
                                    else:
                                        print("Wrong answer!")
                                        continue
                                elif not reply_message2:
                                    print("This id do not exist!")
                        elif msg5 == '2':
                            msg4 = input("Which message do you want to delete?(for no one press 0): ")
                            if msg4 == '0':
                                continue
                            else:
                                check_id_user = user.User.check_id_user(dirName, 'Draft', msg4)
                                if check_id_user:
                                    delete_message = message_management.Message(dirName, 'Draft')
                                    delete_message_2 = delete_message.delete_message(msg4)
                                    print("delete message successfully!")
                                elif not check_id_user:
                                    logging.error('this id do not exist: {}'.format(username))
                                    print("This id do not exist!")
                        else:
                            logging.error('Wrong answer! user: {}'.format(username))
                            print("Wrong answer! ")
                            continue
                    elif msg3 == '3':
                        check_messages = message_management.Message(dirName, 'Sent')
                        number_message = check_messages.total_message()
                        show_sent = check_messages.show_all_message()
                        msg10 = input("Do you want to delete a message?(y/n) ")
                        if msg10.lower() == 'y':
                            msg4 = input("Which message do you want to delete?(for no one press 0): ")
                            if msg4 == '0':
                                continue
                            else:
                                check_id_user = user.User.check_id_user(dirName, 'Sent', msg4)
                                if check_id_user:
                                    delete_message = message_management.Message(dirName, 'Sent')
                                    delete_message_2 = delete_message.delete_message(msg4)
                                    print("delete message successfully!")
                                elif not check_id_user:
                                    logging.error('this id do not exist: {}'.format(username))
                                    print("This id do not exist!")
                        elif msg10.lower() == 'n':
                            continue
                        else:
                            logging.error('Wrong answer! user: {}'.format(username))
                            print("Wrong answer!")
                            continue
                    elif msg3 == '4':
                        username_2 = input("Enter the username of the person you want to text: ")
                        if user.User.check_username(username_2):
                            text = input("Enter your text: ")
                            msg6 = input("Are you sure to send message?(y/n): ")
                            if msg6.lower() == 'y':
                                dirUser = f'Data/{username_2}'
                                check_id = user.User.check_id(dirUser, 'Inbox')
                                open_inbox = file_handler.FileHandler(dirUser, 'Inbox')
                                send_message = open_inbox.write_file(
                                    {'id': check_id, 'username': username, 'message': text, 'time': now_srt,
                                     'readMessage': ''})
                                check_id_2 = user.User.check_id(dirName, 'Sent')
                                open_sent = file_handler.FileHandler(dirName, 'Sent')
                                sent_message = open_sent.write_file(
                                    {'id': check_id_2, 'username': username_2, 'message': text,'time': now_srt})

                                logging.info('user {} send message to {} !'.format(username, username_2))
                                print("Message sent successfully!")
                            elif msg6.lower() == 'n':
                                check_id = user.User.check_id(dirName, 'Draft')
                                open_draft = file_handler.FileHandler(dirName, 'Draft')
                                draft_message = open_draft.write_file(
                                    {'id': check_id, 'username': username_2, 'message': text,'time': now_srt})
                            else:
                                logging.error('Wrong answer! user: {}'.format(username))
                                print("Wrong answer!")
                                continue

                        elif not user.User.check_username(username_2):
                            print("This username do not exist!")

                    elif msg3.upper() == 'Q':
                        logging.info('user log out: {}'.format(username))
                        break
                    else:
                        logging.error('Wrong answer! user: {}'.format(username))
                        print("Wrong answer!")
                        continue
        elif not user.User.check_username(username):
            print("This username do not exist!")
    elif msg1.lower() == 'n':
        msg2 = input("Do you want to create a new account in this messenger?(y/n) ")
        if msg2.lower() == 'y':
            """
            Sign Up
            """
            print("(username must have length of more than 5 and include letter and digit)")
            username = input("please enter a username: ")
            read_file = file_handler.FileHandler.read_file_user('Data/users.csv')
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
                    print(create_user.check_pass())
                else:
                    while True:
                        if not create_user.pattern_pass():
                            print("Password invalid !!")
                            password = input("please enter a password: ")
                            confirm_pass = input("Confirm password: ")
                            create_user = user.User(username, password)
                            sign_up = create_user.signUp(confirm_pass,)
                        else:
                            break
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
                    print(create_user.check_pass())
            print("Your account was created successfully!")
            hashed_password = create_user.hash_password()
            add_user = file_handler.FileHandler.write_file_user('Data/users.csv', {'username': username,
                                                                                   'password': hashed_password})
            dirName = f'Data/{username}'
            if not os.path.exists(dirName):
                os.makedirs(dirName)
            else:
                print("Directory ", dirName, " already exists")
            open_file_inbox = file_handler.FileHandler(dirName, 'Inbox')
            create_inbox = open_file_inbox.write_new_file_inbox()
            open_file_draft = file_handler.FileHandler(dirName, 'Draft')
            create_draft = open_file_draft.write_new_file()
            open_file_sent = file_handler.FileHandler(dirName, 'Sent')
            create_sent = open_file_sent.write_new_file()
            msg7 = input("Do you want to login?(y/n): ")
            if msg7.lower() == 'y':
                continue
            elif msg7.lower() == 'n':
                print("Ok! Good luck")
                break
            else:
                logging.error('Wrong answer! user: {}' .format(username))
                print("Wrong answer!")
                continue
        elif msg2.lower() == 'n':
            print("Ok! Good luck")
            break
    else:
        logging.error('Wrong answer!')
        print("Wrong answer!")
        continue
