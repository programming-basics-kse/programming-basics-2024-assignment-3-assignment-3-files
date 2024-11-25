import os
import csv
def get_header_indexes(header_line):
    dictionary = dict()
    for index, elem in enumerate(header_line):
        dictionary[elem] = index
    return dictionary
with open("noc_regions.csv", 'rt') as file:
    file_csv_reader = csv.reader(file, delimiter=',')
    rows_file = []
    header_file = get_header_indexes(next(file_csv_reader))
    for row in file_csv_reader:
        rows_file.append(row)

class MyClassForArguments:
    def __init__(self, argumentValue, other=''):
        self.value = argumentValue
        self.other = other


    def check_input_file_existing(self):
        if os.path.exists(self.value):
            return self.value

    # def check_output_file_existing(self):
    #     if not self.value is None:
    #         if os.path.exists(self.value):
    #             print(f"File to output is exist! Result will be written in the {self.value} file!")
    #             return self.value
    #         else:
    #             print(f"Your file to output is not exist! {self.value} will be created to output!")

    def check_medals(self):
        if not self.value is None:
            if len(self.value) < 2:
                print(f"To use command 'medals' you have to enter the country and the year!")
            else:
                try:
                    year = int( self.value[-1] )
                    team = " ".join( self.value[:-1] )
                    return year, team
                except Exception:
                    print(f"To use command 'medals' the entered year must be a valid number!")


    def check_total(self):
        if not self.value is None:
            try:
                return int(self.value)
            except ValueError:
                print(f"To use command 'total' the entered year must be a valid number!")


    def check_interactive(self):
        if not self.value is None:
            return self.value


    def check_overall(self):
        if not self.value is None:
            correct_countries = []
            i = 0
            while i < len(self.value):
                self.value[i] = self.value[i].title()
                i += 1

            i = 0
            while i < len(self.value):
                for  row in rows_file:
                    if self.value[i] == row[header_file["NOC"]].title() or self.value[i] == row[header_file["region"]] or self.value[i] == row[header_file["notes"]]:
                        correct_countries.append(self.value[i])
                        break

                else:
                    if (i + 1) < len(self.value):
                        for row in rows_file:
                            if self.value[i+1] == row[header_file["NOC"]].title() or self.value[i+1] == row[header_file["region"]]:
                                break
                        else:
                            new = self.value[i] + " " + self.value[i + 1]
                            self.value[i + 1] = new
                i += 1

            return self.value