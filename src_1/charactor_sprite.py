# -*- coding: utf-8 -*-
import pygame
from sprites import LittleSprite
from finitestatemachine import player_states
import copy

class Charactor(LittleSprite, player_states):
#    jumping = False
    falling = False
    standing = False
    can_climb = False

    def __init__(self, image, display = None):
        LittleSprite.__init__(self, image, display)
        self.state = player_states()

    def centered_move(self):
        
        if self.state.falling:
            vspeed = self.speed * 2
        else:
            vspeed = self.speed

        screen_right  = - LittleSprite.display.bgmax[0] + LittleSprite.display.arena[0]
        screen_bottom = - LittleSprite.display.bgmax[1] + LittleSprite.display.arena[1]

        player_movable_x = True
        player_movable_y = True

        if self.movement[0] != 0 and not self.is_in_horizontal_bounds():

            if LittleSprite.display.bgpos[0] > screen_right and self.movement[0] > 0:
                LittleSprite.display.bgpos[0] -= self.speed
                player_movable_x = False
            elif LittleSprite.display.bgpos[0] < 0 and self.movement[0] < 0:
                LittleSprite.display.bgpos[0] += self.speed
                player_movable_x = False


        if self.movement[1] != 0 and not self.is_in_vertical_bounds():
            if LittleSprite.display.bgpos[1] > screen_bottom and self.movement[1] > 0:
                LittleSprite.display.bgpos[1] -= vspeed # self.speed*2
                player_movable_y = False
            elif LittleSprite.display.bgpos[1] < 0 and self.movement[1] < 0:
                LittleSprite.display.bgpos[1] += vspeed # self.speed*2
                player_movable_y = False

        if player_movable_x or player_movable_y: self.move_player(player_movable_x, player_movable_y)


    def move_player(self, player_movable_x, player_movable_y):

        if player_movable_x:

            if self.movement[0] > 0 \
            and self.rect.left < LittleSprite.display.arena[0] - self.rect.width \
            and self.state.can_walk_right:
                self.rect.move_ip(self.movement[0], 0)
                
            elif self.movement[0] < 0 \
            and self.rect.left > 0 \
            and self.state.can_walk_left:
                self.rect.move_ip(self.movement[0], 0)

        if player_movable_y:

            if self.movement[1] > 0 and self.rect.top < LittleSprite.display.arena[1] - self.rect.height:
                self.rect.move_ip(0, self.movement[1])
            elif self.movement[1] < 0 and self.rect.top > 0:
                self.rect.move_ip(0, self.movement[1])

    def feet(self):
        feet = copy.copy(self)
        r = copy.copy(self.rect)
        r.inflate_ip(0,-40)
        r.move_ip(0,20)
        feet.rect = r
        return feet


    def middle(self):
        middle = copy.copy(self)
        r = copy.copy(self.rect)
        r.inflate_ip(-20, -40)
        r.move_ip(0,10)
        middle.rect = r
        return middle

    def update(self, parent):
        
        self.state.clear_walk_directions()
        
        # self.barrell_collision(parent)

        self.centered_move()
        
        current_pos = self.rect.center
        
        self.rect.left -= self.display.bgpos[0]
        self.rect.top  -= self.display.bgpos[1]
        
        self.meanie_collision(parent)
        
        self.rect.center = current_pos



    def meanie_collision(self, parent):
        collided_list = pygame.sprite.spritecollide(
                                                    self,
                                                    parent.meanies,
                                                    False,
                                                    None
                                                    )
        
        if len (collided_list) > 0:
            
            for meanie in collided_list:
                
                if meanie.hit_time < pygame.time.get_ticks():
                    
                    if not meanie.state.is_upside_down: 
                        meanie.state.change_to_upside_down()
        
        
    def barrell_collision(self, parent):
        
        collided_list = pygame.sprite.spritecollide(
                                                    self,
                                                    parent.barrels,
                                                    False,
                                                    None
                                                    )
        
        if len (collided_list) > 0:
            
            for barrel in collided_list:
                
                if barrel.rect.left < self.rect.left:
                    self.state.cannot_walk_left()
                    
                elif barrel.rect.left > self.rect.left:
                    self.state.cannot_walk_right()
                
    
