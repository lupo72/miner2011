# -*- coding: utf-8 -*-
import pygame
import copy
import os

class Display():

    def __init__(self):
        pygame.init()
#        self.arena = [400,300]
        self.arena = [400,400]
        self.arena = [640, 480]
#        self.arena = [1024,768]
        self.screen = pygame.display.set_mode(self.arena)
        pfad = os.path.abspath(os.path.join('..', '..', 'data'))
        self.bg = pygame.image.load(os.path.join(pfad, "bg05.png"))
        self.bg = self.bg.convert()
        self.bgmax = self.bg.get_size()
        self.bgdim = self.bg.get_rect()
        self.bgpos = [0, -60]
        self.bg_oldpos = [None, None]


    def paint_background(self, dirty):
        
#        bgclip = [self.bgpos[0], self.bgpos[1], self.arena[0], self.arena[1]]
        bgclip = [ self.bgpos, self.arena ]
        self.bg.set_clip(bgclip)
        d = self.screen.blit(self.bg, self.bgpos)

        if self.bg_oldpos[0] != self.bgpos[0] \
        or self.bg_oldpos[1] != self.bgpos[1]:
            dirty.insert(len(dirty), d)
            self.bg_oldpos = copy.copy(self.bgpos)


    def paint_sprite(self, sprite):
        dirty_rect = self.screen.blit(sprite.image, sprite.rect)
        dirty_rect = dirty_rect.inflate(8, 8)
        return dirty_rect



    def move_arena_horizontal(self, movement=[], hspeed=2):
        screen_right  = - self.bgmax[0] + self.arena[0]
        player_movable_x = True
        
        if self.bgpos[0] > screen_right and movement[0] > 0:
            self.bgpos[0] -= hspeed
            player_movable_x = False
        elif self.bgpos[0] < 0 and movement[0] < 0:
            self.bgpos[0] += hspeed
            player_movable_x = False

        return player_movable_x

    def move_arena_vertikal(self, movement=[], vspeed = 2):
        player_movable_y = True
        
        screen_bottom = - self.bgmax[1] + self.arena[1]

        if self.bgpos[1] > screen_bottom and movement[1] > 0:
            self.bgpos[1] -= vspeed
            player_movable_y = False
        elif self.bgpos[1] < 0 and movement[1] < 0:
            self.bgpos[1] += vspeed
            player_movable_y = False

        return player_movable_y
