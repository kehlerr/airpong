import pygame
import math

SPARKLE_SIZE = 6
SPARKLE_TTL = 20
SPARKLE_VEL = 5
SPARKLE_ANG = 45
SPARKLE_DANG = 15

SPARKLES = pygame.sprite.RenderPlain([])

class Sparkle(pygame.sprite.Sprite):
     def __init__( self, 
                   sfce, 
                   pos_x, 
                   pos_y,
                   ang  = SPARKLE_ANG,
                   dang = SPARKLE_DANG,
                   size = SPARKLE_SIZE, 
                   ttl  = SPARKLE_TTL,
                   vel  = SPARKLE_VEL ):

          pygame.sprite.Sprite.__init__(self)
          self.sfce = sfce
          image = pygame.image.load('pic/sparkle4.png')
          self.image = pygame.transform.scale(image, (size, size))
          self.rect  = self.image.get_rect()
          self.rect.center = pos_x, pos_y
          self.ttl = ttl
          self.vel = vel
          self.ang = ang
          self.dang = dang
          SPARKLES.add(self)

     def Live(self):
          if self.ttl > 0:
               self.Move()
               self.ttl -= 1
               if self.vel > 0 : self.vel -= 0.4
          else:
                self.kill()
                del self


     def Move(self):
          self.rect.x += self.vel*math.cos(math.radians(self.ang))
          self.rect.y += self.vel*math.sin(math.radians(self.ang))
          self.ang += self.dang
