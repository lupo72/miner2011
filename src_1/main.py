#!/usr/bin/local/python
import pygame
from pygame.locals import *
import random
import sys
from charactor_sprite import Charactor
from meanie_sprite import Meanie
from display import Display
from umgebung import Boden1, Boden2, Leiter, Fass
from hud import Hud
FPS = 120

class BasicMovement(Display):
    
    def __init__(self):
    
        self.framerate = 0 
        self.number_meanies = 16
        
        self.display = Display()
        self.hud = Hud()
        self.meanie_list = []
        pygame.key.set_repeat(100,5)
        self.meanies = pygame.sprite.Group()
        
        self.player = Charactor("held.png", self.display)
        self.player.speed = 2
       
        self.init_floors()
        self.init_ladders()
        self.barrels = pygame.sprite.Group()

        self.init_barrels()
        
        self.testgroup = pygame.sprite.Group()
        self.init_meanies(0)
        
        
    def init_floors(self):
        
        self.steine = pygame.sprite.Group()
        
        c = 0
        for y in range (300, self.display.bgmax[1], 200):

            if  c % 2 == 0:
                for x in range(self.display.bgmax[0]/2 + 64, self.display.bgmax[0], 32):
                    
                    s = Boden1([x,y])
                    self.steine.add(s)
            else:
                for x in range(64, self.display.bgmax[0]/2, 32):
                    
                    s = Boden1([x,y])
                    self.steine.add(s)
            
            c += 1
        
        del c

        ## Place a Floor at bottom of level
        for x in range(0,self.display.bgmax[0],32):
            s = Boden1([x, self.display.bgmax[1]-16])
            self.steine.add(s)


    def init_ladders(self):
        self.ladders = pygame.sprite.Group()
        
        for x in range(50, 700, 500):
            
            for y in range(0, self.display.bgmax[1], 32):
                
                i = Leiter([x,y])
                self.ladders.add(i)
        

    def init_barrels(self):

        for y in range(87, self.display.bgmax[1], 200):

            x = random.randint(0, self.display.bgmax[0])

            s = Fass([200, y])
            self.barrels.add(s)


    def init_meanies(self, counter):

        move_index = 0
        while counter < self.number_meanies:

            mx = random.randint( 0, self.display.bgmax[0]-40 )
            my = random.randint( 0, self.display.bgmax[1]-40 )

            meanie = Meanie()
            meanie.state.set_random_move_index()
            meanie.rect.center = mx,my
            self.testgroup.add(meanie)

            if meanie.overlaps(self.testgroup):
                self.testgroup.remove(meanie)
                meanie.kill()
                self.init_meanies(counter)
            else:
                self.meanie_list.insert(counter,meanie)
                self.meanies.add(self.meanie_list[counter])
                counter += 1

        if counter == self.number_meanies:
            self.start_game()


    def start_game(self):
        del self.testgroup
        self.gameRunning = True
        self.mainloop()

    def mainloop(self):
        self.clock = pygame.time.Clock()
        self.player.rect.center = [120,220]

        while self.gameRunning:

            dirty = []
            
            self.clock.tick(FPS)
            self.framerate = self.clock.get_fps()

            self.display.paint_background(dirty)

            self.player.state.set_current_state(self)

            # blit player on screen
            d = self.display.paint_sprite(self.player)
            dirty.insert(len(dirty), d)
            
            self.steine.update()
            self.ladders.update()
            self.barrels.update(self)
            self.meanies.update(self, dirty)
            self.hud.showinfo(self, dirty)

            for e in pygame.event.get():

                if e.type == QUIT:
                    self.gameRunning = False
                    pygame.quit()
                    sys.exit()
                elif e.type == KEYDOWN:
                    
                    if e.key == K_ESCAPE:
                        self.gameRunning = False
                        pygame.quit()
                        sys.exit()
                    elif e.key == K_UP and self.player.state.climbing:
                        self.player.movement[1]= - self.player.speed
                            
                    elif e.key == K_DOWN and not self.player.state.falling and self.player.state.climbing:
                        self.player.movement[1]= self.player.speed
                        
                    elif e.key == K_LEFT:
                        if self.player.state.falling:
                            self.player.movement[0] = - self.player.speed/2
                        else:
                            self.player.movement[0] = - self.player.speed
                        
                    elif e.key == K_RIGHT:  
                        if self.player.state.falling:
                            self.player.movement[0] = self.player.speed/2
                        else:
                            self.player.movement[0] = self.player.speed
                
                elif e.type == KEYUP:
                    if e.key == K_UP or e.key == K_DOWN:
                        self.player.movement[1] = 0
                    elif e.key == K_LEFT or e.key == K_RIGHT:
                        self.player.movement[0] = 0

            self.player.update(self)
            pygame.display.update(dirty)


BasicMovement()
