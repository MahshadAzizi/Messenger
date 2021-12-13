import csv
import os


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

    def write_file(self, info, mode="a"):
        if isinstance(info, dict):
            if self.check_unique_id(info["id"]):
                return "id already exists"
            fields = info.keys()
            info = [info]
        elif isinstance(info, list):
            fields = info[0].keys()
        with open(self.file_path, mode, encoding='utf-8-sig') as myfile:
            writer = csv.DictWriter(myfile, fieldnames=fields)
            if myfile.tell() == 0:
                writer.writeheader()
            writer.writerows(info)

    def edit_row(self, new_info):
        all_rows = self.read_file()
        final_rows = []
        for row in all_rows:
            if row["id"] == str(new_info["id"]):
                row = new_info
            final_rows.append(row)
        self.write_file(final_rows, mode="w")

    def check_unique_id(self, id):
        all_rows = self.read_file()
        for row in all_rows:
            if row["id"] == str(id):
                return True
        return False

    def delete_row(self, id):
        all_rows = self.read_file()
        final_rows = []
        for row in all_rows:
            if row["id"] == str(id):
                continue
            final_rows.append(row)
        self.write_file(final_rows, mode="w")
