import re
import os
import binascii
import hashlib
import file_handler


class SignUp:
    def __init__(self, username, password, confirm_pass):
        self.username = username
        self.password = password
        self.confirm_pass = confirm_pass

    def pattern_user(self):
        pattern = "^[A-Za-z][A-Za-z0-9_]{7,29}$"
        patt = re.compile(pattern)
        matched = re.search(patt, self.username)
        if matched:
            return True
        else:
            return False

    def pattern_pass(self):
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
        if self.password == self.confirm_pass:
            return "Welcome, " + self.username
        else:
            return "Incorrect password"


class SignIn:
    def __init__(self, username, password):
        self.username = username
        self.password = password

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
        open_file = file_handler.FileHandler('Data/users.csv')
        read_file = open_file.read_file()
        for row in read_file:
            if row['username'] == username:
                return True
            else:
                return False

    def check_password(self):
        open_file = file_handler.FileHandler('Data/users.csv')
        read_file = open_file.read_file()
        for row in read_file:
            if row['username'] == self.username:
                if self.verify_password(row['password'], self.password):
                    return True
                elif not self.verify_password(row['password'], self.password):
                    return False
