from formaters import *
def handle_medals_arg(data: list, configs: list):
    country, year = configs[0], int(configs[1])
    try:
        entries = [
            entry for entry in data
            if country in (entry['Team'], entry['NOC']) and
               entry['Year'] == year and
               entry['Medal'] != 'NA']

        if not entries:
            raise ValueError("No entries found")

        first10 = [
            (entry["Name"], entry["Sport"], entry["Medal"])
                for entry in entries[0:10 if len(entries) >= 10 else len(entries)]
        ]
        max_len = [max(len(line[i]) for line in first10) for i in range(2)]
        string_len = sum(max_len) + 19

        title: str = format_center('Medalists:', string_len)
        separate_line: str = '-' * string_len
        header: str = f" №   | {' | '.join([format_center(x, max_len[i]) for i, x in enumerate(['Name', 'Sport'])])}  | Medal"

        rows: [str] = []
        for n, athlete in enumerate(first10):
            athlete_info = ' | '.join([format_left(athlete[i], max_len[i]) for i in range(2)])
            medal = athlete[2]
            rows.append(f" {n + 1}. {' ' * (n < 9)}| {athlete_info} | {medal}\n")

        body: str = ""
        for row in rows:
            body += row

        medals = {
            medal: [entry['Medal'] for entry in entries].count(medal)
            for medal in ['Gold', 'Silver', 'Bronze']
        }
        total_medals: str = f"Total medals: Gold: {medals['Gold']}, Silver: {medals['Silver']}, Bronze: {medals['Bronze']}"

        output = f"""
            {title}
            {separate_line}
            {header}
            {separate_line}
            {body}
            {separate_line}
            {total_medals}
        """
        print(output)
        # if config["output"]:
        #     print(output, file=open(config['output'], 'w'))
    except Exception as e:
        print(e)