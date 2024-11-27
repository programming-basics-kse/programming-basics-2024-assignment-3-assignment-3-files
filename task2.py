import argparse

medalists = []
medal_rahunok = {'Gold': 0, 'Silver': 0, 'Bronze': 0}
total_medal_count = {}

parser = argparse.ArgumentParser(description="Медалісти з країн")
parser.add_argument("country", help="Країна")
parser.add_argument("-medals", type=int, help="Рік Олімпіади")
parser.add_argument("-output", type=str, help="Файл виведення результатів")

args = parser.parse_args()

with open("Olympic Athletes - athlete_events.tsv", "r") as file:
    data = file.readline().strip()
    first_str = data.split('\t')

    name_index = first_str.index('Name')
    event_index = first_str.index('Event')
    medal_index = first_str.index('Medal')
    noc_index = first_str.index('NOC')
    year_index = first_str.index('Year')

    for line in file:
        row = line.strip().split('\t')

# Якщо абревіатура співпадає з ввденою країною, тоді...
        if row[noc_index] == args.country:
            if row[medal_index] in medal_rahunok:
                medalists.append(f"{row[name_index]}----{row[event_index]}-----{row[medal_index]}")
                medal_rahunok[row[medal_index]] += 1

            if len(medalists) == 10:
                break


result = []
if medalists:
    result.append("\nПерші 10 медалістів:")
    result.append("\n")
    result.append("\n".join(medalists))

    result.append("\nСумарна кількість медалей:")
    for medal_tipe in ['Gold', 'Silver', 'Bronze']:
        result.append(f"{medal_tipe}: {medal_rahunok[medal_tipe]}")
else:
    result.append(f"Не знайдено медалістів для країни: {args.country}")

result_output = "\n".join(result)
print(result_output)



if args.output:
    with open(args.output, "w") as output_file:
        output_file.write(result_output)
