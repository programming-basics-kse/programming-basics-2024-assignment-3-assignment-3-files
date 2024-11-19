import argparse

parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("filename", type=str, help="Source location")
parser.add_argument("-medals", action="store_true", required=True)
parser.add_argument("country", type=str, help="Country name")
parser.add_argument("year", type=int, help="Year of the olympics")
parser.add_argument("-output", help="Filename of output file")
config = vars(parser.parse_args())

data = [line.split('\t') for line in open(config["filename"], "r").read().splitlines()]
data = [{data[0][n]: int(field) if field.isdigit() else field for n, field in enumerate(entry)} for entry in data[1::]]

def format_left(string, length): return string + " "*(length - len(string))
def format_center(string, length): return ' '*((n := length - len(string))//2) + string + ' '*((n+n%2)//2)

try:
    entries = [entry for entry in data if config["country"] in (entry['Team'], entry['NOC']) and
               entry['Year'] == config["year"] and entry['Medal'] != 'NA']
    if not entries: raise ValueError("No entries found")
    first10 = [(e["Name"], e["Sport"], e["Medal"]) for e in entries[0:10 if len(entries) >= 10 else len(entries)]]
    max_len = [max(len(x[i]) for x in first10) for i in range(2)]
    string_len = sum(max_len) + 19

    output = f"""
{format_center('Medalists:', string_len)}
{'-'*string_len}
 №   | {' | '.join((format_center(x, max_len[i]) for i, x in enumerate(('Name', 'Sport'))))} | Medal
{'-'*string_len}
{'\n'.join((f' {n+1}. {' '*(n < 9)}| ' +
            ' | '.join((*(format_left(x[i], max_len[i]) for i in range(2)), x[2])) for n, x in enumerate(first10)))}
{'-'*string_len}
 Total medals: {"Gold: {Gold}, Silver: {Silver}, Bronze: {Bronze}".format(**{
    medal: [entry['Medal'] for entry in entries].count(medal) for medal in ['Gold', 'Silver', 'Bronze']})}
"""
    print(output)
    if config["output"]:
        print(output, file=open(config['output'], 'w'))
except Exception as e:
    print(e)
