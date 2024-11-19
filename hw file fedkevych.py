with open('Olympic Athletes - raw.tsv', encoding="utf-8") as f:
    lines = f.readlines()
column_names = lines[0].strip().split('\t')
data = [dict(zip(column_names, line.strip().split("\t"))) for line in lines[1:]]