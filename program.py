with open('Olympic Athletes - athlete_events.csv', 'rt') as file:
    next(file)  
    people = []
    for line in file:
        line = line.strip()
        split = line.split(',')  # Розбиваємо рядок
        #if len(split) == 4:  # Перевіряємо, чи є всі потрібні частини
        a = split[0]
        b = split[1]
        c = split[2]
        d = split[3]
        people.append((1, 2, 3, 4)) 
        print(people)

            