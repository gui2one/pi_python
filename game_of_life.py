## game of life

import pygame
import math
import random

import sys
sys.path.insert(0,"./wheels")
from gui2oneUI import *


class GOL_grid():
    def __init__(self,size=[20,20]):
        self.size = size
        self.cells = []
        self.cellSize = 8
        
        self.font = pygame.font.Font(pygame.font.get_default_font(),10)

        self.showCellNums = False


    def build(self):
        counter = 0
        for j in range(0,self.size[1]):

            for i in range(0,self.size[0]):

                boolTest = int(random.random() < 0.5)
                
                cell = GOL_cell(boolTest)
                #cell.state = boolTest
                cell.coords = [i,j]
                self.cells.append(cell)

                counter += 1        

        #self.draw()

    def getNumNeighbours(self,cell):
        x = cell.coords[0]
        y = cell.coords[1]
        width = self.size[0]
        height = self.size[1]
        
        curID = (y * width) + x

        ids = []
        ## starting from top left corner , clockwise
        if x > 0 and y > 0 :        ### id 0
            ids.append(curID - width - 1)
        if y > 0 :                  ### id 1
            ids.append(curID - width)
        if x < width-1 and y > 0:   ### id 2
            ids.append(curID - width + 1)
        if x < width-1:             ### id 3
            ids.append(curID + 1)
        if x < width-1 and y < height-1:### id 4
            ids.append(curID + width + 1)
        if y < height-1:            ### id 5
            ids.append(curID + width)
        if x > 0 and y < height-1:  ### id 6
            ids.append(curID + width - 1)
        if x > 0:                   ### id 7
            ids.append(curID - 1)

        cell.numBuddies = 0
        for i in range(0,len(ids)):
            if(self.cells[ids[i]].state == 1):
                cell.numBuddies += 1

                
        return cell.numBuddies


    def checkBuddies(self):
        for i in range(0,len(self.cells)):

            cell = self.cells[i]
            #if i == 6 : print  self.getNumNeighbours(cell)
            numBuddies = self.getNumNeighbours(cell)

            self.cells[i].numBuddies = numBuddies
            
    def update(self):
        for i in range(0,len(self.cells)):

            cell = self.cells[i]

            if cell.state == 1:
                if cell.numBuddies < 2 or cell.numBuddies > 3:
                    cell.state = 0
                elif cell.numBuddies == 2 or cell.numBuddies == 3:
                    pass
            else:
                if cell.numBuddies == 3:
                    cell.state = 1        

    
    def draw(self):
        #print "draw!!!!"
        self.checkBuddies()
        self.update()
        for i in range(0,len(self.cells)):
            cell = self.cells[i]
       
            if cell.state:
                clr = (255,0,0)
            else:
                clr = (20, 20,20)
            pygame.draw.rect(screen, clr,pygame.Rect(cell.coords[0]*self.cellSize,cell.coords[1]*self.cellSize,self.cellSize-2,self.cellSize-2))

            if self.showCellNums:
                textSurface = self.font.render(str(i), True, (255,255,255))
                
                textPosX = cell.coords[0]* self.cellSize
                textPosY = cell.coords[1]* self.cellSize        
                screen.blit(textSurface,(textPosX,textPosY))

                textSurface = self.font.render(str(cell.numBuddies), True, (100,255,100))
                
                textPosX = (cell.coords[0]* self.cellSize)+ 10
                textPosY = (cell.coords[1]* self.cellSize)+ 10
                screen.blit(textSurface,(textPosX,textPosY))

                textSurface = self.font.render(str(cell.coords), True, (255,255,200))
                
                textPosX = (cell.coords[0]* self.cellSize)+ 10
                textPosY = (cell.coords[1]* self.cellSize)+ 25
                screen.blit(textSurface,(textPosX,textPosY))                  
        
class GOL_cell(object):
    def __init__(self, state=1, coords=[0,0]):
        self.state = state
        self.coords = coords
        self.numBuddies = 0




pygame.init()
screen = pygame.display.set_mode((700, 700))


gridSize = 100
grid = GOL_grid([gridSize,gridSize])
grid.cellSize = 6
grid.build()

oldGridString = ''
for cell in grid.cells: oldGridString += str(cell.state)


pygame.display.set_caption("Game Of Life")
ui = gui2oneUI(screen)

text1 = StaticText(screen,20,650,50,50)
ui.addItem(text1)

resetBtn = Button(screen, 100,650,50,50, "Reset")



def my_callback_func(event):
    print dir(event.source)
    print event.source.__reduce__()
    pass
    # do stuff

def resetFunction():
    #GOL_grid.__init__()
    print "shitt !!"
    pass
    
o = Observable()
o.subscribe(my_callback_func)
    
resetBtn.setCallback(resetFunction.__code__)

ui.addItem(resetBtn)
clock = pygame.time.Clock()
done = False



frameCounter = 0
grid.draw()
while not done:
    newString = ''
    if frameCounter % 2 == 0 :
        for cell in grid.cells: newString += str(cell.state)
        if oldGridString == newString:
            print "Done !!!!!!!"
            done = True
        else:
            oldGridString = newString
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print event
            pygame.quit()

##        if event.type == pygame.MOUSEBUTTONDOWN:
##            grid.draw()
##            #print counter
            
    
    
    
    grid.draw()
    text1.text = str(frameCounter)
    ui.eventUpdate()
    ui.draw()
    frameCounter += 1
    pygame.display.flip()
    clock.tick(60)
