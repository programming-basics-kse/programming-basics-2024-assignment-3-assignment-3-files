import sys

def output_total(results, year, output_file=None):
    medal_counts = {}

    for row in results:
        if int(row["Year"]) == year:
            country = row["Team"]
            if country not in medal_counts:
                medal_counts[country] = {"Gold": 0, "Silver": 0, "Bronze": 0}
            medal_counts[country]["Gold"] += int(row["Gold"])
            medal_counts[country]["Silver"] += int(row["Silver"])
            medal_counts[country]["Bronze"] += int(row["Bronze"])

    output_text = ""
    for country, counts in medal_counts.items():
        output_text += (f"{country} - {counts['Gold']} gold - {counts['Silver']} silver"
                        f" - {counts['Bronze']} bronze\n")

    if not output_text:
        output_text = "No data for this year.\n"

    if output_file:
        with open(output_file, "w", encoding="utf-8") as file:
            file.write(output_text)
    else:
        print(output_text)


def main():
    if len(sys.argv) < 3:
        print("Not enough arguments. Use: python olympics.py <data_file> <command> [...args]")
        return

    data_file = sys.argv[1]
    command = sys.argv[2]
    results = process_data(data_file)
    if command == "-total":
        if len(sys.argv) < 4:
            print("Not enough arguments for command -total. "
              "Use: python olympics.py <data_file> -total <year> [-output <file>]")
        return
    year = int(sys.argv[3])
    output_file = sys.argv[5] \
        if ("-output"
            in sys.argv) else None
    output_total(results, year, output_file)
