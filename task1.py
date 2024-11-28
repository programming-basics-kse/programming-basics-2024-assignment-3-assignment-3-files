import argparse

medalists = []
medal_rahunok = {'Gold': 0, 'Silver': 0, 'Bronze': 0}

parser = argparse.ArgumentParser(description="Медалісти з країн")
parser.add_argument("-medals", type=int, help="Рік Олімпіади для медалістів")
parser.add_argument("country",nargs='?', help="Країна")
parser.add_argument("-output", type=str, help="Файл виведення результатів")
parser.add_argument("-total", type=int, help="Загальний результат про країни даного року")
args = parser.parse_args()

with open("Olympic Athletes - athlete_events.tsv", "r") as file:
    header = file.readline().strip()
    first_str = header.split('\t')

    name_index = first_str.index('Name')
    event_index = first_str.index('Event')
    medal_index = first_str.index('Medal')
    noc_index = first_str.index('NOC')
    year_index = first_str.index('Year')

    if args.total is not None:
        total_medals = {}

        for line in file:
            row = line.strip().split('\t')
            if int(row[year_index]) == args.total:
                country = row[noc_index]
                medal_type = row[medal_index]

                if medal_type in medal_rahunok:
                    if country not in total_medals:
                        total_medals[country] = {'Gold': 0, 'Silver': 0, 'Bronze': 0}
                    total_medals[country][medal_type] += 1

        result = []
        print("Країна-Золото-Срібло-Серебро")

        for country, medals in total_medals.items():
            result.append(f"{country}     {medals['Gold']}     {medals['Silver']}     {medals['Bronze']}")


        if result:
            print("\n".join(result))
        else:
            print(f"Не знайдено медалістів для року {args.total}")
    else:
        for line in file:
            row = line.strip().split('\t')

            if row[noc_index] == args.country:
                if row[medal_index] in medal_rahunok:
                    medalists.append(f"{row[name_index]}----{row[event_index]}-----{row[medal_index]}")
                    medal_rahunok[row[medal_index]] += 1

                    if len(medalists) == 10:
                        break

        result = []
        if medalists:
            result.append("\n")
            result.append("Перші 10 медалістів:")
            result.append("\n")
            result.append("\n".join(medalists))
            result.append("\nСумарна кількість медалей:")

            for medal_type in ['Gold', 'Silver', 'Bronze']:
                result.append(f"{medal_type}: {medal_rahunok[medal_type]}")
        else:
            result.append(f"Не знайдено медалістів для країни {args.country}")

        result_output = "\n".join(result)
        print(result_output)

        if args.output:
            with open(args.output, "w") as output_file:
                output_file.write(result_output)