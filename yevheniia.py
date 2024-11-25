import sys

def output_medals(results, country, year, output_file=None):
    output_text = ""
    for row in results:
        if (row["Team"] == country) and int(row["Year"]) == year:
            output_text += (f"Country: {row['Team']}, Medals: {row['Gold']} gold, {row['Silver']} silver, "
                            f"{row['Bronze']} bronze\n")

    if not output_text:
        output_text = "No data for this country and year.\n"

    if output_file:
        with open(output_file, "w", encoding="utf-8") as file:
            file.write(output_text)
    else:
        print(output_text)
