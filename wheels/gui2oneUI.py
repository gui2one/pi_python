import math
import pygame

def roundValue(value, decimals = 1):
    return math.floor(value * (10 ** (decimals+1)))/ float(10 ** (decimals+1))

class Event(object):
    def __init__(self):
        pass

class Observable(object):
    def __init__(self):
        self.callbacks = []
    def subscribe(self, callback):
        self.callbacks.append(callback)
        self.fire()
    def fire(self, **attrs):
        e = Event()
        #print "event -->", dir(e)
        e.source = self
        for k, v in attrs.iteritems():
            setattr(e, k, v)
        for fn in self.callbacks:
            fn(e)

class gui2oneUI(object):
    def __init__(self, screen):
        self.items = []
        self.screen = screen
        self.draggedItem = None

    def addItem(self,item):
        
        if type(item).__name__ == "Slider" :

            #append empty slider container to keep data
            self.items.append(item)
            
            sliderLine = Line( item.screen, item.position[0], item.position[1], item.size[0],2, item.name)
            sliderLine.color = pygame.Color("gray")
            self.items.append(sliderLine)


            
            sliderButton = Button(item.screen, item.position[0], item.position[1]-6, 12,12,"")
            sliderButton.dragLimits = pygame.Rect(item.position[0], item.position[1], item.size[0],20)
            
            sliderButton.position[0] = (item.defaultValue *  item.size[0] ) + item.position[0]
            sliderButton.draggable = True
            sliderButton.parentItem = item
            self.items.append(sliderButton)
        else:
            self.items.append(item)

    def draw(self):
        for item in self.items:
            item.draw()
            
    def eventUpdate(self):
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
##                print pygame.event.event_name(event.type)
            for item in self.items:

                if item.draggable:
                     
                    if self.draggedItem == None or item == self.draggedItem:
                        if event.type == pygame.MOUSEMOTION and event.buttons[0] == 1 and item.pressed(pygame.mouse.get_pos()) and not item.isDragged:
                            #print "Drag !!!", item.name, event.rel
                            item.isDragged = True
                            
                            if self.draggedItem == None :
                                self.draggedItem = item
                                #print self.draggedItem
                            
                        elif event.type == pygame.MOUSEMOTION and event.buttons[0] == 1  and item.isDragged:
                            if item == self.draggedItem:                    
                                if item.dragDir == "horizontal" :

                                    item.position = [item.position[0]+event.rel[0], item.position[1]]
                                    if item.parentItem != None :
                                        item.parentItem.value = item.getValue()
                                        #print item.parentItem.value
                                    
                                    if item.position[0] < item.dragLimits.left:
                                        item.position[0] = item.dragLimits.left
                                    elif item.position[0] > item.dragLimits.right:
                                        item.position[0] = item.dragLimits.right
                                        
                                elif item.dragDir == "vertical":
                                    item.position = [item.position[0], item.position[1]+event.rel[1]]

                                    if item.position[1] < item.dragLimits.top:
                                        item.position[1] = item.dragLimits.top
                                    elif item.position[1] > item.dragLimits.bottom:
                                        item.position[1] = item.dragLimits.bottom                                    
                        else :
                            item.isDragged = False
                            self.draggedItem = None
                                                        
            if type(item).__name__ == "Button" and event.type == pygame.MOUSEBUTTONDOWN and item.pressed(pygame.mouse.get_pos()) :
                item.callback()
                pass
                    
                
