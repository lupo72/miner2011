#!/usr/bin/local/python
import pygame
from charactor_sprite import Charactor
from display import Display
from controller import Controller
from hud import Hud
from levels import Level
FPS = 120

class Game():
    framerate = 0
    number_meanies = 32
    
    def __init__(self):
        self.display = Display()
        self.player = Charactor(self)
        self.level = Level(self)
        self.hud = Hud()

        self.prepare_stage()

    def prepare_stage(self):
        self.level.load_level(0)
        self.start_game()


    def start_game(self):

        self.gameRunning = True
        self.mainloop()

    def mainloop(self):
        self.clock = pygame.time.Clock()
        self.player.rect.center = [self.display.arena[0]/2, self.display.arena[1]/2]
        controller = Controller()
        while self.gameRunning:

            dirty = []
            
            self.clock.tick(FPS)
            self.framerate = self.clock.get_fps()

            self.display.paint_background(dirty)
            self.player.state.set_current_state()
            d = self.display.paint_sprite(self.player)
            dirty.insert(len(dirty), d)

            self.steine.update()
            self.ladders.update()
            self.barrels.update()
            self.meanies.update(dirty)

            self.hud.showinfo(self, dirty)
            controller.handle_keyboard_input(self.player)
            self.player.update()

## Just for debugging - paint hitareas of charactor ##

            d = self.draw_hitarea(self.player.feet())
            dirty.insert(len(dirty), d)

            d = self.draw_hitarea(self.player.middle(), (0,0,255))
            dirty.insert(len(dirty), d)
            
            d = self.draw_hitarea(self.player.head(), (0,255,255))
            dirty.insert(len(dirty), d)

            pygame.display.update(dirty)

    def draw_hitarea(self, sprite, color=pygame.Color(255,0,0)):
        sfc = pygame.Surface([sprite.rect.width, sprite.rect.height])
        sfc.fill(color)
        dummy = pygame.sprite.Sprite()
        dummy.image = sfc
        dummy.rect = sprite.rect
        d = self.display.paint_sprite(dummy)
        
        return d
        

Game()
