import csv

with open("athlete_events.csv", 'rt') as athlete_events_csv_file:
    athlete_events_csv_reader = csv.reader(athlete_events_csv_file, delimiter=',')
    rows_athletes_events = []
    header_athletes_events = next(athlete_events_csv_reader)
    for row in athlete_events_csv_reader:
        rows_athletes_events.append(row)

with open("noc_regions.csv", 'rt') as noc_regions_csv_file:
    noc_regions_csv_reader = csv.reader(noc_regions_csv_file, delimiter=',')
    rows_noc_regions = []
    header_noc_regions = next(noc_regions_csv_reader)
    for row in noc_regions_csv_reader:
        rows_noc_regions.append(row)

def get_header_indexes(header_line, dictionary):
    dictionary = dict()
    for elem in header_line:
        elem_index = header_line.index(elem)
        dictionary[elem] = elem_index
    return dictionary

dict_header_index_athletes_events = get_header_indexes(header_athletes_events, "dict_header_index_athletes_events")
dict_header_index_noc_regions = get_header_indexes(header_noc_regions, "dict_header_index_noc_regions")
print(dict_header_index_athletes_events)
print(dict_header_index_noc_regions)