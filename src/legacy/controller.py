import pygame
from pygame.locals import *
import sys

class Controller ():
    
    def __init__(self):
        pass
    
#    def __init__(self, game):
#        self.game = game



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
                elif e.key == K_UP and player.state.climbing:
                    player.movement[1]= - player.speed
                    
                    player.face_up()
                        
                elif e.key == K_DOWN \
                 and not player.state.falling \
                 and player.state.climbing:
                    
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


        
#    def handle_keyboard_input(self):
#        
#        for e in pygame.event.get():
#    
#            if e.type == QUIT:
#                self.game.gameRunning = False
#                pygame.quit()
#                sys.exit()
#            elif e.type == KEYDOWN:
#                
#                if e.key == K_ESCAPE:
#                    self.game.gameRunning = False
#                    pygame.quit()
#                    sys.exit()
#                elif e.key == K_UP and self.game.player.state.climbing:
#                    self.game.player.movement[1]= - self.game.player.speed
#                    
#                    self.game.player.face_up()
#                        
#                elif e.key == K_DOWN \
#                 and not self.game.player.state.falling \
#                 and self.game.player.state.climbing:
#                    
#                    self.game.player.movement[1]= self.game.player.speed
#                    
#                    self.game.player.face_down()
#                    
#                elif e.key == K_LEFT:
#                    if self.game.player.state.falling:
#                        self.game.player.movement[0] = - self.game.player.speed/2
#                    else:
#                        self.game.player.movement[0] = - self.game.player.speed
#    
#                    if not self.game.player.state.can_walk_left:
#                        self.game.player.movement[0] = 0
#                        
#                    self.game.player.face_left()
#                    
#                elif e.key == K_RIGHT:  
#                    if self.game.player.state.falling:
#                        self.game.player.movement[0] = self.game.player.speed/2
#                    else:
#                        self.game.player.movement[0] = self.game.player.speed
#    
#                    if not self.game.player.state.can_walk_right:
#                        self.game.player.movement[0] = 0
#                    
#                    self.game.player.face_right()
#    
#            elif e.type == KEYUP:
#                if e.key == K_UP or e.key == K_DOWN:
#                    self.game.player.movement[1] = 0
#                elif e.key == K_LEFT or e.key == K_RIGHT:
#                    self.game.player.movement[0] = 0
