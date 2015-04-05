# -*- coding: utf-8 -*-
from sprites import LittleSprite
from finitestatemachine import * 
import os
import pygame
pfad = os.path.abspath( os.path.join("..", "..", "data"))

brick_alternate = "brick001.png" # "brick_18px.png"
brick = "brick001_radiated.png"  # "brick_18px_radiated.png"

class Boden1(LittleSprite, BodenState):
    coords = None

    alternate_image = pygame.image.load(os.path.join(pfad, brick_alternate))
    image = brick

    def __init__(self, coords):
        self.coords = coords
        LittleSprite.__init__(self, Boden1.image)
        self.rect.inflate_ip(0,-26)
        self.state = BodenState(self)
        
        
    def update(self):
        
        self.rect.centerx = self.game.display.bgpos[0] + self.coords[0]
        self.rect.centery = self.game.display.bgpos[1] + self.coords[1]
        self.game.display.paint_sprite(self)


#
#class Boden2(LittleSprite):
#    coords = None
#
#    def __init__(self, coords):
#        self.coords = coords
#        image = "brick002.png"
#        LittleSprite.__init__(self, image)
#        self.rect = self.rect.inflate(0, -31)
#        self.rect = self.rect.move(0, 31)
#
#
#    def update(self):
#
#        self.rect.centerx = self.display.bgpos[0] + self.coords[0]
#        self.rect.centery = self.display.bgpos[1] + self.coords[1]
#        self.display.paint_sprite(self)



class Leiter(LittleSprite):
    coords = None
    
    def __init__(self, coords):
        self.coords = coords
        image = "leiter001.png"
        LittleSprite.__init__(self, image)
        
    def update(self):
        
        self.rect.centerx = self.game.display.bgpos[0] + self.coords[0]
        self.rect.centery = self.game.display.bgpos[1] + self.coords[1]
        self.game.display.paint_sprite(self)

class Fass(LittleSprite):
    coords = None

    def __init__(self, coords):
        self.coords = coords
        image = "smallbarrel2.png"
        LittleSprite.__init__(self, image)

    def update(self):

        self.rect.centerx = self.game.display.bgpos[0] + self.coords[0]
        self.rect.centery = self.game.display.bgpos[1] + self.coords[1]
        self.game.display.paint_sprite(self)
        
