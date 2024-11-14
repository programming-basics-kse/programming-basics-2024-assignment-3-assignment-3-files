import argparse

parser = argparse.ArgumentParser(description='Medalists database processing program')
parser.add_argument('input_file', help='Data file address')
parser.add_argument('-medals', nargs=2, metavar = ('COUNTRY', 'YEAR'), help='The top ten medalists from this country at a given Olympiad')
parser.add_argument('-output', metavar='NAME', help='The output file')
args = parser.parse_args()