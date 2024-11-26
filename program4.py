def interactive(dataset):
    country = input("Enter country: ")
    list = []
    for row in dataset:
        if row[6] == country or row[7] == country:
            list.append(row)
    if len(list) == 0:
        print("There are no such country")
        return "f"

    first = list[0][9]
    first_place = list[0][11]
    for i in range(1,len(list)):
        if list[i][9] < first:
            first = list[i][9]
            first_place = list[i][11]

    best_years = {}
    for i in list: #list with all games of one country
        if i[9] not in best_years:
            best_years[i[9]] = 0 #dict with key: years and num of medals

    medals = ["Gold","Silver","Bronze"]
    for key in best_years:
        num = 0
        for i in list:
            if i[14] in medals and key == i[9]:
                num += 1
        best_years[key] = num

    best_y_num = -1
    for key in best_years:
        if best_years[key] > best_y_num:
            best_y_num = best_years[key]
            best_y = key

    worth_y_num = best_y_num
    for key in best_years:
        if best_years[key] < worth_y_num:
            worth_y_num = best_years[key]
            worth_y = key

    average = {}
    for i in list:
        if i[9] not in average:
            average[i[9]] = []
    for key in average:
        gold = 0
        silver = 0
        bronze = 0
        for i in list:
            if i[14] == "Gold" and i[9] == key:
                gold += 1
            if i[14] == "Silver" and i[9] == key:
                silver += 1
            if i[14] == "Bronze" and i[9] == key:
                bronze += 1
        average[key].append(gold)
        average[key].append(silver)
        average[key].append(bronze)
    n = 0
    sum_g = 0
    sum_s = 0
    sum_b = 0
    for key in average:
        n += 1
        sum_g += average[key][0]
        sum_s += average[key][1]
        sum_b += average[key][2]
    ave_g = round(sum_g/n,2)
    ave_s = round(sum_s/n,2)
    ave_b = round(sum_b/n,2)
    info = [country, first, first_place, best_y, best_y_num, worth_y, worth_y_num, ave_g, ave_s, ave_b]
    return info