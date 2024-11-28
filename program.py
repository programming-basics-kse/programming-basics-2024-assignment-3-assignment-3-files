# import argparse

# parser = argparse.ArgumentParser("Sample program")

# parser.add_argument('input_file', help="Filepath for an input file")

# args = parser.parse_args()
# input_file = args.input_file

# print(f"input_file: {args.input_file}")

# with open('Olympic Athletes - athlete_events.csv', 'rt') as file:
#     next(file)  
#     people = []
#     for line in file:
#         line = line.strip()
#         split = line.split(',')
#         id = split[0]
#         Name = split[1]
#         Sex = split[2]
#         Age = split[3]
#         Height = split[4]
#         Weight = split[5]
#         Team =split[6]
#         noc = split[7]
#         Games = split[8]
#         Year = split[9]
#         Season = split[10]
#         City = split[11]
#         Sport = split[12]
#         Event = split[13]
#         Medal = split[14]
#         people.append((1, 2, 3, 4)) 
# #        print(people)

            
import csv
import sys

def read_data(file_path, delimiter='\t'):
    """Зчитує файл з даними та повертає список записів."""
    with open(file_path, mode='r', encoding='utf-8') as file:
        return list(csv.DictReader(file, delimiter=delimiter))

def filter_medals(data, country, year):
    """Фільтрує медалі за країною та роком."""
    filtered = [row for row in data if (row['Team'] == country or row['NOC'] == country) and row['Year'] == year and row['Medal']]
    return filtered

def summarize_medals(medal_list):
    """Підраховує кількість медалей за типами."""
    summary = {'Gold': 0, 'Silver': 0, 'Bronze': 0}
    for medal in medal_list:
        if medal['Medal'] in summary:
            summary[medal['Medal']] += 1
    return summary

def save_output(file_path, content):
    """Зберігає результати у файл."""
    with open(file_path, mode='w', encoding='utf-8') as file:
        file.write(content)

def task_medals(file_path, country, year, output_file=None):
    """Виконує завдання з пошуку медалістів."""
    data = read_data(file_path)
    medals = filter_medals(data, country, year)

    if not medals:
        result = f"У {country} немає медалей на Олімпіаді {year}."
    else:
        result = "Перші 10 медалістів:\n"
        result += "\n".join([f"{row['Name']} - {row['Sport']} - {row['Medal']}" for row in medals[:10]])
        summary = summarize_medals(medals)
        result += "\n\nСумарна кількість медалей:\n"
        result += f"Золото: {summary['Gold']}, Срібло: {summary['Silver']}, Бронза: {summary['Bronze']}"

    if output_file:
        save_output(output_file, result)
    print(result)

if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) < 4 or args[1] != '-medals':
        print("Неправильний формат команди.")
        sys.exit(1)

    file_path = args[0]
    country = args[2]
    year = args[3]
    output_file = args[5] if len(args) > 4 and args[4] == '-output' else None

    task_medals(file_path, country, year, output_file)
