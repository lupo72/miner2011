# -*- coding: utf-8 -*-
import os
import pygame
import random
from umgebung import Boden1, Leiter, Fass
from meanie_sprite import Meanie

pfad = os.path.abspath ( os.path.join("..", "..", "data") )

class Level():
    bricks_total = 0
    levelmap = dict()

    def __init__(self, game):

        self.game = game

    def load_level(self, levelnr):
        bricks = dict()
        ladders = dict()
        if levelnr < 10:
            levelnr = "0" + str(levelnr)
        file = "level" + str(levelnr) + ".txt"
        pointer = open( os.path.join (pfad, file), "r")
        level = pointer.read()
        lines = level.split("\n")
        counter = 0
        for l in lines:
            levelparts = l.split(" ")
#            print levelparts[0], levelparts[1], levelparts[2]
            if levelparts[0] == 'bricks':
                bricks[counter] = levelparts[1], levelparts[2]
            if levelparts[0] == 'ladder':
                ladders[counter] = (levelparts[1]), (levelparts[2])

            counter += 1

#        print bricks, ladders
        self.build_level(bricks, ladders)

    def build_level(self, bricks, ladders):
        
        self.meanie_counter = 0
        
        self.init_floors(bricks)
        self.init_ladders(ladders)
        self.init_barrels()
        self.init_meanies(self.game.number_meanies)


    def init_floors(self, bricks):
        self.game.steine = pygame.sprite.Group()

#        for b in bricks.itervalues():
#            startvals = b[0].split(",")
#            start_range_x = int(startvals[0])
#            start_range_y = int(startvals[1])
#            endvals = b[1].split(",")
#            end_range_x = int(endvals[0])
#            end_range_y = int(endvals[1])
#
#            for y in range(start_range_x, end_range_y):
#
#                for x in range(start_range_x, end_range_x, 32):
#
#                    s = Boden1([x,y])
#                    self.game.steine.add(s)

        c = 0
        for y in range (300, self.game.display.bgmax[1], 200):

            if  c % 2 == 0:
                for x in range( self.game.display.bgmax[0]/2 + 64,
                                self.game.display.bgmax[0],
                                32):

                    s = Boden1([x,y])
                    self.game.steine.add(s)
            else:
                for x in range(64,
                               self.game.display.bgmax[0]/2,
                               32):

                    s = Boden1([x,y])
                    self.game.steine.add(s)
            c += 1

        del c

        ## Place a Floor at bottom of level
        for x in range(0,self.game.display.bgmax[0],32):
            s = Boden1([x, self.game.display.bgmax[1]-16])
            self.game.steine.add(s)

        self.bricks_total = len(self.game.steine)



    def init_ladders(self, ladders):
        self.game.ladders = pygame.sprite.Group()

        for x in range(50, 700, 500):

            for y in range(0, self.game.display.bgmax[1], 32):

                i = Leiter([x,y])
                self.game.ladders.add(i)



    def init_barrels(self):
        self.game.barrels = pygame.sprite.Group()

        for y in range(87, self.game.display.bgmax[1], 800):
            s = Fass([200, y])
            self.game.barrels.add(s)

#        s = Fass([340,1960])
#        self.barrels.add(s)

    def init_meanies(self, number_meanies):
        self.number_meanies = number_meanies
        self.game.meanies = pygame.sprite.Group()
        self.testgroup = pygame.sprite.Group()
        while self.meanie_counter < self.number_meanies:
            
            self.init_meanie()
        
        del self.testgroup
            
        
    def init_meanie(self):

            meanie = Meanie()
            meanie.state.set_random_move_index()
            mx = random.randint( 0, self.game.display.bgmax[0]-40 )
            my = random.randint( 0, self.game.display.bgmax[1]-40 )
            meanie.rect.center = mx,my
            self.testgroup.add(meanie)

            if meanie.overlaps(self.testgroup):
                self.testgroup.remove(meanie)
                meanie.kill()
                self.init_meanie()
            else:
                self.game.meanies.add(meanie)
                self.meanie_counter += 1

