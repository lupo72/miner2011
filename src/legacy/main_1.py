#!/usr/bin/local/python
import pygame
from pygame.locals import *
import math
import random
import sys
import copy
from charactor_sprite import Charactor
from meanie_sprite import Meanie
from display import Display
from umgebung import Boden, Leiter

_MIN_TICKS_ = 100

class BasicMovement(Display):
    
    def __init__(self):
    
        self.number_meanies = 70
        
        self.display = Display()
        self.move_schedule = dict()
        self.move_schedule[0] = [-1,0]
        self.move_schedule[1] = [0,-1]
        self.move_schedule[2] = [1,0]
        self.move_schedule[3] = [0,1]
        self.meanies = []
        
        
        pygame.key.set_repeat(100,5)
        
        self.solidgroup = pygame.sprite.Group()

        self.player = Charactor("sprite01.png", self.display)
        self.player.speed = 2
#        self.cloud = LittleSprite("wolke01.png")
#        self.cloud.movement = [1,0]
#        self.cloud.speed = 1
#        self.cloud.rect.center = [50,50]

        
        self.init_floors()
        self.init_ladders()
        self.testgroup = pygame.sprite.Group()
        self.init_meanies(0)
        
        
    def init_floors(self):
        
        self.steine = pygame.sprite.Group()
        
        c = 0
        for y in range (300, self.display.bgmax[1], 200):
            
            if  c % 2 == 0:
                for x in range(self.display.bgmax[0]/2 + 16, self.display.bgmax[0], 32):
                    
                    s = Boden([x,y])
                    self.steine.add(s)
            else:
                for x in range(0, self.display.bgmax[0]/2, 32):
                    
                    s = Boden([x,y])
                    self.steine.add(s)
            
            c += 1
            
        del c
        

    def init_ladders(self):
        self.ladders = pygame.sprite.Group()
        
        for x in range(50, 700, 500):
            
            for y in range(0, self.display.bgmax[1], 32):
                
                i = Leiter([x,y])
                self.ladders.add(i)
        


    def init_meanies(self, counter):

        move_index = 0
        while counter < self.number_meanies:

            mx = random.randint( 0, self.display.bgmax[0]-40 )
            my = random.randint( 0, self.display.bgmax[1]-40 )

            meanie = Meanie("meanie1.png")
            meanie.rect.center = mx,my
            self.testgroup.add(meanie)

            if meanie.overlaps(self.testgroup):
                self.testgroup.remove(meanie)
                meanie.kill()
                self.init_meanies(counter)
            else:
                meanie.movement = self.move_schedule[move_index]
                meanie.current_move_index = move_index
                meanie.speed = 3
                move_index +=1
                if move_index > 3: move_index = 0
                self.meanies.insert(counter,meanie)
                self.solidgroup.add(self.meanies[counter])
                counter += 1

        if counter == self.number_meanies:
            self.start_game()


    def start_game(self):
        del self.testgroup
        self.gameRunning = True
        self.mainloop()

    def mainloop(self):
        print len(self.meanies)
        self.clock = pygame.time.Clock()
        fnt = pygame.font.Font(None, 20)
        self.player.rect.center = [20,220]

        # blit background on screen
        # self.display.paint_background()
        # pygame.display.flip()
  
        while self.gameRunning:

            dirty = []

            self.clock.tick(_MIN_TICKS_)
            framerate = self.clock.get_fps()

            dirty_background = self.display.screen.blit(self.display.bg, self.display.bgpos)

            # check wether background was "moved"
            if self.display.bg_oldpos[0] != self.display.bgpos[0] \
            or self.display.bg_oldpos[1] != self.display.bgpos[1]:
                dirty.insert(len(dirty), dirty_background)
                self.display.bg_oldpos = copy.copy(self.display.bgpos)

            self.player.state.set_current_state(self)

            # blit player on screen
            d = self.display.paint_sprite(self.player)
            dirty.insert(len(dirty), d)
            
            self.steine.update()
            self.steine.draw(self.display.screen)
            
            self.ladders.update()
            self.ladders.draw(self.display.screen)
            
