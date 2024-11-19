import argparse

def receive_application_args() -> [argparse.Namespace]:
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("filename", type=str, help="Source location")
    parser.add_argument("-medals", nargs=2, metavar=('COUNTRY', 'YEAR'),
                        help="List of medals of country in specific olympics")
    parser.add_argument('-total',type=int, metavar='YEAR', help="Every country performance on specific olympics")
    parser.add_argument('-overall', nargs='+', metavar='COUNTRY', help="Best performance year of every country")
    parser.add_argument('-interactive', action="store_true", help="Interactive mode")
    parser.add_argument("-output", metavar='FILENAME', help="Filename of output file")
    return vars(parser.parse_args())