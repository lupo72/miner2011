# -*- coding: utf-8 -*-
import pygame
import os
import random

class LittleSprite(pygame.sprite.Sprite):
    counter = 0
    movement = [0,0]
    speed = 0
    current_move_index = 0
    hit_time = 0
    is_upside_down = False
    display = None


    def __init__(self, image, display = None):
        if LittleSprite.display is None and display is not None:
            LittleSprite.display = display
        pfad =  os.path.abspath( os.path.join('..', '..', 'data') )
        self.image = pygame.image.load( os.path.join(pfad, image) )
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect()
        pygame.sprite.Sprite.__init__(self)
        img = image.split(".")
        spritename = img[0]
        self.name = spritename + str(LittleSprite.counter)
        LittleSprite.counter += 1

    def overlaps(self, testgroup):
        retval = False
        for other_sprite in testgroup.sprites():
            if other_sprite.name != self.name and pygame.sprite.collide_rect(self, other_sprite):
                retval = True
                break

        return retval


    def work_in_progress_centered_move(self):
        """Move Player Char only if on the edges of the *full* screen """

        screen_right  = - LittleSprite.display.bgmax[0] + LittleSprite.display.arena[0]
        screen_bottom = - LittleSprite.display.bgmax[1] + LittleSprite.display.arena[1]

        arena_center = (LittleSprite.display.arena[0]/2, LittleSprite.display.arena[1]/2)
        bgpos_left = LittleSprite.display.bgpos[0]
        bgpos_top = LittleSprite.display.bgpos[1]

#        print self.rect.center, arena_center
#        if self.rect.center == arena_center:

        if self.movement[0] != 0 and (bgpos_left > screen_right or bgpos_left < 0):

            if self.movement[0] < 0:
                LittleSprite.display.bgpos[0] += self.speed
            else:
                LittleSprite.display.bgpos[0] -= self.speed

        if self.movement[1] != 0 and (bgpos_top > screen_bottom or bgpos_top < 0):

            if self.movement[1] < 0:
                LittleSprite.display.bgpos[1] += self.speed
            else:
                LittleSprite.display.bgpos[1] -= self.speed

            pass



    def centered_move(self):

        screen_right  = - LittleSprite.display.bgmax[0] + LittleSprite.display.arena[0]
        screen_bottom = - LittleSprite.display.bgmax[1] + LittleSprite.display.arena[1]
        player_movable = True

        if self.movement[0] != 0 and self.rect.centerx == LittleSprite.display.arena[0]/2:
            
            if LittleSprite.display.bgpos[0] > screen_right and self.movement[0] > 0:
                LittleSprite.display.bgpos[0] -= self.speed
                player_movable = False
            elif LittleSprite.display.bgpos[0] < 0 and self.movement[0] < 0:
                LittleSprite.display.bgpos[0] += self.speed
                player_movable = False
#        else:
#            player_movable = True
                
        if self.movement[1] != 0 and self.rect.centery == LittleSprite.display.arena[1]/2:
            if LittleSprite.display.bgpos[1] > screen_bottom and self.movement[1] > 0:
                LittleSprite.display.bgpos[1] -= self.speed
                player_movable = False
            elif LittleSprite.display.bgpos[1] < 0 and self.movement[1] < 0:
                LittleSprite.display.bgpos[1] += self.speed
                player_movable = False
#        else:
#            player_movable = True

#        print player_movable, self.rect

        if player_movable: self.move_player()


#        if self.movement[0] > 0 \
#        and LittleSprite.display.bgpos[0] > screen_right \
#        and self.rect.centerx == LittleSprite.display.arena[0]/2:
#            LittleSprite.display.bgpos[0] -= self.speed
#
#        elif self.movement[0] < 0 \
#        and LittleSprite.display.bgpos[0] < 0 \
#        and self.rect.centerx == LittleSprite.display.arena[0]/2:
#            LittleSprite.display.bgpos[0] += self.speed
#
#        elif self.movement[1] < 0 \
#        and LittleSprite.display.bgpos[1] < 0 \
#        and self.rect.centery == LittleSprite.display.arena[1]/2:
#            LittleSprite.display.bgpos[1] += self.speed
#
#        elif self.movement[1] > 0 \
#        and LittleSprite.display.bgpos[1] > screen_bottom \
#        and self.rect.centery == LittleSprite.display.arena[1]/2:
#            LittleSprite.display.bgpos[1] -= self.speed
#        else:
#            self.move_player()


    def move_player(self):
        
        if self.movement[0] > 0 and self.rect.left < LittleSprite.display.arena[0] - self.rect.width:
            self.rect.move_ip( self.movement[0], 0 )
        elif self.movement[0] < 0 and self.rect.left > 0:
            self.rect.move_ip( self.movement[0], 0 )

        if self.movement[1] > 0 and self.rect.top < LittleSprite.display.arena[1] - self.rect.height:
            self.rect.move_ip( 0, self.movement[1] )
        elif self.movement[1] < 0 and self.rect.top > 0:
            self.rect.move_ip( 0, self.movement[1] )



    def looping_move(self):

        bounds = LittleSprite.display.bgmax
        #print bounds
        if self.is_upside_down and self.hit_time > 0 and self.hit_time < pygame.time.get_ticks():
            self.image = pygame.transform.flip(self.image, False, True)
            self.is_upside_down = False


        if self.movement[0] < 0 and self.rect.left < -self.rect.width:
            self.rect.left = bounds[0]
        elif self.movement[0] > 0 and self.rect.left > bounds[0]:
            self.rect.left = - self.rect.width


        if self.movement[1] < 0 and self.rect.top < -self.rect.height:
            self.rect.top = bounds[1] - self.rect.top
        elif self.movement[1] > 0 and self.rect.top > bounds[1]:
            self.rect.top = -self.rect.height

        self.rect.move_ip(self.movement)

    def thundercloud(self):
        if self.hit_time < pygame.time.get_ticks():
            self.hit_time = pygame.time.get_ticks() + random.randint(10,300);
            imgarray = pygame.surfarray.array2d(self.image)
            self.image = pygame.surfarray.make_surface( imgarray + random.randint(0,12))
            self.image.set_colorkey(self.image.get_at([0,0]))
            self.image = self.image.convert()

    def is_on_screen(self):

        xpos = self.rect.left + LittleSprite.display.bgpos[0]
        ypos = self.rect.top + LittleSprite.display.bgpos[1]

        if xpos >= -self.rect.width and xpos <= LittleSprite.display.arena[0] + self.rect.width\
        and ypos >=-self.rect.height and ypos <= LittleSprite.display.arena[1] + self.rect.height:
            return True
        else:
            return False