#            d = self.display.paint_sprite(self.stein)
#            dirty.insert(len(dirty), d)

            # blit meanies on screen
            for i in range(0,self.number_meanies):

                if self.meanies[i].is_on_screen():

                    meanie_oldpos = self.meanies[i].rect

                    # ! make blit position relative to scrolling background !
                    meanie_pos_x = self.meanies[i].rect.left + self.display.bgpos[0]
                    meanie_pos_y = self.meanies[i].rect.top + self.display.bgpos[1]
                    self.meanies[i].rect = meanie_pos_x, meanie_pos_y
                    d = self.display.paint_sprite(self.meanies[i])
                    dirty.insert(len(dirty), d)
                    self.meanies[i].rect = meanie_oldpos

            caption = ("bgpos {0} | charpos {1} | fps {2} ").format(
            self.display.bgpos,
            self.player.rect.center,
            framerate
            )
            txt = fnt.render( caption, 1, (0,0,0), (255,255,0))
            dirty.insert( len(dirty), self.display.screen.blit(txt, [0, 0] ) )

            caption = ("stand {0} | climb {1} | fall {2} ").format(
            self.player.state.standing,
            self.player.state.climbing,
            self.player.state.falling
            )

            txt = fnt.render( caption, 1, (0,0,0), (255,255,0))
            dirty.insert( len(dirty), self.display.screen.blit(txt, [0, 20] ) )

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
                            
                    elif e.key == K_DOWN and not self.player.state.falling:
                        self.player.movement[1]= self.player.speed
                        
                    elif e.key == K_LEFT:
                        self.player.movement[0] = - self.player.speed
                        
                    elif e.key == K_RIGHT:  
                        self.player.movement[0] = self.player.speed
                
                elif e.type == KEYUP:
                    if e.key == K_UP or e.key == K_DOWN:
                        self.player.movement[1] = 0
                    elif e.key == K_LEFT or e.key == K_RIGHT:
                        self.player.movement[0] = 0

            if self.player.movement[0] != 0 or self.player.movement[1] != 0:
                self.player.centered_move()
            

#            if self.cloud.is_on_screen():
#                if self.display.bgpos[0] < 0:
#                    self.cloud.rect.left += -1
#
#                d = self.display.paint_sprite(self.cloud)
#                dirty.insert(len(dirty), d)
#                if self.display.bgpos[0] < 0:
#                    self.cloud.rect.left -= -1
#
#                self.cloud.thundercloud
#
#            self.cloud.looping_move()
#

            for i in range(0,self.number_meanies): self.meanies[i].looping_move()

            self.player_collision_test()
            self.meanie_collision_test()

            pygame.display.update(dirty)

    def player_collision_test(self):

        player_current_pos = self.player.rect.center

        self.player.rect.left -= self.display.bgpos[0]
        self.player.rect.top  -= self.display.bgpos[1]
      
        for s in self.solidgroup.sprites():
            
            if pygame.sprite.collide_rect(self.player, s):
                if s.hit_time < pygame.time.get_ticks():

                    s.image = pygame.transform.flip(s.image, False, True)
                    s.is_upside_down = True
                    
                    s.current_move_index +=1
                    if s.current_move_index > 3:
                        s.current_move_index = 0
                    s.movement = self.move_schedule[s.current_move_index]
                    
                    # Meanie will be 'invulnerable' for next three secs
                    s.hit_time = pygame.time.get_ticks() + 3000

        self.player.rect.center = player_current_pos

    def meanie_collision_test(self):

        # first find all meanies that are currently visible on screen

        tmpgroup = pygame.sprite.Group()
        for meanie in self.solidgroup.sprites():
            if meanie.is_on_screen():
                tmpgroup.add(meanie)
        tmpgroup2 = tmpgroup.copy()

        # second compare all meanies in  the group for collisions

        for meanie in tmpgroup.sprites():

            for other_meanie in tmpgroup2.sprites():

                if meanie.name != other_meanie.name:

                    if pygame.sprite.collide_rect(meanie, other_meanie):

                        if other_meanie.hit_time < pygame.time.get_ticks():

                            other_meanie.current_move_index += 1

                            if other_meanie.current_move_index > 3:
                                other_meanie.current_move_index = 0

                            other_meanie.movement = self.move_schedule[other_meanie.current_move_index]
                            other_meanie.hit_time = pygame.time.get_ticks() + 3000
                            other_meanie.image = pygame.transform.flip(other_meanie.image, False, True)
                            other_meanie.is_upside_down = True


                        if meanie.hit_time < pygame.time.get_ticks():

                            meanie.current_move_index += 1

                            if meanie.current_move_index > 3:
                                meanie.current_move_index = 0

                            meanie.movement = self.move_schedule[meanie.current_move_index]
                            meanie.hit_time = pygame.time.get_ticks() + 3000
                            meanie.image = pygame.transform.flip(meanie.image, False, True)
                            meanie.is_upside_down = True


BasicMovement()
