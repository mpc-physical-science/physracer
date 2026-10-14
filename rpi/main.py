# Simple pygame program

# Import and initialize the pygame library
import pygame as pg
import serial
import sys
import glob
import re
import time
from threading import Thread

timer_ready = False;
last_serial_message = "";
result_time = 0.0;
user_text = ''
scorelines =''
state_timer = 0

ser = serial.Serial('/dev/ttyACM0', 9600, timeout=0)
def worker():

   global timer_ready
   global last_serial_message
   while True:
     msg = ser.readline()
     if len(msg) > 0:
      print("("+time.ctime(time.time())+") "+"Message Received: %s" % msg.decode().strip())
      last_serial_message = msg.decode().strip()
      #print(last_serial_message)
      if last_serial_message == "busy":
         timer_ready=False
         print("("+time.ctime(time.time())+") "+"timer ready: "+str(timer_ready)) 
      elif last_serial_message.startswith('t='):
         timer_ready=True 
         print("("+time.ctime(time.time())+") "+"timer ready:"+str(timer_ready))

t = Thread(target=worker)
t.daemon = True
t.start()

class States(object):
    def __init__(self):
        self.done = False
        self.next = None
        self.quit = False
        self.previous = None

pg.init()

#ser = serial.Serial(
#    port='COM5',\
#    baudrate=9600,\
#    parity=serial.PARITY_NONE,\
#    stopbits=serial.STOPBITS_ONE,\
#    bytesize=serial.EIGHTBITS,\
#        timeout=0)

# loading
#   open serial
#   check timer

