import csv
import json

csvfile = open('data.csv', 'r')
jsonfile = open('data.json', 'w')

fieldnames = ("name","a","b","c", "d", "e", "f", "mail", "g", "h", "i", "j", "k", "l")
reader = csv.DictReader(csvfile, fieldnames)
jsonfile.write('[')
for row in reader:
    json.dump(row, jsonfile)
    jsonfile.write(',')
jsonfile.write('{}')
jsonfile.write(']')

