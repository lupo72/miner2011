# -*- coding: utf-8 -*-
import pygame
from sprites import LittleSprite
from finitestatemachine import meanie_states


class Meanie(LittleSprite, meanie_states):
    sprite_animation = True
    tile_width = 32
    tile_height = 32
    update_time = 0
    update_interval = 200
    image = "meanie_sheet.png"
    current_animation_index = 0
            
    def __init__(self):
        LittleSprite.__init__(self, Meanie.image)
        self.state = meanie_states(self)

    def looping_move(self):

        bounds = LittleSprite.display.bgmax
        #print bounds
        if self.state.is_upside_down and self.hit_time < pygame.time.get_ticks(): 
            self.state.change_to_downside_up()

        if self.movement[0] < 0 and self.rect.left < -self.rect.width:
            self.rect.left = bounds[0]
        elif self.movement[0] > 0 and self.rect.left > bounds[0]:
            self.rect.left = - self.rect.width


        if self.movement[1] < 0 and self.rect.top < -self.rect.height:
            self.rect.top = bounds[1] - self.rect.top
        elif self.movement[1] > 0 and self.rect.top > bounds[1]:
            self.rect.top = -self.rect.height

        self.rect.move_ip(self.movement)

    def update(self, parent, dirty):

        self.looping_move()
       
        if self.is_on_screen():
            self.animate()
            # self.collision_test(parent)
            meanie_oldpos = self.rect
            meanie_pos_x = self.rect.left + self.display.bgpos[0]
            meanie_pos_y = self.rect.top + self.display.bgpos[1]
            self.rect = meanie_pos_x, meanie_pos_y
            d = self.display.paint_sprite(self)
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
                
            
    
    def collision_test(self, parent):
        
        group = pygame.sprite.Group()
        group = parent.meanies.copy()
        group.remove(self)
        collide_list = pygame.sprite.spritecollide(self, group, False, None)
        
        if len(collide_list) > 0:
            
            if self.hit_time < pygame.time.get_ticks():
                if not self.state.is_upside_down: self.state.change_to_upside_down()
                
            for meanie in collide_list:
                if meanie.hit_time < pygame.time.get_ticks():
                    if not meanie.state.is_upside_down: meanie.state.change_to_upside_down()
