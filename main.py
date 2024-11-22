import csv
import argparse
import os.path

parser = argparse.ArgumentParser()

parser.add_argument("dataset_filepath", type=str, help="Dataset file filepath")
parser.add_argument("-medals",  nargs="+" ,required=True, help="Medals that receive: [TEAM + YEAR]")
parser.add_argument("-output", help="Receive file name to output results")

args = vars(parser.parse_args())
print(args)
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

def get_medals(noc:str, year:int):
    noc = noc.upper().strip()
    wrong_noc = True
    wrong_year = True
    winners = []
    medals = {"Gold": 0, "Silver": 0, "Bronze": 0}
    for row in rows_file:
        if row[header_file["NOC"]] != noc and row[header_file["Team"]].upper() != noc:
            continue
        wrong_noc = False
        if row[header_file["Year"]] == str(year):
            wrong_year = False
            try:
                medals[row[header_file["Medal"]]] += 1
                if not row[header_file["Name"]] in winners:
                    winner = {"Name": row[header_file["Name"]], "Discipline": row[header_file["Event"]], "Medal": row[header_file["Medal"]]}
                    winners.append(winner)
            except KeyError:
                continue
    if wrong_noc:
        print(f"{"\033[91m"}Seems like the program could not understand what country did you mean.\n{"\033[93m"}You should try using NOC of the country you want.\n")
    if wrong_year:
        print(f"{"\033[91m"}Seems like Olympics did not take place the year you entered.\n{"\033[93m"}You should try double checking that you entered it correctly.\n")
    if not wrong_noc and not wrong_year:
        for winner in winners[:10]:
            print(f"{winner["Name"]} - {winner["Discipline"]} - {winner["Medal"]}")
        print(f"Gold: {medals["Gold"]}")
        print(f"Silver: {medals["Silver"]}")
        print(f"Bronze: {medals["Bronze"]}")

get_medals("Ukraine", 2003)
