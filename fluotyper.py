#sketch.py
add_library('Minim')
from letter import Letter
import cfg

letters = []

def setup():
    global typeSound, errSound, appSound
    size(600, 600)
    background(220)
    textSize(32)
    
    minim = Minim(this)
    typeSound = minim.loadSample("type.mp3")
    errSound = minim.loadSample("ComputerErrorAlert.mp3")
    appSound = minim.loadSample("07073021.wav")
    
def draw():
    if (cfg.light):
        background(random(256), random(256), random(256))
        cfg.lightCnt += 1
        if (cfg.lightCnt > 30):
            cfg.light = False
            cfg.lightCnt = 0
    else:
        background(220)    
    
    for i in range(len(letters)):
        letters[i].display()
        letters[i].update()
    
    fill(0)
    text(cfg.score, width - 100, 32)
    
    # add letters
    while(len(letters) < cfg.maxSize):
        addRandomLetter()
        
    # level check
    if (frameCount % 60 == 0):
        for i in range(len(letters)):
            if (letters[i].onScreen()):
                break
            if (i == len(letters) - 1):
                cfg.maxSize += 1
                print(cfg.maxSize)
                appSound.trigger()
                
    
def addRandomLetter():
    letters.append(Letter(unichr(97 + random(26)), random(width-32), random(-200, -50), color(random(256), random(256), random(256))))
    
    
def keyTyped():
    typeCorrect = False
    for i in range(len(letters)-1, -1,-1):
        if (letters[i].ch == key):
            del letters[i]
            cfg.score += 1
            typeSound.trigger()
            typeCorrect = True

    if (not typeCorrect):
        errSound.trigger()
        
#cfg.py
maxSize = 3
score = 0
life = 3

light = False
lightCnt = 0

#letter.py
import cfg

class Letter():
    
    def __init__(self, ch, x, y, col):
        self.ch = ch
        self.x = x
        self.y = y
        self.col = col
        
    def display(self):
        fill(self.col)
        text(self.ch, self.x, self.y)
        
    def update(self):
        global life
        self.y += 1
        
        if (self.y > height):
            self.y = 0
            
            cfg.life -= 1
            cfg.light = True
            if (cfg.life == 0):
                noLoop()
                
    def onScreen(self):
        if (self.y > 0):
            return(True)
        else:
            return(False)
