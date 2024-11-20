import argparse

parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("filename", type=str, help="Source location")
parser.add_argument("-medals", nargs=2, metavar=('COUNTRY', 'YEAR'), help="List of medals of country in specific olympics")
parser.add_argument('-total', metavar='YEAR', help="Every country performance on specific olympics")
parser.add_argument('-overall', nargs='+', metavar='COUNTRY', help="Best performance year of every country")
parser.add_argument('-interactive', action="store_true", help="Interactive mode")
parser.add_argument("-output", metavar='FILENAME', help="Filename of output file")
config = vars(parser.parse_args())

with open(config["filename"], "r") as file: data = [line.split('\t') for line in file.read().splitlines()]
data = [{data[0][n]: int(field) if field.isdigit() else field for n, field in enumerate(entry)} for entry in data[1::]]

def format_left(string, length): return string + " "*(length - len(string))
def format_center(string, length): return ' '*((n := length - len(string))//2) + string + ' '*((n+n%2)//2)

def handle_medals_arg(data_: list, country: str, year: int) -> str:
    entries = [entry for entry in data_ if country in (entry['Team'].split('-')[0], entry['NOC']) and
               entry['Year'] == year and entry['Medal'] != 'NA']
    if not entries: raise ValueError("No entries found")
    first10 = [(e["Name"], e["Sport"], e["Medal"]) for e in entries[0:10 if len(entries) >= 10 else len(entries)]]
    max_len = [max(len(x[i]) for x in first10) for i in range(3)]
    string_len = sum(max_len) + 15

    title: str = format_center('Medalists:', string_len)
    separator: str = '-' * string_len
    header: str = f" №   | {' | '.join((format_center(x, max_len[i]) for i, x in enumerate(('Name', 'Sport'))))} | Medal  |"
    body: str = '\n'.join(
        f" {n + 1}. {' ' if n < 9 else ''}| " +
        ' | '.join(format_left(x[i], max_len[i]) for i in range(3))
        for n, x in enumerate(first10)
    )
    total_medals = {
        medal: [entry['Medal'] for entry in entries].count(medal) for medal in ['Gold', 'Silver', 'Bronze']
    }
    medal_label = "Gold: {Gold}, Silver: {Silver}, Bronze: {Bronze}".format(**total_medals)
    footer: str = format_center(f"Total medals: {medal_label}", string_len)
    return f"""
{title}
{separator}
{header}
{separator}
{body}
{separator}
{footer}
    """

def handle_total_arg(data_: list, year: int) -> str:
    entries = [entry for entry in data_  if year == entry['Year'] and entry['Medal'] != 'NA']
    if not entries: raise ValueError("No entries found")

    medals_count = {}
    for entry in entries:
        country = entry['Team'].split('-')[0]
        if country not in medals_count: medals_count[country] = {'Gold': 0, 'Silver': 0, 'Bronze': 0}
        medals_count[country][entry['Medal']] += 1

    medals = [(e, str(medals_count[e]['Gold']), str(medals_count[e]['Silver']), str(medals_count[e]['Bronze'])) for e in medals_count.keys()]
    header_list = ('Country', 'Gold', 'Silver', 'Bronze')
    max_len = [max(max(len(x[i]) for x in medals), len(header_list[i])) for i in range(4)]
    string_len = sum(max_len) + 18

    title: str = format_center('Countries:', string_len)
    separator: str = '-' * string_len
    header: str = f" №   | {' | '.join((format_center(x, max_len[i]) for i, x in enumerate(header_list)))} |"
    body: str = '\n'.join(
        f" {n + 1}. {' ' if n < 9 else ''}| " +
        ' | '.join(
            format_left(x[i], max_len[i]) if i == 0 else format_center(x[i], max_len[i])
            for i in range(4)
        ) + ' | '
        for n, x in enumerate(medals)
    )
    return f"""
{title}
{separator}
{header}
{separator}
{body}
{separator}
        """

def output(text: str):
    print(text)
    if config["output"]:
        print(text, file=open(config['output'], 'w'))

if config["medals"]:
    output(handle_medals_arg(data, config["medals"][0], int(config["medals"][1])))
elif config["total"]:
    output(handle_total_arg(data, int(config["total"])))
elif config["overall"]:
    pass
elif config["interactive"]:
    pass