import argparse


def read_file(file_name):
        with open(file_name, "r") as file:
            golova = file.readline().strip()
            data = [line.strip().split('\t') for line in file]
        return golova.split('\t'), data

def parse_arguments():
    parser = argparse.ArgumentParser(description="Медалісти з країн")
    parser.add_argument("-medals", type=int, help="Рік Олімпіади для медалістів")
    parser.add_argument("country", nargs='?', help="Країна")
    parser.add_argument("-output", type=str, help="Файл виведення результатів")
    parser.add_argument("-total", type=int, help="Загальний результат про країни даного року")
    parser.add_argument("-overall", nargs='*', help="Довільна кількість країн")
    parser.add_argument("-interactive", action="store_true", help="Інтерактивний режим")
    return parser.parse_args()


def calculate_total_medals(data, year_index, noc_index, medal_index, year):
    medal_count = {}
    for row in data:
        if len(row) > max(year_index, noc_index, medal_index) and row[year_index] and row[medal_index]:
            if int(row[year_index]) == year:
                country = row[noc_index]
                medal = row[medal_index]
                if medal in ['Gold', 'Silver', 'Bronze']:
                    if country not in medal_count:
                        medal_count[country] = {'Gold': 0, 'Silver': 0, 'Bronze': 0}
                    medal_count[country][medal] += 1
    return medal_count



def display_total_medals(medal_count):
    print("Країна-Золото-Срібло-Бронза")
    for country, medals in medal_count.items():
        print(f"{country}     {medals['Gold']}     {medals['Silver']}     {medals['Bronze']}")


def find_country_medalists(data, country, name_index, event_index, medal_index, noc_index):
    medalists = []
    medal_count = {'Gold': 0, 'Silver': 0, 'Bronze': 0}
    for row in data:
        if len(row) > max(name_index, event_index, medal_index, noc_index) and row[noc_index] == country:
            if row[medal_index] in medal_count:
                medalists.append(f"{row[name_index]}----{row[event_index]}-----{row[medal_index]}")
                medal_count[row[medal_index]] += 1
                if len(medalists) == 10:
                    break
    return medalists, medal_count



def display_medalists(medalists, medal_count, country, output_file=None):
    result = []
    if medalists:
        result.append("")
        result.append("")

        result.append("Перші 10 медалістів:")
        result.append("")

        result.append("\n".join(medalists))
        result.append("\nСумарна кількість медалей:")
        for medal_type in ['Gold', 'Silver', 'Bronze']:
            result.append(f"{medal_type}: {medal_count[medal_type]}")
    else:
        result.append(f"Не знайдено медалістів для {country}")
    result_output = "\n".join(result)
    print(result_output)
    if output_file:
        with open(output_file, "w") as file:
            file.write(result_output)


def calculate_overall(data, countries, noc_index, year_index, medal_index):
    country_data = {country: {} for country in countries}
    for row in data:
        if len(row) > max(noc_index, year_index, medal_index):
            country = row[noc_index]
            year = row[year_index]
            medal = row[medal_index]
            if country in countries and medal:
                if year not in country_data[country]:
                    country_data[country][year] = 0
                country_data[country][year] += 1
    results = []
    for country, years in country_data.items():
        if years:
            max_year = max(years, key=years.get)
            max_medals = years[max_year]
            results.append(f"{country}: {max_year} - {max_medals} медалей")
        else:
            results.append(f"{country}: таку країну не знайдено")
    return results


def interactive_mode(data, indices):
    print("")
    print("__Інтерактивний режим__")
    print("")
    while True:
        country = input("Введіть код країни або якщо вам потрібна інша функція 'exit': ")
        if country.lower() == 'exit':
            print("Вихід з інтерактивного режиму.")
            break

        medalists, medal_count = find_country_medalists(
            data, country, indices['Name'], indices['Event'], indices['Medal'], indices['NOC']
        )
        if medalists:
            first_uchiast = find_first_uchiast(data, country, indices['Year'], indices['City'], indices['NOC'])
            most_successful, least_successful, avg_medals = calculate_country_stats(data, country, indices)

            print(f"Перша участь: {first_uchiast}")
            print(f"Найуспішніша Олімпіада: {most_successful}")
            print(f"Найневдаліша Олімпіада: {least_successful}")
            print(f"Середня кількість медалей на Олімпіаді: {avg_medals}")
        else:
            print(f"Медалісти для країни '{country}' не знайдені.")


def find_first_uchiast(data, country, year_index, city_index, noc_index):
    for row in data:
        if row[noc_index] == country:
            return f"{row[year_index]}, {row[city_index]}"
    return "Дані не знайдені"


def calculate_country_stats(data, country, indices):
    medali_every_year = {}
    for row in data:
        if row[indices['NOC']] == country and row[indices['Medal']] in ['Gold', 'Silver', 'Bronze']:
            year = row[indices['Year']].strip()
            if year not in medali_every_year:
                medali_every_year[year] = {'Gold': 0, 'Silver': 0, 'Bronze': 0}
            medali_every_year[year][row[indices['Medal']]] += 1
    if not medali_every_year:
        return "Дані відсутні"

    max_year = max(medali_every_year, key=lambda y: sum(medali_every_year[y].values()))
    min_year = min(medali_every_year, key=lambda y: sum(medali_every_year[y].values()))
    total_medals = {'Gold': 0, 'Silver': 0, 'Bronze': 0}
    for year_medals in medali_every_year.values():
        for medal, count in year_medals.items():
            total_medals[medal] += count

    num_years = len(medali_every_year)
    avg_medals = {medal: total_medals[medal] / num_years for medal in ['Gold', 'Silver', 'Bronze']}

    return (
        f"{max_year} - {sum(medali_every_year[max_year].values())} медалей",
        f"{min_year} - {sum(medali_every_year[min_year].values())} медалей",
        f"Золото: {avg_medals['Gold']:}, Срібло: {avg_medals['Silver']:}, Бронза: {avg_medals['Bronze']:}"
    )


def main():
    args = parse_arguments()
    golova, data = read_file("Olympic Athletes - athlete_events.tsv")
    indices = {col: i for i, col in enumerate(golova)}

    if args.interactive:
        interactive_mode(data, indices)
    elif args.total is not None:
        medal_count = calculate_total_medals(data, indices['Year'], indices['NOC'], indices['Medal'], args.total)
        display_total_medals(medal_count)
    elif args.country:
        medalists, medal_count = find_country_medalists(
            data, args.country, indices['Name'], indices['Event'], indices['Medal'], indices['NOC']
        )
        display_medalists(medalists, medal_count, args.country, args.output)
    elif args.overall:
        results = calculate_overall(data, args.overall, indices['NOC'], indices['Year'], indices['Medal'])
        print("Результати для країн:")
        print("\n".join(results))

main()