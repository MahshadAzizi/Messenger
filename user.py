import file_handler
import re


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

    def check_pass(self):
        if self.password == self.confirm_pass:
            return "Welcome, " + self.username
        else:
            return "Incorrect password"


class SignIn:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def check_user(self):
        open_file = file_handler.FileHandler('Data/users.csv')
        read_file = open_file.read_file()
        for row in read_file:
            if row['username'] == self.username and row['password'] == self.password:
                return "Welcome Back, " + self.username
            else:
                return "Incorrect data! please try again..."
