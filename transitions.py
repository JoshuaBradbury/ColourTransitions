from tkinter import *
from datetime import datetime

class Colour:
    def __init__(self, red, green, blue, loop=False):
        self.red = red
        self.green = green
        self.blue = blue
        self.backupQueue = []
        self.transitionQueue = []
        self.transTime = 0
        self.transRed = 0
        self.transGreen = 0
        self.transBlue = 0
        self.loop = loop

    def setRed(self, red):
        self.red = red

    def setGreen(self, green):
        self.green = green

    def setBlue(self, blue):
        self.blue = blue

    def update(self):
        if self.transTime > 0:
            self.transTime -= 1
            self.red += self.transRed
            self.green += self.transGreen
            self.blue += self.transBlue
        else:
            if len(self.transitionQueue) > 0:
                self.linearTransition(self.transitionQueue[0][0], self.transitionQueue[0][1])
                self.transitionQueue.remove(self.transitionQueue[0])
            elif self.loop:
                for transition in self.backupQueue:
                    self.transitionQueue.append(transition)
                
    def queueTransition(self, toCol, time):
        self.transitionQueue.append([toCol, time])
        self.backupQueue.append([toCol, time])
    
    def linearTransition(self, toCol, time):
        self.transTime = time
        self.transRed = (toCol.red - self.red) / time
        self.transGreen = (toCol.green - self.green) / time
        self.transBlue = (toCol.blue - self.blue) / time

    def getColour(self):
        redStr = hex(int(self.red))[2:]
        greStr = hex(int(self.green))[2:]
        bluStr = hex(int(self.blue))[2:]
        return "#" + "0" * (2 - len(redStr)) + redStr + "0" * (2 - len(greStr)) + greStr + "0" * (2 - len(bluStr)) + bluStr

t = Tk()
t.title("Colour Transitions")
t.resizable(False, False)
c = Canvas(t, width=720, height=480, bg="#ffffff")
c.pack()

colour = Colour(255, 0, 0, True)

colour.queueTransition(Colour(0, 255, 0), 255)
colour.queueTransition(Colour(0, 0, 255), 255)
colour.queueTransition(Colour(255, 0, 0), 255)

oldTime = datetime.now().timestamp()
currTime = datetime.now().timestamp()

while True:
    currTime = datetime.now().timestamp()
    if datetime.fromtimestamp(currTime - oldTime).microsecond > 10000:
        oldTime = currTime
        c.delete("all")
        colour.update()
        c.create_rectangle(0, 0, 720, 480, fill=colour.getColour(), outline=colour.getColour())
        c.update()
        t.update()
