import pygame
from pygame.locals import *
import sys

class Controller ():
    
    def __init__(self):
        pygame.key.set_repeat(100,5)
        self = self


    def handle_keyboard_input(self, player):
        
        for e in pygame.event.get():
    
            if e.type == QUIT:
                player.game.gameRunning = False
                pygame.quit()
                sys.exit()
            elif e.type == KEYDOWN:
                
                if e.key == K_ESCAPE:
                    player.game.gameRunning = False
                    pygame.quit()
                    sys.exit()
                
                elif e.key == K_SPACE:

                    if player.state.standing:
                        if not player.state.jumping:
                            player.movement[1] -= player.speed * 2.5
                            player.state.change_to_jumping()
                    
                    
                elif e.key == K_UP:
                    if  player.state.climbing is True:
                        player.movement[1]= - player.speed
                        player.face_up()
                        
                elif e.key == K_DOWN:
                    if  player.state.climbing is True:
                        player.movement[1]= player.speed
                        player.face_down()
                    
                elif e.key == K_LEFT:
                    if player.state.falling:
                        player.movement[0] = - player.speed/2
                    else:
                        player.movement[0] = - player.speed
    
                    if not player.state.can_walk_left:
                        player.movement[0] = 0
                        
                    player.face_left()
                    
                elif e.key == K_RIGHT:  
                    if player.state.falling:
                        player.movement[0] = player.speed/2
                    else:
                        player.movement[0] = player.speed
    
                    if not player.state.can_walk_right:
                        player.movement[0] = 0
                    
                    player.face_right()
    
            elif e.type == KEYUP:
                if e.key == K_UP or e.key == K_DOWN:
                    player.movement[1] = 0
                elif e.key == K_LEFT or e.key == K_RIGHT:
                    player.movement[0] = 0


        
