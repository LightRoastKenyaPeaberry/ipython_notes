import sys, random, argparse
import numpy as np
import math
import turtle
from PIL import Image
from datetime import datetime
from math import gcd


# a class that draws a Spirograph
class Spiro:
    # constructor
    def __init__(self, xc, yc, col, R, r, l):
        # create the turtle object
        self.t = turtle.Turtle()
        # set the cursor shape 
        self.t.shape('turtle')

        # set the step in degrees
        self.step =5 
        # set the drawing complete flag
        self.drawingComplete = False

        # set the parameters
        self.setparams(xc,yc,col,R,r,l)

        # initialize the drawing
        self.restart()

    def setparams(self, xc, yc, col, R, r, l):
        # the Spirograph parameters
        self.xc = xc
        self.yc = yc
        self.R = R
        self.r =r
        self.l =l 
        self.col = col
        # reduce r/R to its smallest form by dividing with the GCD
        gcdVal = gcd(self.r, self.R)
        self.nRot = self.r // gcdVal
        # get ratio if radii
        self.k = r/float(R)
        # set the color
        self.t.color(*col)
        # store the current angle
        self.a = 0

    # reset the drawing
    def restart(self):
        # set the flag
        self.drawingComplete = False
        # show the turtle
        self.t.showturtle()
        # go to the first point
        self.t.up()
        R, k, l = self.R, self.k, self.l
        a= 0.0
        x = R*((1-k)*math.cos(a) + l*k*math.cos((1-k)*a/k))
        y = R*((1-k)*math.sin(a) + l*k*math.sin((1-k)*a/k))
        self.t.setpos(self.xc+x, self.yc+y)
        self.t.down()

    # drawing the whole thing
    def draw(self):
        # draw the rest of the points
        R, k, l = self.R, self.k, self.l
        for i in range(0,360*self.nRot+1,self.step):
            a = math.radians(i)
            x = R*((1-k)*math.cos(a) + l*k*math.cos((1-k)*a/k))
            y = R*((1-k)*math.sin(a) + l*k*math.sin((1-k)*a/k))
            self.t.setpos(self.xc+x, self.yc+y)
            self.t.hideturtle()

    # update by one step
    def update(self):
        # skip if drawing is done
        if self.drawingComplete:
            return 
        # increment the angle
        self.a += self.step
        R, k, l = self.R, self.k, self.l
        # draw the step
        a = math.radians(self.a)
        x = R*((1-k)*math.cos(a) + l*k*math.cos((1-k)*a/k))
        y = R*((1-k)*math.sin(a) + l*k*math.sin((1-k)*a/k))
        self.t.setpos(self.xc+x, self.yc+y)
        # if drawing is complete, set the flag
        if self.a >=360*self.nRot:
            self.drawingComplete = True
            self.t.hideturtle()

    def clear(self):
        self.t.clear()


# a class for animating Spirographs
class SpiroAnimator:
    # constructor
    def __init__(self,N):
        # set the timer value in milliseconds
        self.deltaT = 10
        # get the window dimensions
        self.width = turtle.window_width()
        self.height = turtle.window_height()
        # create the Spiro objects 
        self.spiros = []
        for i in range(N):
            # generate radom parameters
            rparams = self.genRandomParams()
            # set the spiro params
            spiro = Spiro(*rparams)
            self.spiros.append(spiro)
            # call timer
            turtle.ontimer(self.update, self.deltaT)

    def restart(self):
        for spiro in self.spiros:
            # clear
            spiro.clear()
            # generate random params
            rparams = self.genRandomParams()
            # set the spiro params
            spiro.setparams(*rparams)
            # restart drawing
            spiro.restart()

    # generate radom parameters
    def genRandomParams(self):
        width, height = self.width, self.height
        R = random.ranint(50, min(width,height)//2)
        r = random.randint(10, 9*R//10)
        l = random.uniform(0.1,0.9)
        xc = random.randint(-width//2, width//2)
        yc = random.randint(-height//2, height//2)
        col = (random.random(),
               random.random(),
               random.random())
        return (xc,yc,col,R,r,l)

    def update(self):
        # update all spiros
        nComplete = 0
        for spiro in self.spiros:
            # update
            spiro.update()
            # count completed spiros
            if spiro.drawingComplte:
                nComplete +=1
        # restart if all spiros are complete
        if nComplete == len(self.spiros):
            self.restart()
        # call the timer
        turtle.ontimer(self.update, self.deltaT)

    # toogle turtle cursor on and off
    def toggleTurtles(self):
        for spiro in self.spiros:
            if spiro.t.isvisivle():
                spiro.t.hideturtle()
            else:
                spiro.t.showturtle()
    
# save drawings as PNG files
def saveDrawing():
    # hide the turtle cursor
    turtle.hideturtle()
    # generate the unique filename
    dateStr = datetime.now().strftime('%y%b%d-%H%M%S')
    fileName = 'spiro'+dateStr
    print(f'saving drawing to {fileName}.eps/png')
    # get the tkinter canvas
    canvas = turtle.getcanvas()
    # save the drawing as a postscript image
    canvas.postscript(file=fileName+'.eps')
    # use PIL to convert the postscript image file to PNG
    img = Image.open(fileName+'.eps')
    img.save(fileName+'.png', 'png')
    # show the turtle cursor
    turtle.showturtle()


def main():
    # use sys.argv if needed
    print('generating spirograph...')
    # create parser
    descStr = '''This program draws Spirographs using the Turtle moudle.
    When run with no arguments, this program draws radom Spirographs
    
    Terminology:
    
    R: radius of outer circle
    r: radius of inner circle
    l: ratio of hole distance to r'''

    parser = argparse.ArgumentParser(description=descStr)
    parser.add_argument('--sparams', nargs=3, dest='sparams', required=False,
                        help='the threee arguments in sparams: R, r, l')
    

