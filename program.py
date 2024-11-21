with open('Olympic Athletes - athlete_events.csv', 'rt') as file:
    next(file)  
    people = []
    for line in file:
        line = line.strip()
        split = line.split(',')
        id = split[0]
        Name = split[1]
        Sex = split[2]
        Age = split[3]
        Height = split[4]
        Weight = split[5]
        Team =split[6]
        noc = split[7]
        Games = split[8]
        Year = split[9]
        Season = split[10]
        City = split[11]
        Sport = split[12]
        Event = split[13]
        Medal = split[14]
        people.append((1, 2, 3, 4)) 
        
        print(people)

            