class uiItem(object):
    def __init__(self,screen,x,y,width, height,name,defaultValue,draggable,dragDir):
        #self.myProp = prop
        self.name = name
        self.screen = screen
        self.draggable = draggable
        self.dragDir = dragDir
        self.isDragged = False
        self.position = [x,y]
        self.size = [width,height]
        self.rect = pygame.Rect(self.position[0],self.position[1],self.size[0],self.size[1])
        self.dragLimits = self.rect
        self.parentItem = None

        self.font = pygame.font.Font(pygame.font.get_default_font(),18)
        self.fontScale = 1.0
        
        self.defaultValue = defaultValue
        self.value = self.defaultValue
        self.callbackString = ""

    def setSize(self, width , height):
        self.size = [width,height]

    def getValue(self):
        
        val = (self.position[0] - self.dragLimits.left) / float(self.dragLimits.right - self.dragLimits.left)
        if val < 0.0 :val = 0.0
        elif val > 1.0:val = 1.0
        
        self.value = val
        return val
    def setCallback(self,func):
        
        self.callbackString = func

    def callback(self):

        exec self.callbackString

class StaticText(uiItem):
    def __init__(self, screen, x,y,width, height,name="item_name",defaultValue=0.0 , draggable=False, dragDir="horizontal"):
        uiItem.__init__(self,screen,x,y,width, height,name,defaultValue,draggable=False, dragDir="horizontal")
        self.text = 'wxcwxc'
        
    def draw(self):
        
        textSurface = self.font.render(self.text, True, (255,255,255))
        #textSurface.transform.move(20,20)
        textPosX = self.rect.left
        textPosY = self.rect.top-30        
        self.screen.blit(textSurface,(textPosX,textPosY))  

class Line(uiItem):
    def __init__(self, screen, x,y,width, height,name="item_name",defaultValue=0.0 , draggable=False, dragDir="horizontal"):
        uiItem.__init__(self,screen,x,y,width, height,name,defaultValue,draggable=False, dragDir="horizontal")
        self.color = (55,55,55)
        

    def draw(self):
        self.rect = pygame.Rect(self.position[0],self.position[1],self.size[0],self.size[1])
        pygame.draw.rect(self.screen, self.color, self.rect)
        
        textSurface = self.font.render(self.name, True, (255,255,255)) 
        textPosX = self.rect.left
        textPosY = self.rect.top-30
        
        self.screen.blit(textSurface,(textPosX,textPosY))        
        
class Slider(uiItem):
    def __init__(   self, screen,x,y,width, height,name="item_name",defaultValue=0.0,draggable=False,dragDir="horizontal"):
        
        uiItem.__init__(self,screen,
                        x,y,
                        width, height, 
                        name,
                        defaultValue, 
                        draggable=False, 
                        dragDir="horizontal")
        self.color = pygame.Color("#555555")
        

        
    def draw(self):
        
        textSurface = self.font.render(str(roundValue(self.value)), True, (255,255,255))

        textPosX = self.rect.right+15
        textPosY = self.rect.top-7
        self.screen.blit(textSurface,(textPosX,textPosY))   

 
        
class Button(uiItem):
    
    def __init__(self, screen, x,y,width, height,name="item_name", defaultValue=0.0,draggable=False, dragDir="horizontal"):
        uiItem.__init__(self,screen,x,y,width, height, name, defaultValue,draggable=False, dragDir="horizontal")
        #self.screen = screen
        self.color = (255,20,20)        
        self.text = self.name

    
    def draw(self):
        self.rect = pygame.Rect(self.position[0],self.position[1],self.size[0],self.size[1])
        pygame.draw.rect(self.screen, self.color,self.rect)
        
        
        textSurface = self.font.render(self.text, True, (255,255,255))        
        textPosX = self.rect.centerx - (textSurface.get_width()/2.0)
        textPosY = self.rect.centery - (textSurface.get_height()/2.0)
        
        self.screen.blit(textSurface,(textPosX,textPosY))

    def pressed(self,mouse):
        if mouse[0] > self.rect.topleft[0]:
            if mouse[1] > self.rect.topleft[1]:
                if mouse[0] < self.rect.bottomright[0]:
                    if mouse[1] < self.rect.bottomright[1]:

                        return True
                        
                    else:                        
                        return False
                else:                   
                    return False
            else:                
                return False
        else:            
            return False



def main():
    if(__name__ != "__main__"):
        main()

    
