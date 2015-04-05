#!/usr/bin/local/python
import pygame
import random
from pygame.locals import *

from charactor_sprite import Charactor
#from meanie_sprite import Meanie
from display import Display
from controller import Controller
from hud import Hud
from levels import Level
FPS = 120

class Game(Display, Controller):
    
    def __init__(self):

        self.framerate = 0 
        self.number_meanies = 32
        self.bricks_in_level = 0
        self.display = Display()
        self.hud = Hud()
        pygame.key.set_repeat(100,5)
        self.meanies = pygame.sprite.Group()
        
        self.player = Charactor(self)
        self.player.speed = 2
       
        self.level = Level(self)

        self.level.load_level(0)
        self.start_game()
        
#        self.testgroup = pygame.sprite.Group()
#        self.init_meanies(0)
        
        


#    def init_meanies(self, counter):
#
#        while counter < self.number_meanies:
#
#            mx = random.randint( 0, self.display.bgmax[0]-40 )
#            my = random.randint( 0, self.display.bgmax[1]-40 )
#
#            meanie = Meanie()
#            meanie.state.set_random_move_index()
#            meanie.rect.center = mx,my
#            self.testgroup.add(meanie)
#
#            if meanie.overlaps(self.testgroup):
#                self.testgroup.remove(meanie)
#                meanie.kill()
#                self.init_meanies(counter)
#            else:
#                self.meanies.add(meanie)
#                counter += 1
#
#        if counter == self.number_meanies:
#            self.start_game()


    def start_game(self):

        self.gameRunning = True
        self.mainloop()

    def mainloop(self):
        self.clock = pygame.time.Clock()
        self.player.rect.center = [self.display.arena[0]/2, self.display.arena[1]/2]
        controller = Controller()
        while self.gameRunning:

            dirty = []
            
            self.clock.tick(FPS)
            self.framerate = self.clock.get_fps()

            self.display.paint_background(dirty)
            self.player.state.set_current_state(self)
            d = self.display.paint_sprite(self.player)
            dirty.insert(len(dirty), d)

            self.steine.update()
            self.ladders.update()
            self.barrels.update()
            self.meanies.update(dirty)

            self.hud.showinfo(self, dirty)
            controller.handle_keyboard_input(self.player)
            self.player.update()
            pygame.display.update(dirty)


Game()
