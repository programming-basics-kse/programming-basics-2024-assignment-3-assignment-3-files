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

def output_medals(results, country, year, output_file=None):
    output_text = ""
    for row in results:
        if (row["Team"] == country) and int(row["Year"]) == year:
            output_text += (f"Country: {row['Team']}, Medals: {row['Gold']} gold, {row['Silver']} silver, "
                            f"{row['Bronze']} bronze\n")

    if not output_text:
        output_text = "No data for this country and year.\n"

    if output_file:
        with open(output_file, "w", encoding="utf-8") as file:
            file.write(output_text)
    else:
        print(output_text)

def output_interactive(results):
    while True:
        country = input("Enter a country (or 'exit' to quit): ")
        if country.lower() == 'exit':
            break
        country_data = [row for row in results if row["Team"] == country]

        if not country_data:
            print("No data found for this country.")
            continue

        first_participation = None
        for row in country_data:
            if first_participation is None or int(row["Year"]) < int(first_participation["Year"]):
                first_participation = row
        print(f"First participation: {first_participation['Year']} in {first_participation['City']}")

        most_successful_olympics = None
        for row in country_data:
            total_medals = int(row["Gold"]) + int(row["Silver"]) + int(row["Bronze"])
            if most_successful_olympics is None or total_medals > (int(most_successful_olympics["Gold"]) +
                                                                   int(most_successful_olympics["Silver"]) +
                                                                   int(most_successful_olympics["Bronze"])):
                most_successful_olympics = row
        total_medals = int(most_successful_olympics["Gold"]) + int(most_successful_olympics["Silver"]) + int(
            most_successful_olympics["Bronze"])
        print(f"Most successful Olympics: {most_successful_olympics['Year']} with {total_medals} medals")

        least_successful_olympics = None
        for row in country_data:
            total_medals = int(row["Gold"]) + int(row["Silver"]) + int(row["Bronze"])
            if least_successful_olympics is None or total_medals < (int(least_successful_olympics["Gold"]) +
                                                                    int(least_successful_olympics["Silver"]) +
                                                                    int(least_successful_olympics["Bronze"])):
                least_successful_olympics = row
        total_medals = int(least_successful_olympics["Gold"]) + int(least_successful_olympics["Silver"]) + int(
            least_successful_olympics["Bronze"])
        print(f"Least successful Olympics: {least_successful_olympics['Year']} with {total_medals} medals")

        total_gold = 0
        total_silver = 0
        total_bronze = 0
        num_olympics = len(country_data)

        for row in country_data:
            total_gold += int(row["Gold"])
            total_silver += int(row["Silver"])
            total_bronze += int(row["Bronze"])

        avg_gold = total_gold / num_olympics
        avg_silver = total_silver / num_olympics
        avg_bronze = total_bronze / num_olympics

        print(f"Average medals per Olympics: Gold: {avg_gold:.2f}, Silver: {avg_silver:.2f}, Bronze: {avg_bronze:.2f}")
        print()

def main():
    if len(sys.argv) < 3:
        print("Not enough arguments. Use: python olympics.py <data_file> <command> [...args]")
        return
    data_file = sys.argv[1]
    command = sys.argv[2]
    results = process_data(data_file)

    if command == "-medals":
        if len(sys.argv) < 5:
            print("Not enough arguments for command -medals. "
                  "Use: python olympics.py <data_file> -medals <country> <year> [-output <file>]")
            return
        country = sys.argv[3]
        year = int(sys.argv[4])
        output_file = sys.argv[6] \
            if "-output" in sys.argv \
            else None
        output_medals(results, country, year, output_file)
    elif command == "-interactive":
        output_interactive(results)

    else:
        print(f"Invalid command: {command}")
