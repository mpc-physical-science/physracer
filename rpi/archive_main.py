# Simple pygame program

# Import and initialize the pygame library
import pygame as pg
import serial
import sys
import glob
import re
from threading import Thread

timer_ready = False;
last_serial_message = "";
result_time = 0.0;
user_text = ''

ser = serial.Serial('/dev/tty.usbmodem126912001', 9600, timeout=0)
def worker():

   global timer_ready
   global last_serial_message
   while True:
     msg = ser.readline()
     if len(msg) > 0:
      print("Message Received: %s" % msg.decode())
      last_serial_message = msg.decode()
     if msg == "busy\n":
      timer_ready=False
     elif msg == "ready\n":
      timer_ready=True 

print("timer ready:")
print(timer_ready)  

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
        ports = glob.glob('/dev/tty.*')
        print('Serial Ports:')
        print(ports)
        global timer_ready        
    def cleanup(self):
        print('cleaning up loading state stuff')
    def startup(self):
        print('starting loading state stuff')
    def get_event(self, event):
        if event.type == pg.KEYDOWN:
            print('loading keydown')
        elif event.type == pg.MOUSEBUTTONDOWN:
            self.done = True
    def update(self, screen, dt):
        self.draw(screen)
    def draw(self, screen):
        white = (255, 255, 255)
        green = (0, 255, 0)
        blue = (0, 0, 128)
        X = 600
        Y = 400
        pg.display.set_caption('Physics Racer')
        font = pg.font.Font('freesansbold.ttf', 64)
        font.set_italic(True)
        text = font.render('Physics Racer', True, green, blue)
        textRect = text.get_rect()
        # set the center of the rectangular object.
        textRect.center = (X // 2, Y // 2)
        screen.fill((0,0,255))    
        screen.blit(text, textRect)        

# instructions
#   check race started

class Instructions(States):
    def __init__(self):
        States.__init__(self)
        self.next = 'racing'
        global timer_ready        
    def cleanup(self):
        print('cleaning up Instructions state stuff')
        print("timer ready:")
        print(timer_ready)        
    def startup(self):
        print('starting Instructions state stuff')
        print("timer ready:")
        print(timer_ready)        
    def get_event(self, event):
        if event.type == pg.KEYDOWN:
            print('Instructions keydown')
        elif event.type == pg.MOUSEBUTTONDOWN:
            self.done = True
    def update(self, screen, dt):
        if last_serial_message=='race started!\r\n':
            self.done = True
        self.draw(screen)
    def draw(self, screen):
        global settings
        white = (255, 255, 255)
        green = (0, 255, 0)
        blue = (0, 0, 128)
        yellow = (255,255,0)        
        X = 600
        Y = 400
        pg.display.set_caption('Instructions')
        font = pg.font.Font('freesansbold.ttf', 48)
        text1 = font.render('Instructions', True, green, blue)
        font = pg.font.Font('freesansbold.ttf', 20)
        text2 = font.render('1. Build a LEGO racecar', True, green, blue)
        text3 = font.render('2. Race it down the ramp!', True, green, blue)
        text4 = font.render('Your race time will be automatically measured', True, green, blue)
        font.set_italic(True)        
        text5 = font.render('Good luck! May the mass*acceleration be with you', True, yellow, blue)
        text1Rect = text1.get_rect()
        text2Rect = text2.get_rect()
        text3Rect = text3.get_rect()
        text4Rect = text4.get_rect()
        text5Rect = text5.get_rect()        
        # set the center of the rectangular object.
        text1Rect.center = (X // 2, 1*Y // 6)
        text2Rect.center = (X // 2, 2.3*Y // 6)
        text3Rect.center = (X // 2, 3*Y // 6)
        text4Rect.center = (X // 2, 3.7*Y // 6)
        text5Rect.center = (X // 2, 5*Y // 6)        
        screen.fill((0,0,255))    
        screen.blit(text1, text1Rect)
        screen.blit(text2, text2Rect)
        screen.blit(text3, text3Rect)
        screen.blit(text4, text4Rect)
        screen.blit(text5, text5Rect)        

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
        print('cleaning up Racing state stuff')
        print(result_time)
        print(last_serial_message)        
        print("timer ready:")
        print(timer_ready)                 
    def startup(self):
        print('starting Racing state stuff')
        print("timer ready:")
        print(timer_ready)                 
    def get_event(self, event):
        if event.type == pg.KEYDOWN:
            print('Racing keydown')
        elif event.type == pg.MOUSEBUTTONDOWN:
            self.done = True
    def update(self, screen, dt):
        global result_time
        global last_serial_message
        try:
            t_index = last_serial_message.index("t=")
            print(last_serial_message.index("t="))
            str=''
            result_time=float(str.join(re.findall("\d+\.\d+",last_serial_message)))
            print(result_time)
            print(last_serial_message)
            self.done = True
        except ValueError:
            t_index = -1
        self.draw(screen)
    def draw(self, screen):
        white = (255, 255, 255)
        green = (0, 255, 0)
        blue = (0, 0, 128)
        X = 600
        Y = 400
        pg.display.set_caption('Race Underway!')
        font = pg.font.Font('freesansbold.ttf', 32)
        text = font.render('Race Underway!', True, green, blue)
        textRect = text.get_rect()
        # set the center of the rectangular object.
        textRect.center = (X // 2, Y // 2)
        screen.fill((0,0,255))    
        screen.blit(text, textRect)
   

# results
#   enter name
#   display ranking

class Results(States):
    def __init__(self):
        States.__init__(self)
        self.next = 'highscores'
        global result_time
        global last_serial_message
        print("timer ready:")
        print(timer_ready)        
    def cleanup(self):
        print('cleaning up Results state stuff')  
        with open('highscores.txt', 'a') as highscores_file:
            highscores_file.write(str(result_time) + ' ' + user_text + '\n')       
    def startup(self):
        global timer_ready 
        print('starting Results state stuff')
        print("timer ready:")
        print(timer_ready)         
        try:
            t_index = last_serial_message.index("t=")
            print(last_serial_message.index("t="))
            str=''
            result_time=float(str.join(re.findall("\d+\.\d+",last_serial_message)))
            print(result_time)
            print(last_serial_message)
        except ValueError:
            t_index = -1
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
        elif event.type == pg.MOUSEBUTTONDOWN:
            self.done = True
    def update(self, screen, dt):
        self.draw(screen)
    def draw(self, screen):
        global result_time
        white = (255, 255, 255)
        green = (0, 255, 0)
        blue = (0, 0, 128)
        yellow = (255,255,0)
        X = 600
        Y = 400
        pg.display.set_caption('Race Results:')
        font = pg.font.Font('freesansbold.ttf', 32)
        text1 = font.render('Your time:', True, yellow, blue)
        font = pg.font.Font('freesansbold.ttf', 48)
        text2 = font.render(str(result_time)+' seconds', True, yellow, blue)
        font = pg.font.Font('freesansbold.ttf', 20)
        text3 = font.render('Type your nickname', True, green, blue)
        text4 = font.render('Press [ENTER] when done', True, green, blue) 
        font = pg.font.Font('freesansbold.ttf', 48)               
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
        print('cleaning up highscores state stuff')
        global user_text
        global result_time
        user_text = ''
        result_time = 0.0
        print("timer ready:")
        print(timer_ready)         
    def startup(self):
        print('starting highscores state stuff')
        print("timer ready:")
        print(timer_ready)          
    def get_event(self, event):
        if event.type == pg.KEYDOWN:
            print('highscores keydown')
        elif event.type == pg.MOUSEBUTTONDOWN:
            self.done = True
    def update(self, screen, dt):
        self.draw(screen)
    def draw(self, screen):
        white = (255, 255, 255)
        green = (0, 255, 0)
        blue = (0, 0, 128)
        X = 600
        Y = 400
        pg.display.set_caption('Best Times:')
        font = pg.font.Font('freesansbold.ttf', 32)
        text = font.render('Best Times:', True, green, blue)
        textRect = text.get_rect()
        # set the center of the rectangular object.
        textRect.center = (X // 2, Y // 2)
        screen.fill((0,0,255))    
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
    'size':(600,400),
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