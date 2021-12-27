import csv
import os
import pandas as pd


class FileHandler:
    def __init__(self, dirName, csv_type):
        self.dirName = dirName
        self.csv_type = csv_type

    def read_file(self):
        if os.path.exists(os.path.join(self.dirName, self.csv_type + '.csv')):
            with open(os.path.join(self.dirName, self.csv_type + '.csv'), 'r', encoding='utf-8-sig') as myfile:
                reader = csv.DictReader(myfile)
                return list(reader)
        else:
            return "path is incorrect"

    @staticmethod
    def read_file_user(path):
        with open(path, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            return list(reader)

    def write_file(self, info, mode="a"):
        if isinstance(info, dict):
            fields = info.keys()
            info = [info]
            with open(os.path.join(self.dirName, self.csv_type + '.csv'), mode, encoding='utf-8-sig') as myfile:
                writer = csv.DictWriter(myfile, fieldnames=fields)
                if myfile.tell() == 0:
                    writer.writeheader()
                writer.writerows(info)
        elif isinstance(info, list):
            if len(info) != 0:
                fields = info[0].keys()
                with open(os.path.join(self.dirName, self.csv_type + '.csv'), mode, encoding='utf-8-sig') as myfile:
                    writer = csv.DictWriter(myfile, fieldnames=fields)
                    if myfile.tell() == 0:
                        writer.writeheader()
                    writer.writerows(info)
            else:
                if self.csv_type == 'Inbox':
                    self.write_new_file_inbox()
                else:
                    self.write_new_file()

    @staticmethod
    def write_file_user(path, info, mode="a"):
        if isinstance(info, dict):
            fields = info.keys()
            info = [info]

        elif isinstance(info, list):
            fields = info[0].keys()

        with open(path, mode, encoding='utf-8-sig') as myfile:
            writer = csv.DictWriter(myfile, fieldnames=fields)
            if myfile.tell() == 0:
                writer.writeheader()
            writer.writerows(info)

    def write_new_file(self):
        with open(os.path.join(self.dirName, self.csv_type + '.csv'), "w", encoding='utf-8-sig') as f:
            fieldnames = ['id', 'username', 'message']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()

    def write_new_file_inbox(self):
        with open(os.path.join(self.dirName, self.csv_type + '.csv'), "w", encoding='utf-8-sig') as f:
            fieldnames = ['id', 'username', 'message', 'readMessage']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()

    # def edit_row(self, new_info):
    #     all_rows = self.read_file()
    #     df = pd.DataFrame(all_rows)
    #     final_rows = []
    #     for row in all_rows:
    #         if row['id'] == new_info['id']:
    #             row = new_info
    #         final_rows.append(row)
    #     self.write_file(final_rows, mode="w")

    def delete_row(self, id):
        all_rows = self.read_file()
        df = pd.DataFrame(all_rows)
        data_with_index = df.set_index('id')
        data_with_index.head()
        data_with_index = data_with_index.drop(id)
        data_with_index.reset_index(inplace=True)
        self.write_file(data_with_index.to_dict('records'), mode='w')
