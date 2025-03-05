import csv
import os

class CsvUser:
    def __init__(self, file_name):
        self.filename = file_name

    def read_csv(self):
        if not os.path.exists(self.filename):
            print(f"Создаю {self.filename}")
            with open(self.filename, "w") as file:
                pass
        with open(self.filename, mode="r", newline="") as file:
            reader = csv.reader(file)
            return list(reader)

    def write_csv(self, data):
        with open(self.filename, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(data)