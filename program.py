import csv
import sys

def parse_arguments(args):
    if len(args) < 3:
        raise ValueError("Недостатньо аргументів. Мінімальна кількість: 3 (файл, команда, країна/рік).")
    
    file_path = args[1]
    command = args[2]
    
    if command == "-medals":
        if len(args) < 5:
            raise ValueError("Для -medals необхідно вказати країну та рік.")
        country = args[3]
        year = args[4]
        output_file = args[6] if len(args) > 6 and args[5] == "-output" else None
        return file_path, command, country, year, output_file
    
    elif command == "-total":
        if len(args) < 4:
            raise ValueError("Для команди -total необхідно вказати рік.")
        year = args[3]
        return file_path, command, None, year, None
    elif command == "-overall":
        if len(args) < 4:
            raise ValueError("Для -overall необхідно вказати щонайменше одну країну.")
        countries = args[3:]
        return file_path, command, countries, None, None
    elif command == "-interactive":
        return file_path, command, None, None, None
    else:
        raise ValueError(f"Trouble with: {command}")

def read_csv(file_path):
    with open(file_path, encoding="utf-8") as f:
        sample = f.read(1024)
        delimiter = '\t' if '\t' in sample else ','
        f.seek(0)
        reader = csv.DictReader(f, delimiter=delimiter)
        data = list(reader)
        if not data:
            raise ValueError("Trouble with file")
        return data

def medals_per_country(data, country, year):
    filtered_data = [
        row for row in data 
        if (row.get("Team") == country or row.get("NOC") == country) 
        and row.get("Year") == year 
        and row.get("Medal") != "NA"
    ]
    filtered_data.sort(key=lambda x: (x["Name"], x["Event"]))

    summary = {"Gold": 0, "Silver": 0, "Bronze": 0}
    for row in filtered_data:
        summary[row["Medal"]] += 1

    return filtered_data[:10], summary

def total_medals_by_year(data, year):
    filtered_data = [row for row in data if row.get("Year") == year and row.get("Medal") != "NA"]
    summary = {}
    for row in filtered_data:
        team = row.get("Team", "Unknown")
        if team not in summary:
            summary[team] = {"Gold": 0, "Silver": 0, "Bronze": 0}
        summary[team][row["Medal"]] += 1
    return summary

def overall_medals_by_country(data, countries):
    result = {}
    for country in countries:
        country_data = [ row for row in data if (row.get("Team")== country or row.get("NOC") == country) and row.get("Medal") != "NA"]
        yearly_medals = {}

        for row in country_data:
            year = row.get("Year")
            if year not in yearly_medals:
                yearly_medals[year] = 0
            yearly_medals[year] += 1

        if yearly_medals:
            best_year = max(yearly_medals, key=yearly_medals.get)
            result[country] = best_year, yearly_medals[best_year]
        else:
            result[country] = 0, 0

    return result

def interactive_mode(data):
    print("Інтерактивний режим активовано.")
    print("Введіть назву або код країни для отримання статистики, або 'exit' для виходу.")
    while True:
        country = input("Країна (назва або код): ").strip()
        if country.lower() == "exit":
            print("Вихід з інтерактивного режиму.")
            break

        country_data = [row for row in data if row.get("Team") == country or row.get("NOC") == country]
        if not country_data:
            print(f"Дані для країни '{country}' не знайдено.")
            continue

        first_participation = min(country_data, key=lambda x: int(x["Year"]))
        first_year, first_city = first_participation["Year"], first_participation["City"]

        medal_stats = {}

        for row in country_data:
            year = row["Year"]
            if year not in medal_stats:
                medal_stats[year] = {"Gold": 0, "Silver": 0, "Bronze": 0}
            if row["Medal"] != "NA":
                medal_stats[year][row["Medal"]] += 1

        most_successful = max(medal_stats.items(), key=lambda x: sum(x[1].values()))
        least_successful = min(medal_stats.items(), key=lambda x: sum(x[1].values()))

        total_medals = {"Gold": 0, "Silver": 0, "Bronze": 0}
        for stats in medal_stats.values():
            for medal, count in stats.items():
                total_medals[medal] += count

        avg_medals = {medal: count / len(medal_stats) for medal, count in total_medals.items()}

        print(f"\nКраїна: {country}")
        print(f"Перша участь: {first_year}, {first_city}")
        print(f"Найуспішніший рік: {most_successful[0]} (медалей: {sum(most_successful[1].values())})")
        print(f"Найневдаліший рік: {least_successful[0]} (медалей: {sum(least_successful[1].values())})")
        print(
            f"Середня кількість медалей: Gold: {avg_medals['Gold']:.2f}, Silver: {avg_medals['Silver']:.2f}, Bronze: {avg_medals['Bronze']:.2f}\n")


def save_to_file(output_file, content):
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(content)

def main():
    try:
        args = sys.argv
        file_path, command, country, year, output_file = parse_arguments(args)
        data = read_csv(file_path)
        
        if command == "-medals":
            medalists, summary = medals_per_country(data, country, year)
            result = "Медалісти:\n"
            result += "\n".join([f"{row['Name']} - {row['Event']} - {row['Medal']}" for row in medalists])
            result += "\n\nСумарна кількість медалей:\n"
            result += f"Gold: {summary['Gold']}, Silver: {summary['Silver']}, Bronze: {summary['Bronze']}\n"
            print(result)
            if output_file:
                save_to_file(output_file, result)

        elif command == "-total":
            summary = total_medals_by_year(data, year)
            result = "Результати за країнами:\n"
            result += "\n".join([f"{team} - Gold: {medals['Gold']}, Silver: {medals['Silver']}, Bronze: {medals['Bronze']}" for team, medals in summary.items()])

            print(result)

        elif command == "-overall":
            summary = overall_medals_by_country(data, country)
            result = "Результати для кожної країни:\n"
            result += "\n".join([f"{country}: {year} - {medals}" for country, (year, medals) in summary.items()])
            print(result)

         elif command == "-interactive":

            interactive_mode(data)

    except Exception as e:
        print(f"Trouble: {e}")

if __name__== "__main__":
    main()
