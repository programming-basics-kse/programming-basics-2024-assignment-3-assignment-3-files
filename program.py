import os

def file_to_list(file):
    data = []
    with open(os.getcwd()+"\\"+file, "rt") as f:
        next(f)
        for l in f:
            l = l[:-1]
            s = l.split(",")
            data.append(s)
    return data