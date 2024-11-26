import argparse
import program2 as pr2
import program4 as pr4


parser = argparse.ArgumentParser()
parser.add_argument("file", type=str, help='Enter name of file(example: data.csv)')
parser.add_argument("-total", type=int, help='Enter the year(example: 1972)')
parser.add_argument("-interactive", action="store_true", help='No arguments')

args = parser.parse_args()

dataset = pr2.file_to_list(args.file)

if args.total:
    year = args.total
    t = pr2.total(dataset,year)
    pr2.pr_total(t)
elif args.interactive:
    info = pr4.interactive(dataset)
    if info != "f":
        pr4.pr_interactive(info)
