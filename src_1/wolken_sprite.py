# -*- coding: utf-8 -*-
from sprites import LittleSprite


class Wolke(LittleSprite):
    pass

    def thundercloud(self):
        if self.hit_time < pygame.time.get_ticks():
            self.hit_time = pygame.time.get_ticks() + random.randint(10, 300);
            imgarray = pygame.surfarray.array2d(self.image)
            self.image = pygame.surfarray.make_surface(imgarray + random.randint(0, 12))
            self.image.set_colorkey(self.image.get_at([0, 0]))
            self.image = self.image.convert()

