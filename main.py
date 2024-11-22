import csv
import argparse
import os.path

parser = argparse.ArgumentParser()

parser.add_argument("dataset_filepath", type=str, help="Dataset file filepath")
parser.add_argument("-medals",  nargs="+", help="Medals that receive: [TEAM + YEAR]")
parser.add_argument("-output", help="Receive file name to output results")
parser.add_argument("-total", type=int, help="Receive year to total func")
parser.add_argument("-overall", nargs="+", help="Receive teams for overall medals")

args = vars(parser.parse_args())
#
print(args)

dataset_filepath = args["dataset_filepath"]

if os.path.exists(dataset_filepath) == False:
    print(f'There is no such file!')
    # return False

def get_header_indexes(header_line):
    dictionary = dict()
    for index, elem in enumerate(header_line):
        dictionary[elem] = index
    return dictionary

with open(dataset_filepath, 'rt') as file:
    file_csv_reader = csv.reader(file, delimiter=',')
    rows_file = []
    header_file = get_header_indexes(next(file_csv_reader))
    for row in file_csv_reader:
        rows_file.append(row)

def get_medals(noc:str, year:int):
    noc = noc.upper().strip()
    wrong_noc = True
    wrong_year = True
    winners = []
    medals = {"Gold": 0, "Silver": 0, "Bronze": 0}
    for row in rows_file:
        if row[header_file["NOC"]] != noc and row[header_file["Team"]].upper() != noc:
            if row[header_file["Year"]] == str(year):
                wrong_year = False
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



medals_list = args["medals"]
if medals_list != None:
    if len(medals_list) < 2:
        print(f"To use command 'medals' you have to enter the country and the year!")
        # pass
    else:
        try:
            #
            print(medals_list)
            year_medals_arg = int(medals_list[-1])
            team_medals_arg = " ".join(medals_list[:-1])
            #
            print(f"Year: {year_medals_arg}, team: {team_medals_arg}")
            get_medals(team_medals_arg, year_medals_arg)
        except Exception:
            print(f"To use command 'medals' the entered year must be a valid number")
            # pass

totalYear = args["total"]
if totalYear != None:
    pass
    # call function total()

overall = args["overall"]
print(overall)
if overall != None:
    pass
    # call function
    # overallTeams = []
    # for elem in overall:
    #     overallTeams.append(elem)
    # print(overallTeams)


# file_to_output = args["output"]
# # todo validation to output file in the end of the proj