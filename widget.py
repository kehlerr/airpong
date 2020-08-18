import pygame

from common import X, Y
from color_defs import GOLDEN


class Skin:
    def __init__(self, name, img_path, pieces):
        self.name = name
        self.img_path = img_path
        self.pieces = pieces
        self.sprite_atlas = None

    def set_on_widget(self, widget):
        if not self.sprite_atlas:
            self.sprite_atlas = pygame.image.load(self.img_path)
        w_size = widget.size
        left_padding = 0
        right_padding = w_size[0]
        top_padding = 0
        bottom_padding = w_size[1]
        for piece in self.pieces:
            area_crop = piece['area_crop']
            size = piece['size']
            piece_sf = pygame.Surface(size)
            piece_sf.blit(self.sprite_atlas, (0,0), (area_crop, size))
            align_x = piece['align_x']
            align_y = piece['align_y']
            surface_position = [0, 0]
            stretch_size = (0, 0)
            if align_x == 'left':
                if size[0] > left_padding:
                    left_padding = size[0]
            elif align_x == 'right':
                pos_x = w_size[0] - size[0]
                surface_position[0] = pos_x
                if pos_x < right_padding:
                    right_padding = pos_x
            elif align_x == 'stretch':
                surface_position[0] = left_padding
                new_width = right_padding - left_padding
                stretch_size = (new_width, size[1])

            if align_y == 'top':
                if size[1] > top_padding:
                    top_padding = size[1]
            elif align_y == 'bottom':
                pos_y = w_size[1] - size[1]
                surface_position[1] = pos_y
                if pos_y < bottom_padding:
                    bottom_padding = pos_y
            elif align_y == 'stretch':
                surface_position[1] = top_padding
                new_height = bottom_padding - top_padding
                if stretch_size[0] > 0:
                    stretch_size = (stretch_size[0], new_height)
                else:
                    stretch_size = (size[0], new_height)

            if (stretch_size[0] > 0 and stretch_size[1] > 0):
                piece_sf = pygame.transform.scale(piece_sf, stretch_size)

            widget.surface.blit(piece_sf, surface_position)


class Widget:
    on_hover_skin = None
    default_skin = None

    def __init__(self, parent, name, w_size, pos,
                 caption_data=None, skin_name=None, visible=True):
        self.parent = parent
        self.background_surface = self.parent.surface
        self.size = w_size
        self.position = pos
        self.visible = visible != 'False'
        self.surface = pygame.Surface(w_size, pygame.SRCALPHA, 32)
        self.rect = self.surface.get_rect()
        parent_pos = self.parent.get_absolute_position()
        self.absolute_pos = (
            parent_pos[X] + self.position[X],
            parent_pos[Y] + self.position[Y]
        )
        self.caption = None
        if caption_data is not None:
            self.caption_data = caption_data
            self.set_caption()
        self.skin_name = skin_name or self.default_skin
        self.reskin(skin_name)
        self.is_hovered = False
        self.on_pressed = None

    def set_caption(self):
        self.caption = self.caption_data.get('value')
        self.caption_position = (
            int(self.caption_data['left']),
            int(self.caption_data['top'])
        )

    def set_skin(self):
        skin_name = self.skin_name or self.default_skin
        if not skin_name:
            return
        skin = self.parent.skins[skin_name]
        skin.set_on_widget(self)

    def reskin(self, skin_name):
        self.skin_name = skin_name
        self.set_skin()
        self.draw()

    def is_mouse_on_wiget(self, cursor_pos: (int, int)) -> bool:
        if not self.visible:
            return
        absolute_rect = pygame.Rect(self.absolute_pos, self.size)
        return absolute_rect.collidepoint(cursor_pos)

    def set_on_hover(self):
        pass

    def reset_hover(self):
        pass

    def set_onpressed(self, func):
        self.on_pressed = func

    def on_mouse_pressed(self):
        pass

    def draw(self):
        if not self.visible:
            return
        if self.caption:
            self.draw_caption()
        self.parent.draw(self.surface, self.absolute_pos, self.rect)

    def draw_caption(self):
        font_obj = self.parent.fonts['btn_caption']
        caption_sf = font_obj.render(self.caption, True, GOLDEN)
        self.surface.blit(caption_sf, self.caption_position)


class Button(Widget):
    on_hover_skin = 'menu_panel_btn_highlighted'
    default_skin = 'menu_panel_btn'

    def set_on_hover(self):
        self.is_hovered = True
        self.reskin(self.on_hover_skin)

    def reset_hover(self):
        self.is_hovered = False
        self.reskin(self.default_skin)

    def on_mouse_pressed(self):
        if self.on_pressed:
            self.on_pressed()
        self.reskin(self.on_hover_skin)
