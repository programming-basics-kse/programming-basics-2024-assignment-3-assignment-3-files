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

            country_medal_years[country][year] += total_medals

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

    if command == "-overall":
        if len(sys.argv) < 4:
            print("Not enough arguments for command -overall. "
              "Use: python olympics.py <data_file> -overall <country1> <country2> ... [-output <file>]")
        return
        countries = sys.argv[3:]
        if "-output" in countries:
            output_index = countries.index("-output")
            output_file = countries[output_index + 1]
            countries = countries[:output_index]
        else:
            output_file = None
        output_overall(results, countries, output_file)
    else:
        print(f"Invalid command: {command}")

    main()


