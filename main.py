import argparse
import sys

def parse_medal_count(value):
    return int(value) if value.isdigit() else 0

def process_data(data_file):
    results = []
    data_file = "Olympic Athletes - athlete_events.tsv"

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

def output_medals(results, country, year, output_file=None):
    output_text = ""
    bronze = 0
    silver = 0
    gold = 0
    for row in results:
        if (row["Team"] == country) and int(row["Year"]) == year:
            if row["Medal"] == "Gold":
                gold+=1
            elif row["Medal"] == "Silver":
                silver+=1
            elif row["Medal"] == "Bronze":
                bronze+=1
            output_text = (f"Country: {row['Team']}, Medals: {gold} gold, {silver} silver, {bronze} bronze\n")

    if not output_text:
        output_text = "No data for this country and year.\n"
    if output_file:
        with open(output_file, "w", encoding="utf-8") as file:
            file.write(output_text)
    else:
        print(output_text)

def output_total(results, year, output_file=None):
    medal_counts = {}

    for row in results:
        if int(row["Year"]) == year:
            country = row["Team"]
            if country not in medal_counts:
                medal_counts[country] = {"Gold": 0, "Silver": 0, "Bronze": 0}
            if row["Medal"] == "Gold":
                medal_counts[country]["Gold"] += 1
            elif row["Medal"] == "Silver":
                medal_counts[country]["Silver"] += 1
            elif row["Medal"] == "Bronze":
                medal_counts[country]["Bronze"] += 1

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
def output_overall(results, countries, output_file=None):
    country_medal_years = {}

    for row in results:
        country = row["Team"]
        if country in countries:
            year = int(row["Year"])
            total_medals = int(row["Gold"]) + int(row["Silver"]) + int(row["Bronze"])

            if country not in country_medal_years:
                country_medal_years[country] = {}
            if year not in country_medal_years[country]:
                country_medal_years[country][year] = 0
            if medal_type in ["Gold", "Silver", "Bronze"]:
                country_medal_years[country][year] += 1

    output_text = ""
    for country in countries:
        if country in country_medal_years:
            best_year = None
            max_medals = 0
            for year, medals in country_medal_years[country].items():
                if medals > max_medals:
                    best_year = year
                    max_medals = medals
            output_text += f"{country}: {best_year} year, {max_medals} medals\n"
        else:
            output_text += f"{country}: has no data.\n"
    if output_file:
        with open(output_file, "w", encoding="utf-8") as file:
            file.write(output_text)
    else:
        print(output_text)
def output_interactive(results):
    print("Interactive mode activated. Enter a country name (or 'exit' to quit).")
    while True:
        country = input("Enter a country (or 'exit' to quit): ")
        if country.lower() == 'exit':
            break
        country_data = [row for row in results if row["Team"] == country]

        if not country_data:
            print("No data found for this country.")
            continue

        country_data = [row for row in results if "Team" in row and country in row["Team"]]
        if not country_data:
            print(f"No data found for country '{country}'.")
            continue

        country_data = [row for row in country_data if "Year" in row and row["Year"].isdigit()]
        if not country_data:
            print(f"No valid data found for country '{country}'.")
            continue
        first_participation = min(country_data, key=lambda x: int(x["Year"]))
        print(f"First participation: {first_participation['Year']} in {first_participation['City']}")
        medal_counts = {}
        for row in country_data:
            year = int(row["Year"])
            medal_type = row["Medal"]
            if year not in medal_counts:
                medal_counts[year] = {"Gold": 0, "Silver": 0, "Bronze": 0}
            if medal_type and medal_type in ["Gold", "Silver", "Bronze"]:
                medal_counts[year][medal_type] += 1

        most_successful_year = None
        most_medals = 0
        least_successful_year = None
        least_medals = float("inf")

        for year, counts in medal_counts.items():
            total_medals = sum(counts.values())
            if total_medals > most_medals:
                most_medals = total_medals
                most_successful_year = year
            if total_medals < least_medals:
                least_medals = total_medals
                least_successful_year = year

        if most_successful_year is not None:
            print(f"Most successful Olympics: {most_successful_year} with {most_medals} medals")
        if least_successful_year is not None:
            print(f"Least successful Olympics: {least_successful_year} with {least_medals} medals")

        total_gold = sum(counts["Gold"] for counts in medal_counts.values())
        total_silver = sum(counts["Silver"] for counts in medal_counts.values())
        total_bronze = sum(counts["Bronze"] for counts in medal_counts.values())
        num_olympics = len(medal_counts)

        avg_gold = total_gold / num_olympics if num_olympics > 0 else 0
        avg_silver = total_silver / num_olympics if num_olympics > 0 else 0
        avg_bronze = total_bronze / num_olympics if num_olympics > 0 else 0

        print(f"Average medals per Olympics: Gold: {avg_gold:.2f}, Silver: {avg_silver:.2f}, Bronze: {avg_bronze:.2f}")
        print()

def main():
    parser = argparse.ArgumentParser(description="Olympic medals")
    parser.add_argument('data_file', help="Path to tsv data file")
    parser.add_argument("-medals", action='store_true', help="Command not in list")
    parser.add_argument("-overall", action='store_true', help="Command not in list")
    parser.add_argument("-total", type=int, help="Calculate total medals for a specific year")
    parser.add_argument("-interactive",  action='store_true', help="Start interactive mode")
    parser.add_argument("args", nargs="*", help="Arguments for the command")
    parser.add_argument("Olympic Athletes - athlete_events.tsv", nargs='?', default=None, help="Path to tsv data file")
    args = parser.parse_args()

    results = process_data(args.data_file)

    if not args.data_file:
        print("Error: You must provide a path to the TSV data file.")
        sys.exit(1)

    if args.medals:
        if len(sys.argv) < 2:
            print("Not enough arguments for command -overall. "
              "Use: python olympics.py <data_file> -overall <country1> <country2> ... [-output <file>]")
            return
        country = sys.argv[2]
        year = int(sys.argv[3])
        output_file = sys.argv[4] if "-output" in sys.argv else None
        output_medals(results, country, year, output_file)
        
    elif args.total is not None:
        year = args.total
        output_file = args.args[0] if len(args.args) > 0 else None
        output_total(results, year, output_file)
        
    elif args.overall is not None:
        countries = args.args
        output_file = None
        if "-output" in countries:
            output_index = countries.index("-output")
            output_file = countries[output_index + 1]
            countries = countries[:output_index]
        output_overall(results, countries, output_file)
        
    elif args.interactive:
        print("Starting interactive mode...")
        if not args.data_file:
            print("Error: You must provide a data file for interactive mode.")
            sys.exit(1)
        output_interactive(results)
    else:
        print("No valid command provided. Use -h for help.")
        
main()