class Loading(States):
    def __init__(self):
        States.__init__(self)
        self.next = 'instructions'
        ports = glob.glob('/dev/ttyA*')
        print("("+time.ctime(time.time())+") "+'Serial Ports:')
        print(ports)
        global timer_ready        
    def cleanup(self):
        print("("+time.ctime(time.time())+") "+'exiting [loading]')
    def startup(self):
        print("("+time.ctime(time.time())+") "+'entering [loading]')
    def get_event(self, event):
        if event.type == pg.KEYDOWN:
            print("("+time.ctime(time.time())+") "+'loading keydown')
            self.done = True
        #elif event.type == pg.MOUSEBUTTONDOWN:
        #    self.done = True
    def update(self, screen, dt):
        self.draw(screen)
    def draw(self, screen):
        white = (255, 255, 255)
        green = (0, 255, 0)
        blue = (0, 0, 128)
        X = 960
        Y = 1000
        pg.display.set_caption('Physics Racer')
        font = pg.font.Font('freesansbold.ttf', 96)
        font.set_italic(True)
        text1 = font.render('Physics Racer', True, green, blue)
        text1Rect = text1.get_rect()
        text1Rect.center = (X // 2, Y // 3)
        font = pg.font.Font('freesansbold.ttf', 32)
        font.set_italic(False)
        text2 = font.render('press any key to continue', True, green, blue)
        text2Rect = text2.get_rect()
        text2Rect.center = (X // 2, 2*Y // 3)
        screen.fill((0,0,255))    
        screen.blit(text1, text1Rect)        
        screen.blit(text2, text2Rect) 

# instructions
#   check race started

class Instructions(States):
    def __init__(self):
        States.__init__(self)
        self.next = 'racing'
        global timer_ready        
    def cleanup(self):
        print("("+time.ctime(time.time())+") "+'exiting [Instructions]')    
    def startup(self):
        print("("+time.ctime(time.time())+") "+'entering [Instructions]')    
    def get_event(self, event):
        if event.type == pg.KEYDOWN:
            print("("+time.ctime(time.time())+") "+'Instructions keydown')
        #elif event.type == pg.MOUSEBUTTONDOWN:
        #    self.done = True
    def update(self, screen, dt):
        if last_serial_message == "race started!":
            self.done = True
        self.draw(screen)
    def draw(self, screen):
        global settings
        white = (255, 255, 255)
        green = (0, 255, 0)
        blue = (0, 0, 128)
        yellow = (255,255,0)        
        X = 960
        Y = 1000
        pg.display.set_caption('Instructions')
        font = pg.font.Font('freesansbold.ttf', 96)
        font.set_italic(True) 
        text0 = font.render('Physics Racer', True, green, blue)
        font = pg.font.Font('freesansbold.ttf', 48)
        text1 = font.render('How to play:', True, green, blue)
        font = pg.font.Font('freesansbold.ttf', 48)
        text2 = font.render('1. Build a LEGO racecar', True, green, blue)
        text3 = font.render('2. Race it down the ramp!', True, green, blue)
        text4 = font.render('Your race time will be', True, green, blue)
        text5 = font.render('automatically measured', True, green, blue)
        font = pg.font.Font('freesansbold.ttf', 32)        
        font.set_italic(True)        
        text6 = font.render('Good luck!', True, yellow, blue)
        text7 = font.render('May the mass*acceleration be with you', True, yellow, blue)
        text0Rect = text0.get_rect()
        text1Rect = text1.get_rect()
        text2Rect = text2.get_rect()
        text3Rect = text3.get_rect()
        text4Rect = text4.get_rect()
        text5Rect = text5.get_rect()
        text6Rect = text6.get_rect()
        text7Rect = text7.get_rect()                        
        # set the center of the rectangular object.
        text0Rect.center = (X // 2, 1*Y // 6)
        text1Rect.center = (X // 2, 1.8*Y // 6)
        text2Rect.center = (X // 2, 2.3*Y // 6)
        text3Rect.center = (X // 2, 2.8*Y // 6)
        text4Rect.center = (X // 2, 3.3*Y // 6)
        text5Rect.center = (X // 2, 3.6*Y // 6) 
        text6Rect.center = (X // 2, 5*Y // 6)
        text7Rect.center = (X // 2, 5.2*Y // 6)                        
        screen.fill((0,0,255))    
        screen.blit(text0, text0Rect)
        screen.blit(text1, text1Rect)
        screen.blit(text2, text2Rect)
        screen.blit(text3, text3Rect)
        screen.blit(text4, text4Rect)
        screen.blit(text5, text5Rect)
        screen.blit(text6, text6Rect) 
        screen.blit(text7, text7Rect)                        

# racing
#   check finish

class Racing(States):
    def __init__(self):
        States.__init__(self)
        self.next = 'results'
        global result_time
        global last_serial_message
        global timer_ready
    def cleanup(self):
        global result_time
        print("("+time.ctime(time.time())+") "+'exiting [Racing]')
        #print(result_time)
        #print(last_serial_message)                        
    def startup(self):
        print("("+time.ctime(time.time())+") "+'entering [Racing]')                 
    def get_event(self, event):
        if event.type == pg.KEYDOWN:
            print("("+time.ctime(time.time())+") "+'Racing keydown')
            # clean up any racing data here
            self.done = True
        #elif event.type == pg.MOUSEBUTTONDOWN:
        #    self.done = True
    def update(self, screen, dt):
        global result_time
        global last_serial_message
        if(last_serial_message.startswith('t=')):
            str=''
            result_time=float(str.join(re.findall("\d+\.\d+",last_serial_message)))
            self.done = True
        self.draw(screen)
    def draw(self, screen):
        white = (255, 255, 255)
        green = (0, 255, 0)
        blue = (0, 0, 128)
        X = 960
        Y = 1000
        pg.display.set_caption('Race Underway!')
        font = pg.font.Font('freesansbold.ttf', 64)
        text1 = font.render('Race Underway!', True, green, blue)
        text1Rect = text1.get_rect()
        text1Rect.center = (X // 2, Y // 3)
        font = pg.font.Font('freesansbold.ttf', 32)
        text2 = font.render('press any key to cancel', True, green, blue)
        text2Rect = text2.get_rect()
        text2Rect.center = (X // 2, 2*Y // 3)
        screen.fill((0,0,255))    
        screen.blit(text1, text1Rect)
        screen.blit(text2, text2Rect)
   

# results
#   enter name
#   display ranking

class Results(States):
    def __init__(self):
        States.__init__(self)
        self.next = 'highscores'
        global result_time
        global last_serial_message   
    def cleanup(self):
        print("("+time.ctime(time.time())+") "+'exiting [Results]')  
        if(result_time > 0.0):        
            with open('highscores.txt', 'a') as highscores_file:
                highscores_file.write("{:.6f}".format(result_time) + ' ' + user_text + '\n')       
    def startup(self):
        global timer_ready 
        print("("+time.ctime(time.time())+") "+'entering [Results]')       
        #try:
            #t_index = last_serial_message.index("t=")
            #print(last_serial_message.index("t="))
            #str=''
            #result_time=float(str.join(re.findall("\d+\.\d+",last_serial_message)))
            #print(result_time)
            #print(last_serial_message)
            #t_index = -1
    def get_event(self, event):
        global user_text
        if event.type == pg.KEYDOWN:
           # Check for backspace 
            if event.key == pg.K_BACKSPACE: 
                user_text = user_text[:-1] 
            elif event.key == pg.K_RETURN: 
                self.done = True
            else: 
                user_text += event.unicode
        #elif event.type == pg.MOUSEBUTTONDOWN:
        #    self.done = True
    def update(self, screen, dt):
        self.draw(screen)
    def draw(self, screen):
        global result_time
        white = (255, 255, 255)
        green = (0, 255, 0)
        blue = (0, 0, 128)
        yellow = (255,255,0)
        X = 960
        Y = 1000
        pg.display.set_caption('Race Results:')
        if(result_time == 0.0):
          font = pg.font.Font('freesansbold.ttf', 48)
          text1 = font.render('Race Cancelled', True, yellow, blue)
          font = pg.font.Font('freesansbold.ttf', 32)
          #text2 = font.render(str(result_time)+' seconds', True, yellow, blue)
          #font = pg.font.Font('freesansbold.ttf', 20)
          #text3 = font.render('Type your nickname', True, green, blue)
          text4 = font.render('Press [ENTER] to continue', True, green, blue) 
          #font = pg.font.Font('freesansbold.ttf', 48)               
          #text5 = font.render(user_text, True, yellow, blue)
          text1Rect = text1.get_rect()
          #text2Rect = text2.get_rect()
          #text3Rect = text3.get_rect()
          text4Rect = text4.get_rect()
          #text5Rect = text5.get_rect()
          # set the center of the rectangular object.
          text1Rect.center = (X // 2, 1.3*Y // 8)
          #text2Rect.center = (X // 2, 2.2*Y // 8)
          #text3Rect.center = (X // 2, 4.2*Y // 8) 
          text4Rect.center = (X // 2, 4.8*Y // 8)                        
          #text5Rect.center = (X // 2, 6*Y // 8)                        
          screen.fill((0,0,255))    
          screen.blit(text1, text1Rect)
          #screen.blit(text2, text2Rect)
          #screen.blit(text3, text3Rect)                
          screen.blit(text4, text4Rect) 
          #screen.blit(text5, text5Rect)                
        else:
          font = pg.font.Font('freesansbold.ttf', 64)
          text1 = font.render('Your time:', True, yellow, blue)
          font = pg.font.Font('freesansbold.ttf', 64)
          text2 = font.render(str(result_time)+' seconds', True, yellow, blue)
          font = pg.font.Font('freesansbold.ttf', 48)
          text3 = font.render('Type your nickname', True, green, blue)
          text4 = font.render('Press [ENTER] when done', True, green, blue) 
          font = pg.font.Font('freesansbold.ttf', 64)               
          text5 = font.render(user_text, True, yellow, blue)
          text1Rect = text1.get_rect()
          text2Rect = text2.get_rect()
          text3Rect = text3.get_rect()
          text4Rect = text4.get_rect()
          text5Rect = text5.get_rect()
          # set the center of the rectangular object.
          text1Rect.center = (X // 2, 1.3*Y // 8)
          text2Rect.center = (X // 2, 2.2*Y // 8)
          text3Rect.center = (X // 2, 4.2*Y // 8) 
          text4Rect.center = (X // 2, 4.8*Y // 8)                        
          text5Rect.center = (X // 2, 6*Y // 8)                        
          screen.fill((0,0,255))    
          screen.blit(text1, text1Rect)
          screen.blit(text2, text2Rect)
          screen.blit(text3, text3Rect)                
          screen.blit(text4, text4Rect) 
          screen.blit(text5, text5Rect)                

 
# highscores
#   delay, go to instructions

class Highscores(States):
    def __init__(self):
        States.__init__(self)
        self.next = 'instructions'
        global timer_ready        
    def cleanup(self):
        print("("+time.ctime(time.time())+") "+'exiting [Highscores]')
        global user_text
        global result_time
        user_text = ''
        result_time = 0.0        
    def startup(self):
        global scorelines
        print("("+time.ctime(time.time())+") "+'entering [Highscores]')  
        scorelines = open('highscores.txt', 'r').readlines()
        for line in sorted(scorelines, key=lambda line: float(line.split()[0])):  
            print(line.strip())             
    def get_event(self, event):
        if event.type == pg.KEYDOWN:
            print("("+time.ctime(time.time())+") "+'highscores keydown')
            self.done = True
        #elif event.type == pg.MOUSEBUTTONDOWN:
        #    self.done = True
    def update(self, screen, dt):
        self.draw(screen)
    def draw(self, screen):
        white = (255, 255, 255)
        green = (0, 255, 0)
        blue = (0, 0, 128)
        X = 960
        Y = 1000
        pg.display.set_caption('Best Times:')
        font = pg.font.Font('freesansbold.ttf', 48)        
        screen.fill((0,0,255))
        text = font.render('Best Times:', True, green, blue)
        textRect = text.get_rect()
        textRect.topright = (1.3*X // 4, Y // 8)
        screen.blit(text, textRect)
        font = pg.font.Font('freesansbold.ttf', 32)        
        text = font.render('press any key', True, green, blue)
        textRect = text.get_rect()
        textRect.topright = (1.3*X // 4, 2*Y // 8)
        screen.blit(text, textRect)
        text = font.render('to continue', True, green, blue)
        textRect = text.get_rect()
        textRect.topright = (1.3*X // 4, 2.3*Y // 8)
        screen.blit(text, textRect)


        for index, line in enumerate(sorted(scorelines, key=lambda line: float(line.split()[0]))):  
            text = font.render(line.strip(), True, green, blue)
            textRect.topleft = (3*X // 8, Y // 8 + index*40) 
            screen.blit(text, textRect)   
                                        
  
class Control:
    def __init__(self, **settings):
        self.__dict__.update(settings)
        self.done = False
        self.screen = pg.display.set_mode(self.size)
        self.clock = pg.time.Clock()
    def setup_states(self, state_dict, start_state):
        self.state_dict = state_dict
        self.state_name = start_state
        self.state = self.state_dict[self.state_name]
    def flip_state(self):
        self.state.done = False
        previous,self.state_name = self.state_name, self.state.next
        self.state.cleanup()
        self.state = self.state_dict[self.state_name]
        self.state.startup()
        self.state.previous = previous
    def update(self, dt):
        if self.state.quit:
            self.done = True
        elif self.state.done:
            self.flip_state()
        self.state.update(self.screen, dt)
    def event_loop(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.done = True
            self.state.get_event(event)
    def main_game_loop(self):
        while not self.done:
            delta_time = self.clock.tick(self.fps)/1000.0
            self.event_loop()
            self.update(delta_time)
            pg.display.update()

settings = {
    'size':(960,1000),
    'fps' :60,

}
  
app = Control(**settings)
state_dict = {
    'loading': Loading(),
    'instructions': Instructions(),
    'racing': Racing(),
    'results': Results(),
    'highscores': Highscores(),

}
app.setup_states(state_dict, 'loading')
app.main_game_loop()
pg.quit()
sys.exit()