import csv
import argparse
# parser = argparse.ArgumentParser("Main parser")
# parser.add_argument("data_file", type=str, help="Data files address")
# parser.add_argument("--medals", "-m", help="Medals", required=True)
#
# args = parser.parse_args()
# print(args)

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

print(header_athletes_events)
print(header_noc_regions)