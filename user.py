import re
import os
import binascii
import hashlib
import pandas as pd
import file_handler
import datetime
import logging

logging.basicConfig(filename='users_info.log', level=logging.INFO,
                    format='%(levelname)s*%(asctime)s -%(name)s -%(message)s', datefmt='%d-%b-%y %H:%M:%S')


class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def signUp(self, confirm_pass):
        self.confirm_pass = confirm_pass
        logging.info('Sign up user: {}'.format(self.username))

    def pattern_user(self):
        """The pattern that the username must have"""
        pattern = "^[A-Za-z][A-Za-z0-9_]{7,29}$"
        patt = re.compile(pattern)
        matched = re.search(patt, self.username)
        if matched:
            return True
        else:
            return False

    def pattern_pass(self):
        """The pattern that the password must have"""
        pattern = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$"
        patt = re.compile(pattern)
        matched = re.search(patt, self.password)
        if matched:
            return True
        else:
            return False

    def hash_password(self):
        """Hash a password for storing."""
        salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
        password_hash = hashlib.pbkdf2_hmac('sha512', self.password.encode('utf-8'),
                                            salt, 100000)
        password_hash = binascii.hexlify(password_hash)
        return (salt + password_hash).decode('ascii')

    def check_pass(self):
        """confirm password"""
        if self.password == self.confirm_pass:
            return "Welcome, " + self.username
        else:
            return "Incorrect password"

    def signIn(self):
        # self.logging_user(dirName)
        logging.info('Login user: {}'.format(self.username))

    def verify_password(self, stored_password, provided_password):
        """Verify a stored password against one provided by user"""
        salt = stored_password[:64]
        stored_password = stored_password[64:]
        password_hash = hashlib.pbkdf2_hmac('sha512',
                                            provided_password.encode('utf-8'),
                                            salt.encode('ascii'),
                                            100000)
        password_hash = binascii.hexlify(password_hash).decode('ascii')
        return password_hash == stored_password

    @staticmethod
    def check_username(username):
        """Checks the username"""
        read_file = file_handler.FileHandler.read_file_user('Data/users.csv')
        for row in read_file:
            if row['username'] == username.lower():
                return True
        else:
            return False

    def check_password(self):
        """Compares the entered password with the user"""
        read_file = file_handler.FileHandler.read_file_user('Data/users.csv')
        for row in read_file:
            if row['username'] == self.username:
                if self.verify_password(row['password'], self.password):
                    return True
                elif not self.verify_password(row['password'], self.password):
                    return False

    @staticmethod
    def check_id(dirName, csv_type):
        """ Gives each message an ID """
        open_file = file_handler.FileHandler(dirName, csv_type)
        read_file = open_file.read_file()
        df = pd.DataFrame(read_file)
        index = df.index
        number_of_rows = len(index)
        id_number = number_of_rows + 1
        return id_number

    @staticmethod
    def check_id_user(dirName, csv_type, id):
        read_file = file_handler.FileHandler(dirName, csv_type)
        read_inbox = read_file.read_file()
        for row in read_inbox:
            if row['id'] == id:
                return True
        else:
            return False

    @staticmethod
    def locked_user(username):
        now = datetime.datetime.now()
        now_srt = now.strftime("%Y-%m-%d %H:%M:%S")
        info = {'username': username, 'locktime': now_srt}
        write_locked_user = file_handler.FileHandler.write_file_user('Data/LockedUser.csv', info)

    @staticmethod
    def check_locked_time_user(username):
        read_file = file_handler.FileHandler.read_file_user('Data/LockedUser.csv')
        for row in read_file:
            if row['username'] == username:
                lockTime = row['locktime']
                date = datetime.datetime.strptime(lockTime, '%Y-%m-%d %H:%M:%S')
                now = datetime.datetime.now()
                duration = now - date
                duration_in_s = duration.total_seconds()
                if duration_in_s >= 3600:
                    return True
                else:
                    return False

    @staticmethod
    def check_locked_user(username):
        read_file = file_handler.FileHandler.read_file_user('Data/LockedUser.csv')
        for row in read_file:
            if row['username'] == username:
                return True
        else:
            return False


# check = User.check_locked_user('mahshad98')

# def pass_count(self):
#     count = 0
#     while count < 3:
#         if self.check_password():
#         elif not create_user.check_password():
#             count += 1
#             continue
#     if count == 3:
#         print("Your account has been locked!")
#         logging.info('user locked: {}'.format(username))

# @staticmethod
# def logging_user(self, dirName):
#     path = os.path.join(dirName + '.log')
#     logging.basicConfig(filename=path, level=logging.INFO,
#                         format='%(levelname)s*%(asctime)s -%(name)s -%(message)s', datefmt='%d-%b-%y %H:%M:%S')
