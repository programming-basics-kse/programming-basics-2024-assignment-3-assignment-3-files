import csv
import argparse
import os.path

parser = argparse.ArgumentParser()

parser.add_argument("dataset_filepath", type=str, help="Dataset file filepath")
parser.add_argument("-medals",  nargs="+" ,required=True, help="Medals that receive: [TEAM + YEAR]")
parser.add_argument("-output", help="Receive file name to output results")

args = vars(parser.parse_args())
print(args)
# dataset_filepath = valid_file_path( args["dataset_filepath"] )
dataset_filepath = args["dataset_filepath"]

if os.path.exists(dataset_filepath) == False:
    print(f'There is no such file!')
    pass

medals_list = args["medals"]
if len(medals_list) < 2:
    print(f"You have to enter a country and the year!")
    pass

try:
    print(medals_list)
    year = int(medals_list[-1])
    team = " ".join(medals_list[:-1])
    print(f"Year: {year}, team: {team}")
except Exception:
    print(f'The entered year is not a valid number')
    pass


file_to_output = args["output"]
# todo validation to output file

def get_header_indexes(header_line):
    dictionary = dict()
    for index, elem in enumerate(header_line):
        dictionary[elem] = index
    return dictionary

with open(dataset_filepath, 'rt') as file:
    file_csv_reader = csv.reader(file, delimiter=',')
    rows_file = []
    header_file = get_header_indexes(next(file_csv_reader))
    for row in file:
        rows_file.append(row)

with open("noc_regions.csv", 'rt') as noc_regions_csv_file:
    noc_regions_csv_reader = csv.reader(noc_regions_csv_file, delimiter=',')
    rows_noc_regions = []
    header_noc_regions = get_header_indexes(next(noc_regions_csv_reader))
    for row in noc_regions_csv_reader:
        rows_noc_regions.append(row)