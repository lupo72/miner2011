# -*- coding: utf-8 -*-
import os
import random
import pygame

class LittleSprite(pygame.sprite.Sprite):

    counter = 0
    movement = [0, 0]
    speed = 0
    hit_time = 0
    
    update_time = 0
    update_interval = 0
    current_animation_index = 0 
     
    is_upside_down = False
    display = None

    def __init__(self, image, display=None):
        if LittleSprite.display is None and display is not None:
            LittleSprite.display = display
        
        pfad = os.path.abspath(os.path.join('..', '..', 'data', image))
        
        self.image = pygame.image.load(pfad)
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect()
        pygame.sprite.Sprite.__init__(self)
        img = image.split(".")
        spritename = img[0]
        self.name = spritename + "_" + str(LittleSprite.counter)
        LittleSprite.counter += 1
        
        if hasattr(self, 'sprite_animation') :
            self.handle_spritesheet()
        
    def handle_spritesheet(self):
        self.images = []
        spritesheet = self.image
        
        for y in range(0, self.image.get_height(), self.tile_height):
            
            for x in range(0, self.image.get_width(), self.tile_width):
                
                img = spritesheet.subsurface( [ x, y, self.tile_width, self.tile_height ] )
                self.images.append(img)
                
        self.image = self.images[ random.randint(0, len(self.images)-1) ]
        
        

    def overlaps(self, testgroup):

        retval = False
        for other_sprite in testgroup.sprites():
            if other_sprite.name != self.name and pygame.sprite.collide_rect(self, other_sprite):
                retval = True
                break

        return retval

    def is_in_horizontal_bounds(self):

        retval = None
        min  = LittleSprite.display.arena[0] / 2 # - 100
        max = LittleSprite.display.arena[0] / 2  # + 100

        if self.rect.centerx > min and self.rect.centerx < max:
            retval = True
        elif self.rect.centerx >= max and self.movement[0] < 0:
            retval = True
        elif self.rect.centerx <= min and self.movement[0] > 0:
            retval = True
        else:
            retval = False
        
        return retval

    def is_in_vertical_bounds(self):

        retval = None
        min  = LittleSprite.display.arena[1] / 2 # - 100
        max = LittleSprite.display.arena[1] / 2  # + 100

        if self.rect.centery > min and self.rect.centery < max:
            retval = True
        elif self.rect.centery >= max and self.movement[1] < 0:
            retval = True
        elif self.rect.centery <= min and self.movement[1] > 0:
            retval = True
        else:
            retval = False

        return retval


    def is_on_screen(self):

        xpos = self.rect.left + LittleSprite.display.bgpos[0]
        ypos = self.rect.top + LittleSprite.display.bgpos[1]

        if xpos >= -self.rect.width and xpos <= LittleSprite.display.arena[0] + self.rect.width\
        and ypos >= -self.rect.height and ypos <= LittleSprite.display.arena[1] + self.rect.height:
            return True
        else:
            return False



