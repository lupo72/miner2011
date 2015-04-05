# -*- coding: utf-8 -*-
import os
import pygame
import random
from sprites import LittleSprite
from finitestatemachine import MeanieState

pfad = os.path.abspath( os.path.join ("..", "..", "data", "meanie_sheet.png") )

class Meanie(LittleSprite, MeanieState):
    sprite_animation = True
    tile_width = 32
    tile_height = 32
    update_time = 0
    update_interval = 200
    image = pygame.image.load(pfad)
    images = []
    current_animation_index = 0
    basename = "meanie.png"

    def __init__(self):
        self.handle_spritesheet()
        LittleSprite.__init__(self, Meanie.image)
        self.state = MeanieState(self)


    def handle_spritesheet(self):
        spritesheet = self.image

        if len(Meanie.images) < 2 :

            for y in range(0, self.image.get_height(), self.tile_height):

                for x in range(0, self.image.get_width(), self.tile_width):

                    img = spritesheet.subsurface( [ x, y, self.tile_width, self.tile_height ] )
                    Meanie.images.append(img)


        self.image = Meanie.images[ random.randint(0, len(Meanie.images)-1) ]
        self.rect = self.image.get_rect()


    def looping_move(self):

        bounds = self.game.display.bgmax

        if self.movement[0] < 0 and self.rect.left < -self.rect.width:
            self.rect.left = bounds[0]
        elif self.movement[0] > 0 and self.rect.left > bounds[0]:
            self.rect.left = - self.rect.width


        if self.movement[1] < 0 and self.rect.top < -self.rect.height:
            self.rect.top = bounds[1] - self.rect.top
        elif self.movement[1] > 0 and self.rect.top > bounds[1]:
            self.rect.top = -self.rect.height

        self.rect.move_ip(self.movement)

    def update(self, dirty):
        self.looping_move()

        if self.is_on_screen():
            self.animate()
#            self.collision_test()
            meanie_oldpos = self.rect
            meanie_pos_x = self.rect.left + self.game.display.bgpos[0]
            meanie_pos_y = self.rect.top + self.game.display.bgpos[1]
            self.rect = meanie_pos_x, meanie_pos_y
            d = self.game.display.paint_sprite(self)
            dirty.insert(len(dirty), d)
            self.rect = meanie_oldpos

            
    def animate(self):
            if self.update_time < pygame.time.get_ticks():
                self.update_time += self.update_interval
                self.current_animation_index += 1
                if self.current_animation_index > len(self.images) - 1:
                    self.current_animation_index = 0
                self.image = self.images[self.current_animation_index]
                if self.state.is_upside_down:
                    self.image = pygame.transform.flip(self.image, False, True)
                    
            if self.state.is_upside_down \
            and self.hit_time < pygame.time.get_ticks():
               self.state.change_to_downside_up()
               
            
    
    def collision_test(self):
#        return 

        self.game.meanies.remove(self)
        collide_list = pygame.sprite.spritecollide(self, self.game.meanies, False, None)

#        print collide_list.sprites()

        if len(collide_list) > 0:
            
            if self.hit_time < pygame.time.get_ticks():
                if not self.state.is_upside_down:
                    self.state.change_to_upside_down()
                
            for meanie in collide_list:
                if meanie.hit_time < pygame.time.get_ticks():
                    if not meanie.state.is_upside_down:
                        meanie.state.change_to_upside_down()
                        
        self.game.meanies.add(self)