# -*- coding: utf-8 -*-
import pygame
import random

#GRAVITY = 0.09

class PlayerState():
    game = None

    def __init__(self, game):
        self.game = game
        self.falling = True
        self.jumping = False
        self.climbing = False
        self.standing = False
        self.can_walk_left  = True
        self.can_walk_right = True
        self.facing_left = False
        self.facing_right = False
        self.facing_top = False
        self.facing_bottom = False
        

    def set_current_state(self): # , game
        self.player = self.game.player        
        if pygame.sprite.spritecollide(
                                       self.player.middle(),
                                       self.game.ladders,
                                       False,
                                       None
                                       ): self.change_to_climbing()
        else:
            self.climbing = False

        grp = pygame.sprite.Group()
        grp.add(self.game.steine, self.game.barrels)

        brick_list = pygame.sprite.spritecollide(
                            self.player.feet(),
                            grp,
                            False,
                            None
                            )

        if len(brick_list) > 0:
            if not self.climbing:
                self.change_to_standing()
                self.player.handle_bricklist(brick_list)
        else:
            if not self.jumping and not self.climbing:
                self.change_to_falling()

## 17/10/2011 - charactor can bump its head now

        bump_list = pygame.sprite.spritecollide(
                            self.player.head(),
                            grp,
                            False,
                            None
                            )

        if len(bump_list) > 0 and not self.climbing:
            self.change_to_falling()

## end 17/10/2011

        if not self.standing and not self.climbing and not self.jumping :
            self.change_to_falling()

        if self.jumping:
            self.continue_jumping()

    def continue_jumping(self):
        
        self.game.player.movement[1] += 0.09
        if self.game.player.movement[1] >= 0:
            self.jumping = False
            

    def change_to_falling(self):

        self.standing = False
        self.jumping = False
        self.falling = True
        
        self.game.player.movement[1] = 4

    def change_to_climbing(self):
        self.jumping = False
        self.climbing = True
        if self.falling:
            self.falling = False
            self.game.player.movement[1] = 0

    def change_to_standing(self):
        self.jumping = False
        self.standing = True
        self.falling = False
        self.game.player.movement[1] = 0
        
    def change_to_jumping(self):
        self.standing = False
        self.falling = False
        self.climbing = False
        self.jumping = True



    def cannot_walk_left(self):
        self.can_walk_left = False
    
    
    def cannot_walk_right(self):
        self.can_walk_right = False
        
        
    def set_walk_directions(self):
        self.can_walk_left  = True
        self.can_walk_right = True
        
    def face_left(self):
        self.player.change_current_animation_index()
        self.player.image = pygame.transform.flip(self.player.images[self.player.current_animation_index, 1], True, False)
        self.facing_left = True
 


class MeanieState():
    is_upside_down = False
    can_fly = True
    
    def __init__(self, game):
        self.parent = game
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

    def change_fly_state(self):
        if self.can_fly:
            self.can_fly = False


class BodenState():
    states = ['radiated', 'clean']
    state_index = 0
    stepped_on = False

    def __init__(self, parent):
        self.parent = parent

    def set_to_cleared(self):
        state_changed = False

        if self.state_index == 0:
            self.state_index = 1
            self.parent.image = self.parent.alternate_image
            state_changed = True

        return state_changed