from csv import writer
import csv

def clearAll():
  header = ['User', 'Data']
  with open('data.csv', 'w', newline = '') as writingTo:
    csv_writer = writer(writingTo)
    csv_writer.writerow(header)
  writingTo.close()

def clearFake():
  lines = list()

  with open('data.csv', 'r') as readFile:
    reader = csv.reader(readFile)
    for row in reader:
      if len(row) != 0:
        if row[len(row)-1] != '-10':
          lines.append(row)
  readFile.close()

  with open('data.csv', 'w', newline='') as writeFile:
    writer = csv.writer(writeFile)
    for line in lines:
      writer.writerow(line)
  writeFile.close()

clearAll()