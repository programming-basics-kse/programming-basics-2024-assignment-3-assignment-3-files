from formaters import *
def handle_total_arg(data: list, config: int):
    year = config
    try:
        entries = [entry for entry in data if entry['Year'] == year]
        if not entries:
            raise ValueError("No entries found")

        countries = {}
        for country in entries:
            if country['Medal'] in {'Gold', 'Silver', 'Bronze'}:
                countries.setdefault(country['Team'], {'Gold': 0, 'Silver': 0, 'Bronze': 0})[country['Medal']] += 1

        countries = [
            (key, str(value['Gold']), str(value['Silver']), str(value['Bronze']))
            for key, value in countries.items()
        ]
        print(countries)

        max_len = [max(len(country[i]) for country in countries) for i in range(4)]
        string_len = sum(max_len) + 19

        print("=============")
        title: str = format_center('Countries:', string_len)
        separate_line: str = '-' * string_len
        header: str = f" №   | {' | '.join([format_center(x, max_len[i]) for i, x in enumerate(['Country', 'Gold', 'Silver', 'Bronze'])])}"

        rows: [str] = []
        for n, country in enumerate(countries):
            country_info = ' | '.join([format_left(country[i], max_len[i]) for i in range(4)])
            medal = country[2]
            print(country[0], country[1], country[2], country[3])
            rows.append(f" {n + 1}. {' ' * (n < 9)}| {country_info} |\n")

        body: str = ""
        for row in rows:
            body += row

        medals = {
            medal: [entry['Medal'] for entry in entries].count(medal)
            for medal in ['Gold', 'Silver', 'Bronze']
        }

        output = f"""
                {title}
                {separate_line}
                {header}
                {separate_line}
                {body}
                {separate_line}
            """
        print(output)
        # if config["output"]:
        #     print(output, file=open(config['output'], 'w'))
    except Exception as e:
        print(e)