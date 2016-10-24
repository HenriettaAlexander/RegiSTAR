import csv

with open('names.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')

    first_names = []
    last_names = []

    for row in readCSV:
        first_name = row[1]
        last_name = row[2]

        first_names.append(first_name)
        last_names.append(last_name)

    for i in range(len(first_names)-1):
        print first_names[i], last_names[i]
