import sys

def output_total(results, year, output_file=None):
    medal_counts = {}

    for row in results:
        if int(row["Year"]) == year:
            country = row["Team"]
            if country not in medal_counts:
                medal_counts[country] = {"Gold": 0, "Silver": 0, "Bronze": 0}
            medal_counts[country]["Gold"] += int(row["Gold"])
            medal_counts[country]["Silver"] += int(row["Silver"])
            medal_counts[country]["Bronze"] += int(row["Bronze"])

    output_text = ""
    for country, counts in medal_counts.items():
        output_text += (f"{country} - {counts['Gold']} gold - {counts['Silver']} silver"
                        f" - {counts['Bronze']} bronze\n")

    if not output_text:
        output_text = "No data for this year.\n"

    if output_file:
        with open(output_file, "w", encoding="utf-8") as file:
            file.write(output_text)
    else:
        print(output_text)
