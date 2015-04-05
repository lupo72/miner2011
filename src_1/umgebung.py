# -*- coding: utf-8 -*-
from sprites import LittleSprite
#import copy
import pygame


class Boden1(LittleSprite):
    coords = None
    
    def __init__(self, coords):
        self.coords = coords
        image = "brick001.png"
        LittleSprite.__init__(self, image)
        self.rect.inflate_ip(0,-26)
        #self.rect = self.rect.move(0,0)
        
        
    def update(self):
        
        self.rect.centerx = self.display.bgpos[0] + self.coords[0] 
        self.rect.centery = self.display.bgpos[1] + self.coords[1]
        self.display.paint_sprite(self)



class Boden2(LittleSprite):
    coords = None
    
    def __init__(self, coords):
        self.coords = coords
        image = "brick002.png"
        LittleSprite.__init__(self, image)
        self.rect = self.rect.inflate(0, -31)
        self.rect = self.rect.move(0, 31)
        
        
    def update(self):
        
        self.rect.centerx = self.display.bgpos[0] + self.coords[0] 
        self.rect.centery = self.display.bgpos[1] + self.coords[1]
        self.display.paint_sprite(self)



class Leiter(LittleSprite):
    coords = None
    
    def __init__(self, coords):
        self.coords = coords
        image = "leiter001.png"
        LittleSprite.__init__(self, image)
        
    def update(self):
        
        self.rect.centerx = self.display.bgpos[0] + self.coords[0] 
        self.rect.centery = self.display.bgpos[1] + self.coords[1]
        self.display.paint_sprite(self)

class Fass(LittleSprite):
    coords = None

    def __init__(self, coords):
        self.coords = coords
        image = "smallbarrel2.png"
        LittleSprite.__init__(self, image)

    def update(self, parent):

        self.rect.centerx = self.display.bgpos[0] + self.coords[0]
        self.rect.centery = self.display.bgpos[1] + self.coords[1]
        self.display.paint_sprite(self)
        
        if pygame.sprite.collide_rect( self, parent.player.feet() ) and parent.player.state.falling :
            parent.player.state.change_to_standing(parent)

#        if pygame.sprite.collide_rect(self, parent.player ) and parent.player.state.standing :
#            if self.rect.left < parent.player.rect.left:
#                print "blocking left"
#            elif self.rect.left > parent.player.rect.left:
#                print "blocking right"
    