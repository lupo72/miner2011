# -*- coding: utf-8 -*-
import pygame

class Hud(pygame.font.Font):

    def __init__(self):
        pygame.font.Font.__init__(self, None, 16)
        pass

    def showinfo(self, parent, dirty):

        caption = ("arena {2} | bgpos {0} | bgmax {3} | fps {1}").format(
        parent.display.bgpos,
        "%.2f" % parent.framerate,
        parent.display.arena,
        parent.display.bgmax
        )
        txt = self.render( caption, 1, (0,0,0), (255,255,0))
        dirty.insert( len(dirty), parent.display.screen.blit(txt, [0, 0] ) )

        caption = ("charpos {3} | stand {0} | climb {1} | fall {2} ").format(
        parent.player.state.standing,
        parent.player.state.climbing,
        parent.player.state.falling,
        parent.player.rect.center
        )

        txt = self.render( caption, 1, (0,0,0), (255,255,0))
        dirty.insert( len(dirty), parent.display.screen.blit(txt, [0, 14] ) )

        caption = ("pspeed {0} | pmovement {1}").format(
        parent.player.speed,
        parent.player.movement
        )

        txt = self.render( caption, 1, (0,0,0), (255,255,0))
        dirty.insert( len(dirty), parent.display.screen.blit(txt, [0, 28] ) )
