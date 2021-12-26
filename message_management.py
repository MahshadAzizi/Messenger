import file_handler
import os
import pandas as pd


class Message:
    def __init__(self, dirName, csv_type):
        self.dirName = dirName
        self.csv_type = csv_type

    def show_all_message(self):
        read_file_1 = file_handler.FileHandler(self.dirName, f'{self.csv_type}')
        read_file = read_file_1.read_file()
        # print(read_file)
        for row in read_file:
            print(f"id: {row['id']}, username: {row['username']}, message: {row['message']}")

    def delete_message(self, id):
        path = os.path.join(self.dirName, self.csv_type + '.csv')
        delete_message_1 = file_handler.FileHandler(self.dirName, self.csv_type)
        delete_message = delete_message_1.delete_row(id)


class Inbox(Message):
    def __init__(self, dirName, csv_type):
        super(Inbox, self).__init__(dirName, csv_type)

    def tag_read_message(self):
        read_file_1 = file_handler.FileHandler(self.dirName, f'{self.csv_type}')
        read_file = read_file_1.read_file()
        df = pd.DataFrame(read_file)
        df.replace('', '*', inplace=True)
        # path = os.path.join(self.dirName, self.csv_type + '.csv')
        # open_file = file_handler.FileHandler(self.dirName, f'{self.csv_type}')
        write_file = read_file_1.write_file(df.to_dict('records'), mode='w')

    def number_of_unread_messages(self):
        count = 0
        read_file_1 = file_handler.FileHandler(self.dirName, f'{self.csv_type}')
        read_file = read_file_1.read_file()
        for row in read_file:
            if row['readMessage'] != '*':
                count += 1
        return count

    def reply_message(self, id):
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

    # def ask_to_send(self):
    #     pass


class Sent(Message):
    def __init__(self, dirName, csv_type):
        super(Sent, self).__init__(dirName, csv_type)
