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

def total(list,year):
    countries = {}
    med = ["Gold","Silver","Bronze"]
    for row in list:
        if (row[9] == str(year)) and (row[14] in med):
            if row[6] not in countries:
                countries[row[6]] = []
    if len(countries) == 0:
        print("There are no olympics in that year")
    for key in countries:
        g = 0
        s = 0
        b = 0
        for row in list:
           if row[9] == str(year) and key == row[6]:
                if row[14] == "Gold":
                    g += 1
                if row[14] == "Silver":
                    s += 1
                if row[14] == "Bronze":
                    b += 1
        countries[key].append(g)
        countries[key].append(s)
        countries[key].append(b)
    return countries

def pr_total(diction):
    for key in diction:
        print(f"{key} - Gold: {diction[key][0]} - Silver: {diction[key][1]} - Bronze: {diction[key][2]}")