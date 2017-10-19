import pygame
from field_defs import POST_SIZE

global POSTS
POSTS = []

class Post(pygame.sprite.Sprite):
     def __init__(self, sfce, pos_x, pos_y, size = POST_SIZE):
          pygame.sprite.Sprite.__init__(self)
          self.sfce = sfce         
          image = pygame.image.load('pic/post2.png')
          self.image = pygame.transform.scale(image, (size, size))
          self.rect = self.image.get_rect()
          self.rect.center = pos_x, pos_y
          self.size = size
          POSTS.append(self)
     
