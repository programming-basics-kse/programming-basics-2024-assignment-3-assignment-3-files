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
#
# print(header_athletes_events)
# print(header_noc_regions)

def get_medals(noc:str, year:int):
    noc = noc.upper().strip()
    winners = []
    medals = {"Gold": 0, "Silver": 0, "Bronze": 0}
    counter = 0
    for row in rows_athletes_events:
        if row[header_athletes_events["NOC"]] == noc and row[header_athletes_events["Year"]] == str(year):
            try:
                medals[row[header_athletes_events["Medal"]]] += 1
                if not row[header_athletes_events["Name"]] in winners:
                    winners.append(row[header_athletes_events["Name"]])
            except KeyError:
                continue
    print(medals)
    print(winners[:10])
get_medals("USA", 2004)
