import obj_template

class Post(obj_template.T):
     def Move(self, dx, dy):
          if dx: self.rect.centerx = dx
          if dy: self.rect.centery = dy
