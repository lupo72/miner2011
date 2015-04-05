# -*- coding: utf-8 -*-
import pygame
import random

class player_states():

    def __init__(self):
        self.falling = True
        self.climbing = False
        self.standing = False
        self.can_walk_left  = True
        self.can_walk_right = True

    def set_current_state(self, parent):
        if pygame.sprite.spritecollide(
                                       parent.player.middle(),
                                       parent.ladders,
                                       False,
                                       None
                                       ): self.change_to_climbing(parent)
        else:
            self.climbing = False

        if not self.climbing and \
        pygame.sprite.spritecollide(
                                    parent.player.feet(),
                                    parent.steine,
                                    False,
                                    None
                                    ): self.change_to_standing(parent)
        elif not self.climbing:
            self.change_to_falling(parent)


    def change_to_falling(self, parent):
        
#        if self.falling:
#            parent.player.movement[1] += 0.14
#        else:
        self.standing = False
        self.falling = True
        parent.player.movement[1] = 4
            

    def change_to_climbing(self, parent):
        self.climbing = True
        if self.falling:
            self.falling = False
            parent.player.movement[1] = 0

    def change_to_standing(self, parent):
        self.standing = True
        self.falling = False
        parent.player.movement[1] = 0
        
    
    def cannot_walk_left(self):
        self.can_walk_left = False
    
    
    def cannot_walk_right(self):
        self.can_walk_right = False
        
        
    def clear_walk_directions(self):
        self.can_walk_left  = True
        self.can_walk_right = True
        


class meanie_states():
    is_upside_down = False
    
    def __init__(self, parent):
        self.parent = parent
        self.move_schedule = dict()
        self.move_schedule[0] = [-1,0]
        self.move_schedule[1] = [0,-1]
        self.move_schedule[2] = [1,0]
        self.move_schedule[3] = [0,1]
        self.current_move_index = 0

        
    def change_move_index(self):
        self.current_move_index += 1
        if self.current_move_index > len(self.move_schedule) - 1:
            self.current_move_index = 0
        self.parent.movement = self.move_schedule[self.current_move_index]

            
    def set_random_move_index(self):
        index = random.randint(0, len(self.move_schedule)-1)
        self.parent.movement = self.move_schedule[index]

        
    def change_to_upside_down(self):
        self.is_upside_down = True
        self.parent.hit_time = pygame.time.get_ticks() + 3000
        self.change_move_index()
        self.parent.image = pygame.transform.flip(self.parent.image, False, True)
    
    def change_to_downside_up(self):
        self.parent.image = self.parent.images[self.parent.current_animation_index]
        self.is_upside_down = False