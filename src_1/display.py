# -*- coding: utf-8 -*-
import pygame
import copy
import os

class Display():

    def __init__(self):
        pygame.init()
#        self.arena = [400,300]
        self.arena = [400,400]
        self.arena = [640,480]
#        self.arena = [1024,768]
        self.screen = pygame.display.set_mode(self.arena)
        pfad =  os.path.abspath( os.path.join('..', '..', 'data') )
        self.bg = pygame.image.load( os.path.join(pfad, "bg06.png") )
        self.bg = self.bg.convert()
        self.bgmax = self.bg.get_size()
        self.bgdim = self.bg.get_rect()
        self.bgpos = [0,-1200]
        self.bg_oldpos = [None, None]



    def paint_background(self, dirty):
        # @TODO: Limit Background Image blitting to visible Area plus some pixels ...
        bgclip = [self.bgpos[0], self.bgpos[1], self.arena[0], self.arena[1]]
        self.bg.set_clip(bgclip)
        d = self.screen.blit(self.bg, self.bgpos)
        # check wether background was "moved"
        if self.bg_oldpos[0] != self.bgpos[0] \
        or self.bg_oldpos[1] != self.bgpos[1]:
            dirty.insert(len(dirty), d)
            self.bg_oldpos = copy.copy(self.bgpos)



    def paint_sprite(self, sprite):
        dirty_rect = self.screen.blit( sprite.image, sprite.rect )
        dirty_rect = dirty_rect.inflate(8,8)
        return dirty_rect