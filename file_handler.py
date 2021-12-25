import csv
import os
import pandas as pd


class FileHandler:
    def __init__(self, file_path):
        self.file_path = file_path

    def read_file(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r', encoding='utf-8-sig') as myfile:
                reader = csv.DictReader(myfile)
                return list(reader)
        else:
            return "path is incorrect"

    @staticmethod
    def read_file_user(dirName, csv_type):
        with open(os.path.join(dirName, csv_type + '.csv'), 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            return list(reader)

    def write_file(self, info, mode="a"):
        if isinstance(info, dict):
            fields = info.keys()
            info = [info]
        elif isinstance(info, list):
            # if len(info) != 0:
            fields = info[0].keys()
            # else:
            #     return self.read_file()
        with open(self.file_path, mode, encoding='utf-8-sig') as myfile:
            writer = csv.DictWriter(myfile, fieldnames=fields)
            if myfile.tell() == 0:
                writer.writeheader()
            writer.writerows(info)

    @staticmethod
    def write_new_file(dirName, csv_type):
        with open(os.path.join(dirName, csv_type + '.csv'), "w", encoding='utf-8-sig') as f:
            fieldnames = ['id', 'username', 'message']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()

    @staticmethod
    def write_new_file_inbox(dirName, csv_type):
        with open(os.path.join(dirName, csv_type + '.csv'), "w", encoding='utf-8-sig') as f:
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
        # update_df = df.drop(id)
        # print(data_with_index.to_dict('records'))
        # print(df)

        # final_rows = []
        # for row in all_row:
        #     if row['id'] == str(id):
        #         continue
        #     final_rows.append(row)
        # self.write_file(final_rows, mode="w")
