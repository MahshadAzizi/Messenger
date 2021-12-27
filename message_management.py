import file_handler
import os
import pandas as pd
from tabulate import tabulate


class Message:
    def __init__(self, dirName, csv_type):
        self.dirName = dirName
        self.csv_type = csv_type

    def show_all_message(self):
        """Displays all messages in the desired csv file"""
        path = os.path.join(self.dirName, self.csv_type + '.csv')
        df = pd.read_csv(path, index_col=0)
        print(tabulate(df, headers='keys', tablefmt='pretty'))


    def delete_message(self, id):
        """Clears the message based on the ID entered by the user"""
        path = os.path.join(self.dirName, self.csv_type + '.csv')
        delete_message_1 = file_handler.FileHandler(self.dirName, self.csv_type)
        delete_message = delete_message_1.delete_row(id)

    def total_message(self):
        """Displays the total number of messages"""
        open_file = file_handler.FileHandler(self.dirName, self.csv_type)
        read_file = open_file.read_file()
        df = pd.DataFrame(read_file)
        index = df.index
        number_of_rows = len(index)
        print(f"you have {number_of_rows} messages ")


class Inbox(Message):
    def __init__(self, dirName, csv_type):
        super(Inbox, self).__init__(dirName, csv_type)

    def tag_read_message(self):
        """If a message is read, it gives it a single star"""
        read_file_1 = file_handler.FileHandler(self.dirName, f'{self.csv_type}')
        read_file = read_file_1.read_file()
        df = pd.DataFrame(read_file)
        df.replace('', '*', inplace=True)
        write_file = read_file_1.write_file(df.to_dict('records'), mode='w')

    def number_of_unread_messages(self):
        """Displays the number of unread messages"""
        count = 0
        read_file_1 = file_handler.FileHandler(self.dirName, f'{self.csv_type}')
        read_file = read_file_1.read_file()
        for row in read_file:
            if row['readMessage'] != '*':
                count += 1
        return count

    def reply_message(self, id):
        """The message that the user replies to"""
        read_file_1 = file_handler.FileHandler(self.dirName, f'{self.csv_type}')
        read_file = read_file_1.read_file()
        for row in read_file:
            if row['id'] == str(id):
                username = row['username']
                return username
        else:
            return False


class Draft(Message):
    def __init__(self, dirName, csv_type):
        super(Draft, self).__init__(dirName, csv_type)


class Sent(Message):
    def __init__(self, dirName, csv_type):
        super(Sent, self).__init__(dirName, csv_type)
