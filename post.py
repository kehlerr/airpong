import pygame
from field_defs import POST_SIZE, POST_IMAGE
from color_defs import BLACK

global POSTS
POSTS = []

class Post(pygame.sprite.Sprite):
     def __init__(self, sfce, pos_x, pos_y, size = POST_SIZE, img_name = POST_IMAGE):
          pygame.sprite.Sprite.__init__(self)
          POSTS.append(self)
          self.sfce = sfce         
          self.size = size
          if img_name:
               image = pygame.image.load(img_name)
               self.image = pygame.transform.scale(image, (size, size))
               self.image.set_colorkey(BLACK)
               self.mask = pygame.mask.from_surface(self.image)
               self.rect = self.image.get_rect()
               self.rect.center = pos_x, pos_y
               self.sfce.blit(self.image, self.rect)
     
     
     def Move(self, dx, dy):
          if dx: self.rect.centerx = dx
          if dy: self.rect.centery = dy
