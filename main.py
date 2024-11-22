import csv

def get_header_indexes(header_line):
    dictionary = dict()
    for index, elem in enumerate(header_line):
        dictionary[elem] = index
    return dictionary

with open("athlete_events.csv", 'rt') as athlete_events_csv_file:
    athlete_events_csv_reader = csv.reader(athlete_events_csv_file, delimiter=',')
    rows_athletes_events = []
    header_athletes_events = get_header_indexes(next(athlete_events_csv_reader))
    for row in athlete_events_csv_reader:
        rows_athletes_events.append(row)

with open("noc_regions.csv", 'rt') as noc_regions_csv_file:
    noc_regions_csv_reader = csv.reader(noc_regions_csv_file, delimiter=',')
    rows_noc_regions = []
    header_noc_regions = get_header_indexes(next(noc_regions_csv_reader))
    for row in noc_regions_csv_reader:
        rows_noc_regions.append(row)

def get_medals(noc:str, year:int):
    noc = noc.upper().strip()
    wrong_noc = True
    wrong_year = True
    winners = []
    medals = {"Gold": 0, "Silver": 0, "Bronze": 0}
    for row in rows_athletes_events:
        if row[header_athletes_events["NOC"]] != noc and row[header_athletes_events["Team"]].upper() != noc:
            continue
        wrong_noc = False
        if row[header_athletes_events["Year"]] == str(year):
            wrong_year = False
            try:
                medals[row[header_athletes_events["Medal"]]] += 1
                if not row[header_athletes_events["Name"]] in winners:
                    winner = {"Name": row[header_athletes_events["Name"]], "Discipline": row[header_athletes_events["Event"]], "Medal": row[header_athletes_events["Medal"]]}
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
