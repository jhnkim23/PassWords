import random
from csv import writer

for i in range(10):
  fakeDynamics = []
  timesteps = random.randint(300,350)

  for step in range(timesteps):
    id1 = random.randint(0,27)
    id2 = random.randint(0,27)
    h1 = round(random.uniform(.001, .8), 16)
    h2 = round(random.uniform(.001, .8), 16)
    u1d2 = round(random.uniform(-.08, .8), 16)
    d1d1= round(random.uniform(.003, h1+h2+.3), 16)
    if id1 == 26:
      id1 = 'Key.space'
    elif id1 == 27:
      id1 = 'Key.backspace'
    else:
      id1 = chr(id1+97)
    if id2 == 26:
      id2 = 'Key.space'
    elif id2 == 27:
      id2 = 'Key.backspace'
    else:
      id2 = chr(id2+97)
    fakeDynamics += [id1, id2, h1, h2, u1d2, d1d1]

  with open('data.csv', 'a+', newline = '') as writingTo:
    csv_writer = writer(writingTo)
    csv_writer.writerow([0] + fakeDynamics + [-10, -10, -10])
  writingTo.close()