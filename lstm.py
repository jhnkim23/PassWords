import csv
import pandas as pd
import numpy as np
import math
from tensorflow.keras.utils import Sequence
from keras.models import Sequential
from keras.layers import Dense, LSTM, Dropout, Masking
from tensorflow.keras.optimizers import Adam
from keras.preprocessing.sequence import pad_sequences
from sklearn.preprocessing import MinMaxScaler

def predict():
  lxTrain = []
  lyTrain = []
  xTrain = []
  alphabet = 28
  maxLen = 0

  with open('data.csv','r') as cf:
    lines = csv.reader(cf)
    
    #Ignore the Header
    next(lines)

    for line in lines:
      #Whether or not it was user
      lyTrain += [int(line[0])]

      #Last three standard inputs: [wpm, rawWpm, acc]
      xTrain = [float(i) for i in line[-3:]]

      #Recursive Input into LSTM
      recurInput = line[1:(len(line)-4)//6 * 6 + 1]
      preEncode = [[recurInput[i*6: (i+1)*6] for i in range(len(recurInput)//6)]]
      
      adding = []
      for pairs in preEncode:
        for pair in pairs:
          alpha1 = pair[0]
          alpha2 = pair[1]
          
          ohe1 = [0 for i in range(alphabet)]
          ohe2 = [0 for i in range(alphabet)]

          if 'backspace' in alpha1:
            ohe1[27] = 1
          elif 'space' in alpha1:
            ohe1[26] = 1
          else:
            ohe1[ord(alpha1)-97] = 1
          if 'backspace' in alpha2:
            ohe2[27] = 1
          elif 'space' in alpha2:
            ohe2[26] = 1
          else:
            ohe2[ord(alpha2)-97] = 1

          adding += [ohe1+ohe2+pair[2:]]
      maxLen = max(len(adding), maxLen)
      lxTrain += [adding]
  cf.close()
  yTrain = lyTrain

  for i in range(len(lxTrain)):
    for remain in range(maxLen - len(lxTrain[i])):
      lxTrain[i] += [[-10] * 60]

  for i in range(len(lxTrain)):
    lxTrain[i] = np.array(lxTrain[i])
  lxTrain, lyTrain = np.array(lxTrain[:-1]), np.array(lyTrain[:-1])
  x_test = np.array([np.array(np.array(lxTrain[-1]))])

  #LSTM creation
  model = Sequential()
  #variable sequence, 60 inputs per timestep
  model.add(Masking(mask_value=np.array([-10]*60), input_shape=(None, 60)))
  model.add(LSTM(80))
  model.add(Dense(1))

  opt = Adam(lr=1e-2, decay=1e-5)
  model.compile(loss='mse', optimizer=opt, metrics=['accuracy'])
  model.fit(lxTrain, lyTrain, epochs=5)

  predictions = model.predict(x_test)
  print(predictions)