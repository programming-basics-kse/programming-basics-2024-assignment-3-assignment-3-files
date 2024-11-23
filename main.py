import csv
import argparse
from classes import MyClassForArguments

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("dataset_filepath", type=str, help="Dataset file filepath")
    parser.add_argument("-medals", nargs="+", help="Medals that receive: [TEAM + YEAR]")
    parser.add_argument("-output", help="Receive file name to output results")
    parser.add_argument("-total", type=int, help="Receive year to total func")
    parser.add_argument("-overall", nargs="+", help="Receive teams for overall medals")
    #todo add -interactive argument (function for it is almost done)

    args = vars(parser.parse_args())
    #
    print(args)

    dataset_filepath = MyClassForArguments(args["dataset_filepath"])

    if dataset_filepath.check_input_file_existing() == False:
        print(f"File {dataset_filepath.value} does not exist!")
        print("PROGRAM STOPPED")
        return
        # done STOP THE PROGRAM HERE !!!!

    with open(dataset_filepath.value, 'rt') as file:
        file_csv_reader = csv.reader(file, delimiter=',')
        rows_file = []
        header_file = get_header_indexes(next(file_csv_reader))
        for row in file_csv_reader:
            rows_file.append(row)

    medals_list = args["medals"]
    if not medals_list is None:
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
                get_medals(team_medals_arg, year_medals_arg, rows_file, header_file)
            except Exception:
                print(f"To use command 'medals' the entered year must be a valid number")
                # pass

    totalYear = args["total"]
    if totalYear != None:
        # get_total(totalYear, rows_file, header_file)
        get_interactive(rows_file, header_file)  #added for testing REMOVE LATER!
    overall = args["overall"]

    if overall != None:
        pass
        # call function

    output_filepath = MyClassForArguments(args["output"])
    if output_filepath.check_output_file_existing() != False:
        pass
        # call function


def get_medals(noc: str, year: int, rows_file, header_file):
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
                    winner = {"Name": row[header_file["Name"]], "Discipline": row[header_file["Event"]],
                              "Medal": row[header_file["Medal"]]}
                    winners.append(winner)
            except KeyError:
                continue
    if wrong_noc:
        print(
            f"{"\033[91m"}Seems like the program could not understand what country did you mean.\n{"\033[93m"}You should try using NOC of the country you want.\n{"\033[0m"}")
    if wrong_year:
        print(
            f"{"\033[91m"}Seems like Olympics did not take place the year you entered.\n{"\033[93m"}You should try double checking that you entered it correctly.\n{"\033[0m"}")
    if not wrong_noc and not wrong_year:
        for winner in winners[:10]:
            print(f"{winner["Name"]} - {winner["Discipline"]} - {winner["Medal"]}")
        print(f"Gold: {medals["Gold"]}")
        print(f"Silver: {medals["Silver"]}")
        print(f"Bronze: {medals["Bronze"]}")

def get_total(year:int, rows_file, header_file):
    year = str(year).strip()
    wrong_year = True
    countries = dict()
    medals = {"Gold": 0, "Silver": 0, "Bronze": 0}

    for row in rows_file:
        if year == row[header_file["Year"]]:
            wrong_year = False
            if row[header_file["Medal"]] != "NA":
                team = str(row[header_file["Team"]]).split("-")[0]  #some countries have more than 1 team with only difference is "...-1" in the end e.g. "Germany-1"
                try:
                    countries[team][row[header_file["Medal"]]] += 1
                except KeyError:
                    countries[team] = dict(medals)
                    countries[team][row[header_file["Medal"]]] += 1

    if wrong_year:
        print(
            f"{"\033[91m"}Seems like Olympics did not take place the year you entered.\n{"\033[93m"}You should try double checking that you entered it correctly.\n")
        return
    for country in countries:
        print(f"{"\033[0m"}{country}: {"\033[1;93m"}Gold: {countries[country]["Gold"]}{"\033[0m"}, {"\033[0;37m"}Silver: {countries[country]["Silver"]}{"\033[0m"}, {"\033[0;33m"}Bronze: {countries[country]["Bronze"]}{"\033[0m"}.")

def get_interactive(rows_file, header_file):
    while True:
        print("Enter name or NOC of the country you want to get info about or 'exit'.")
        country_name = input("Country: ").strip().lower()
        if country_name == "exit":
            print("Stopping the program.")
            return
        wrong_country = True
        first_olymp = {"Year": 2077, "Season": 0,"City": 0}
        medals = {"Gold": 0, "Silver": 0, "Bronze": 0, "Overall": 0}
        medals_by_game = {"Overall": dict(medals)}

        for row in rows_file:
            if country_name == row[header_file["Team"]].lower() or country_name == row[header_file["NOC"]].lower():
                wrong_country = False
                try:
                    row_year = int(row[header_file["Year"]])
                except ValueError:
                    continue
                if int(first_olymp["Year"]) == row_year:
                    if first_olymp["Season"] == "Summer" and row[header_file["Season"]] == "Winter":
                        first_olymp["Season"] = "Winter"
                        first_olymp["City"] = row[header_file["City"]]
                elif int(first_olymp["Year"]) > row_year:
                    first_olymp["Season"] = row[header_file["Season"]]
                    first_olymp["Year"] = row_year
                    first_olymp["City"] = row[header_file["City"]]


        if wrong_country:
            print(f"{"\033[91m"}Seems like the program could not understand what country did you mean.\n{"\033[93m"}You should try using NOC of the country you want.\n{"\033[0m"}")
        else:
            print(first_olymp)


def get_header_indexes(header_line):
    dictionary = dict()
    for index, elem in enumerate(header_line):
        dictionary[elem] = index
    return dictionary

main()