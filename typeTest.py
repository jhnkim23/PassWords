import pygame_textinput
import pygame
from pygame.locals import *
import sys
import time
import random

import prepareData
import klog
import lstm
from subprocess import Popen, PIPE

numWords = 51

class Game:
  def __init__(self):
    self.w=750
    self.h=500
    self.reset=True
    self.active = False
    self.john = False

    self.input_text=''
    self.final_text=''
    self.textinput = pygame_textinput.TextInput()
    self.word = ''
    self.time_start = 0
    self.total_time = 0
    self.accuracy = '0%'
    self.results = 'Time:0 Accuracy:0 % Wpm:0 '
    self.wpm = 0
    self.rawWpm = 0
    self.end = False
    self.HEAD_C = (255,213,102)
    self.TEXT_C = (240,240,240)
    self.RESULT_C = (255,213,102)
    pygame.init()
    #self.open_img = pygame.image.load('type-speed-open.png')
    #self.open_img = pygame.transform.scale(self.open_img, (self.w,self.h))
    self.bg = pygame.image.load('images/background.jpg')
    self.bg = pygame.transform.scale(self.bg, (self.w,self.h))
    self.screen = pygame.display.set_mode((self.w,self.h))
    pygame.display.set_caption('Type Speed test')

  def run(self):
    self.reset_game()
    self.running=True
    while(self.running):
      clock = pygame.time.Clock()
      self.screen.fill((0,0,0), (50,250,650,50))
      pygame.draw.rect(self.screen,self.HEAD_C, (50,250,650,50), 2)
      
      # update the text of user input
      self.draw_text(self.screen, self.textinput.get_text(), 274, 26,(250,250,250))
    
      events = pygame.event.get()
      if self.active:
        self.textinput.update(events)
      
      for event in events:
        if event.type == QUIT:
          self.running = False
          sys.exit()
        
        elif event.type == pygame.MOUSEBUTTONUP:
          x,y = pygame.mouse.get_pos()
          if (x <= 10 and x>= 0 and y <= 10 and y <= 10):
            self.john = True

          # position of input box
          if(x>=50 and x<=650 and y>=250 and y<=300) and self.active == False:
            self.active = True
            self.time_start = time.time()

          # position of reset box
          if(x>=310 and x<=510 and y>=390 and self.end) and self.end:
            self.reset_game()
            x,y = pygame.mouse.get_pos()

        #this isnt working
        elif event.type == pygame.KEYDOWN:
          if self.active and not self.end:
            if event.key == pygame.K_RETURN:
              self.final_text = self.textinput.get_final_text()
              self.show_results(self.screen)
              self.draw_text(self.screen, self.results,350, 28, self.RESULT_C)
              self.end = True
              self.textinput.clear_text()
              self.textinput.final_string = ''
              prepareData.addTrainingData(self.john, self.wpm, self.rawWpm, self.accuracy)
              lstm.predict()
      pygame.display.update()
      clock.tick(30)
  
  def reset_game(self):
    Popen(['python','klog.py'])

    self.screen.blit(self.bg, (0,0))
    pygame.display.update()
    self.active=False
    self.reset=False
    self.end = False
    self.john = False
    self.word = ''
    self.time_start = 0
    self.total_time = 0
    self.wpm = 0
    self.rawWpm = 0
    # Get random sentence
    self.word = self.get_sentence()
    if (not self.word): self.reset_game()
    #drawing heading
    self.screen.fill((0,0,0))
    self.screen.blit(self.bg,(0,0))
    msg = "Typing Speed Test"
    self.draw_text(self.screen, msg,80, 80,self.HEAD_C)
    # draw the rectangle for input box
    pygame.draw.rect(self.screen,(255,192,25), (50,250,650,50), 2)
    # draw the sentence string
    actual = ''
    start = 135
    while '\\' in self.word:
      split = self.word[:self.word.index('\\')]
      self.draw_text(self.screen, split,start, 28,self.TEXT_C)
      self.word = self.word[self.word.index('\\')+1:]
      start += 20
      actual += split + ' '
    self.draw_text(self.screen, self.word,start, 28,self.TEXT_C)
    self.word = actual + self.word
    pygame.display.update()
  
  def show_results(self, screen):
    if(not self.end):
      #Calculate time
      self.total_time = time.time() - self.time_start
      #Calculate accuracy
      inputWords = self.final_text.split(' ')
      rawWords = self.word.split(' ')

      incorrect = abs(len(inputWords) - len(rawWords)) #accounts for differences in spaces
      correct = len(inputWords)-1
      if len(inputWords) > len(rawWords):
        correct -= incorrect
      
      for ind in range(max(len(inputWords), len(rawWords))):
        if ind >= min(len(inputWords), len(rawWords)):
          incorrect += len(inputWords[ind]) if len(inputWords) > len(rawWords) else len(rawWords[ind])
        else:
          for chInd in range(min(len(inputWords[ind]), len(rawWords[ind]))):
            if inputWords[ind][chInd] == rawWords[ind][chInd]:
              correct += 1
            else:
              incorrect+=1
          incorrect += max(len(inputWords[ind]),len(rawWords[ind])) - min(len(inputWords[ind]),len(rawWords[ind])) 
      print("Correct Vs. Incorrect:",correct, incorrect)
      
      self.accuracy = correct/(correct+incorrect)*100
      #Calculate words per minute
      self.wpm = correct * (60/self.total_time)/5
      self.rawWpm = (correct+incorrect) * (60/self.total_time)/5
      self.end = True
      print(self.total_time)
      self.results = 'Time: '+str(round(self.total_time)) +"s  Accuracy: "+ str(round(self.accuracy)) + "%" + '  Wpm: ' + str(round(self.wpm))
      self.draw_text(screen,"Reset", self.h - 70, 26, (100,100,100))
      print(self.results)
      pygame.display.update()
  
  def get_sentence(self):
    f = open('wordList.txt').read()
    words = f.split('\n')
    sentence = random.choice(words)
    sentenceLen = 1
    for i in range(numWords-1):
      randomWord = random.choice(words)
      if len(sentence + ' ' + randomWord) > 70*sentenceLen:
        sentence = sentence + '\\' + randomWord
        sentenceLen+=1
      else:
        sentence = sentence + ' ' + randomWord
    return sentence
  
  def draw_text(self, screen, msg, y ,fsize, color):
    font = pygame.font.Font(None, fsize)
    text = font.render(msg, 1,color)
    text_rect = text.get_rect(center=(self.w/2, y))
    screen.blit(text, text_rect)
    pygame.display.update()

if __name__ == '__main__':
  Game().run()

#Make pygame show only up to 75 charcters of the sentence.
#Then after each type press change sentence and display the new one
#By subtracting one from sentence and then adding the other character