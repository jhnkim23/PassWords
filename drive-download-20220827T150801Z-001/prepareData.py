from csv import writer

def addTrainingData(isUser, wpm, rawWpm, accuracy):
  txt_reader = open('keyLog.txt', 'r')
  lines = txt_reader.readlines()
  
  press = []
  release = []
  for keyStroke in lines:
    timeTaken = float(keyStroke[:keyStroke.index(' ')])
    keyStroke = keyStroke[keyStroke.index(' ')+1:]
    
    #you need to make this work for Key.space and Key.backspace
    keyID = keyStroke[:keyStroke.index(' ')]
    if "'" in keyID:
      keyID = keyID[1]
    keyStroke = keyStroke[keyStroke.index(' ')+1:]

    if keyStroke[0] == 'P':
      press += [(keyID, timeTaken)]
    else:
      release += [(keyID, timeTaken)]
  
  keystrokeDynamics = []
  #ID1, ID2, H1, H2, U1D1, D1D1
  #-2 just to be safe
  size = min(len(press), len(release)) - 1
  for ind in range(size):
    firstP = press[ind]
    secondP = press[ind+1]

    removeInd = -1
    secondInd = -1
    for indR, val in enumerate(release):
      if removeInd == -1 and val[0] == firstP[0]:
        firstR = val
        removeInd = indR
      elif secondInd == -1 and val[0] == secondP[0]:
        secondR = val
        secondInd = indR
      if removeInd != -1 and secondInd != -1:
        break
    release = release[:removeInd] + release[removeInd+1:]
    
    id1 = firstP[0]
    id2 = secondP[0]
    h1 = firstR[1] - firstP[1]
    h2 = secondR[1] - secondP[1]
    u1d2 = secondP[1] - firstR[1]
    d1d2 = secondP[1] - firstP[1]
    keystrokeDynamics += [id1, id2, h1, h2, u1d2, d1d2]

  with open('data.csv', 'a+', newline = '') as writingTo:
    csv_writer = writer(writingTo)
    csv_writer.writerow([int(isUser)] + keystrokeDynamics + [wpm, rawWpm, accuracy])
  writingTo.close()