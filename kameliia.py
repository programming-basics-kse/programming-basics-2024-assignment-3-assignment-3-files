import sys

def process_data(data_file):
    results = []
    data_file = "athlete_events.tsv"

    with open(data_file, "r", encoding="utf-8") as file:
        lines = file.readlines()
        headers = lines[0].strip().split("\t")
        for line in lines[1:]:
            values = line.strip().split("\t")
            row = {}
            for i in range(len(headers)):
                row[headers[i]] = values[i]
            results.append(row)

    return results

