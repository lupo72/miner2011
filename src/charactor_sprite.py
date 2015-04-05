# -*- coding: utf-8 -*-
import os
import pygame
from sprites import LittleSprite
from finitestatemachine import PlayerState
import copy

class Charactor(LittleSprite, PlayerState):

    images = {}
    basename = "Hero"
    current_animation_index = 0
    update_interval = 200
    speed = 2
    
    def __init__(self, game = None):
        self.handle_spritesheet()
        LittleSprite.__init__(self, self.image, game)
        self.state = PlayerState(game)

    def handle_spritesheet(self):
        tilewidth  = 24
        tileheight = 32
        pfad = os.path.abspath ( os.path.join("..", "..", "data", "chara_trashman.png") )
        spritesheet = pygame.image.load(pfad).convert()
        colorkey = spritesheet.get_at([0,0])
        spritesheet.set_colorkey(colorkey)   
        ix, iy = 0, 0
         
        for x in range(0, spritesheet.get_width(), tilewidth):
            
            iy = 0
            
            for y in range(0, spritesheet.get_height(), tileheight):
                
                img = spritesheet.subsurface( [x, y, tilewidth, tileheight] )
                big = pygame.transform.scale2x(img)
                
                self.images[ix, iy] = big
                
                iy += 1
                
            ix += 1
        
        self.image = self.images[self.current_animation_index, 2]
        self.rect = self.image.get_rect().inflate(-12, -14)
        
        

    def move_screen(self):
        vspeed = hspeed = self.speed
        dir = self.movement
        player_movable_x = True
        player_movable_y = True

        if self.state.falling:
            vspeed = self.speed * 2
        else:
            vspeed = self.speed

        if dir[0] != 0 and not self.is_in_horizontal_bounds():
            player_movable_x = self.game.display.move_arena_horizontal(dir, hspeed)

        if dir[1] != 0 and not self.is_in_vertical_bounds():
            player_movable_y = self.game.display.move_arena_vertikal(dir, vspeed)

        if player_movable_x or player_movable_y:
            self.move_player(player_movable_x, player_movable_y)


    def move_player(self, player_movable_x, player_movable_y):

        if player_movable_x:

            if self.movement[0] > 0 \
            and self.rect.left < self.game.display.arena[0] - self.rect.width :
                self.rect.move_ip(self.movement[0], 0)
                
            elif self.movement[0] < 0 \
            and self.rect.left > 0 :
                self.rect.move_ip(self.movement[0], 0)

        if player_movable_y:

            if self.movement[1] > 0 and self.rect.top < self.game.display.arena[1] - self.rect.height:
                self.rect.move_ip(0, self.movement[1])
            elif self.movement[1] < 0 and self.rect.top > 0:
                self.rect.move_ip(0, self.movement[1])

#    def feet(self):
#        self.rect.inflate_ip(-16,-46)
#        self.rect.move_ip(8,42)


    def feet(self):
        feet = copy.copy(self)
        r = copy.copy(self.rect)
        r.inflate_ip(-16,-46)
        r.move_ip(8,42)
        feet.rect = r
        return feet


    def middle(self):
        middle = copy.copy(self)
        r = copy.copy(self.rect)
        r.inflate_ip(-32, -40)
        r.move_ip( 6, 24)
        middle.rect = r
        return middle


    def head(self):
        head = copy.copy(self)
        r = copy.copy(self.rect)
        r.inflate_ip(-16, -44)
        r.move_ip( 6, 0)
        head.rect = r
        return head



    def update(self):
        
        
        
        self.state.set_walk_directions()
        
        self.barrell_collision()

        self.move_screen()
        
        current_pos = self.rect.center
        
        self.rect.left -= self.game.display.bgpos[0]
        self.rect.top  -= self.game.display.bgpos[1]
        
        self.meanie_collision()
        
        self.rect.center = current_pos



    def meanie_collision(self):
                                                    
        collided_list = pygame.sprite.spritecollide(
                                                    self,
                                                    self.game.meanies,
                                                    False,
                                                    None
                                                    )
        
        if len (collided_list) > 0:
            
            for meanie in collided_list:
                
                if meanie.hit_time < pygame.time.get_ticks():
                    
                    if not meanie.state.is_upside_down: 
                        meanie.state.change_to_upside_down()
        


        
    def barrell_collision(self):
        
        collided_list = pygame.sprite.spritecollide(
                                                    self,
                                                    self.game.barrels,
                                                    False,
                                                    None
                                                    )
        if len (collided_list) > 0:
            
            for barrel in collided_list:

                if barrel.rect.left < self.rect.left:
                    self.state.cannot_walk_left()
                elif barrel.rect.left > self.rect.left:
                    self.state.cannot_walk_right()
                
    def handle_bricklist(self, brick_list):
        for b in brick_list:
            
            if hasattr(b,'state') and b.state.set_to_cleared() is True:
                self.game.level.bricks_total -= 1
                
    def change_current_animation_index(self):
        
        if self.update_time < pygame.time.get_ticks():
            self.update_time += self.update_interval
        
            self.current_animation_index += 1
            if self.current_animation_index > 2:
                self.current_animation_index = 0
            
        
                
                
    def face_left(self):
        self.state.face_left()
        
    def face_right(self):
        self.change_current_animation_index()
        self.image = self.images[self.current_animation_index, 1]
        
    def face_up(self):
        self.change_current_animation_index()
        self.image = self.images[self.current_animation_index, 2]
        
    def face_down(self):
        self.change_current_animation_index()
        self.image = self.images[self.current_animation_index, 2] 
        
        
    
        

