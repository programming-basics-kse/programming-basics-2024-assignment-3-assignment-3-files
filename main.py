import argparse

MEDALISTS = 10

def parser_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Medalists database processing program')
    parser.add_argument('input_file', help='Data file address')
    parser.add_argument('-medals', nargs=2, metavar = ('COUNTRY', 'YEAR'), help='The top ten medalists from this country at a given Olympiad')
    parser.add_argument('-output', metavar='NAME', help='The output file')
    return parser.parse_args()

def medals(input_file, country, year) -> list[list]:
    with open(input_file, 'rt') as file:
        counter = 0
        medalists = []
        next(file)
        for line in file:
            elements = line.split('\t')
            year_line = elements[9]
            team = elements[6]
            noc = elements[7]
            medal = elements[14].split('\n')[0]

            if not (year == year_line and (country == team or country == noc)) or medal == 'NA':
                continue

            name = elements[1]
            discipline = elements[12]

            medalists.append([name, discipline, medal])

            if counter >= MEDALISTS - 1:
                break
            counter += 1
        return medalists

def output_file(output_file_name: str, content: str):
    with open(output_file_name, 'wt') as file:
        file.write(content)

def output(medals_out: list[list], output_file_name: str):
    output_content = ''

    if len(medals_out) == 0:
        output_content = 'No medalists found\nPlease enter the correct country or year.'
    else:
        for i in range(len(medals_out)):
            output_content += f'{i+1}. '
            output_content += f'{medals_out[i][0]} - {medals_out[i][1]} - {medals_out[i][2]}'
            output_content += '\n'
        gold = 0
        silver = 0
        bronze = 0
        for i in medals_out:
            gold += i.count('Gold')
            silver += i.count('Silver')
            bronze += i.count('Bronze')
        output_content += f'Gold: {gold}\n'
        output_content += f'Silver: {silver}\n'
        output_content += f'Bronze: {bronze}'

    print(output_content)
    if output_file_name is not None:
        output_file(output_file_name, output_content)

def main():
    args = parser_arguments()
    medals_result = medals(args.input_file, args.medals[0], args.medals[1])
    output(medals_result, args.output)

if __name__ == '__main__':
    main()