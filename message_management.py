import file_handler
import os
import pandas as pd


class Message:
    def __init__(self, dirName, csv_type):
        self.dirName = dirName
        self.csv_type = csv_type

    def show_all_message(self):
        read_file = file_handler.FileHandler.read_file_user(self.dirName, f'{self.csv_type}')
        print(read_file)
        # for row in read_file:
        #     return f"id: {row['id']}, username: {row['username']}, message: {row['message']}"

    def delete_message(self, id):
        path = os.path.join(self.dirName, self.csv_type + '.csv')
        delete_message_1 = file_handler.FileHandler(path)
        delete_message = delete_message_1.delete_row(id)


class Inbox(Message):
    def __init__(self, dirName, csv_type):
        super(Inbox, self).__init__(dirName, csv_type)

    def tag_read_message(self):
        read_file = file_handler.FileHandler.read_file_user(self.dirName, f'{self.csv_type}')
        df = pd.DataFrame(read_file)
        df.replace('', '*', inplace=True)
        path = os.path.join(self.dirName, self.csv_type + '.csv')
        open_file = file_handler.FileHandler(path)
        write_file = open_file.write_file(df.to_dict('records'), mode='w')

    def number_of_unread_messages(self):
        count = 0
        read_file = file_handler.FileHandler.read_file_user(self.dirName, f'{self.csv_type}')
        for row in read_file:
            if row['readMessage'] != '*':
                count += 1
        return count

    def reply_message(self, id):
        read_file = file_handler.FileHandler.read_file_user(self.dirName, f'{self.csv_type}')
        for row in read_file:
            if row['id'] == str(id):
                username = row['username']
                return username
        else:
            return False


class Draft(Message):
    def __init__(self, dirName, csv_type):
        super(Draft, self).__init__(dirName, csv_type)

    def ask_to_send(self):
        pass


class Sent(Message):
    def __init__(self, dirName, csv_type):
        super(Sent, self).__init__(dirName, csv_type)
