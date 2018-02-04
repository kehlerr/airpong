import obj_template
from obj_template import X, Y

class Line(obj_template.T):
        def __init__(self,
                     spr_img,
                     pos,
                     size,
                     sfce,
                     group=None
                     ):

            obj_template.T.__init__(self, spr_img, size, (pos[X]+size[X]/2, pos[Y]+size[Y]/2), group, sfce)
