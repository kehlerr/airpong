import pygame
from PIL import Image
from field_defs import *
from color_defs import SNOW


class Net(pygame.sprite.Sprite):
     def __init__(self, sfce, pos_x, pos_y, width, height):
          pygame.sprite.Sprite.__init__(self)
          self.sfce = sfce
          img = Image.open(r'pic/net4.png').crop((0,0, width, height))
          cropped_imgname = r'pic/tmp_net.png'

          try:
               cropped_imgfile = open(cropped_imgname, 'wb')
               img.save(cropped_imgfile, 'png', quality=90)
               cropped_imgfile.close()
          except:
               print 'Cannot save temp image'
          
          try:
               self.image = pygame.image.load(cropped_imgname)
               self.sfce.blit(self.image, (pos_x, pos_y))
               self.rect  = self.image.get_rect()
               self.rect.move_ip(pos_x, pos_y)
          except:
               print 'Cannot open image'
          finally:          
               for y in range(FIELD_H / NET_DENSE):
                    pygame.draw.aaline(self.sfce, SNOW, (pos_x, y*NET_DENSE), (pos_x+NET_SIZE, (y+1)*NET_DENSE), 1) 
                    pygame.draw.aaline(self.sfce, SNOW, (pos_x+NET_SIZE, y*NET_DENSE), (pos_x, (y+1)*NET_DENSE), 1) 
