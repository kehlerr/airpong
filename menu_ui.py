from lxml import etree
import pygame


from common import X, Y
from field import DISPLAY_SIZE
from widget import Widget, Skin


class MenuUI:
    fader_bg_path = 'pic/fader_bg.png'
    width = 400
    height = 500

    def __init__(self, display, field):
        self.skins = {}
        self.load_skins()
        self.fonts = {}
        self.load_fonts()
        self.display = display
        self.create_bg_surface()
        self.surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA, 32)
        self.position = (
            (field.rect.width-self.width)/2,
            (field.rect.height-self.height)/2
        )
        self.widgets = {}
        self.load_layout()

    def load_skins(self):
        tree = etree.parse('ui/skins.xml')
        root = tree.getroot()
        root_skins = root.findall('skin')

        for skin_element in root_skins:
            pieces = []
            cfg = skin_element.attrib
            name = cfg['name']
            img_path = cfg['img_src']
            for piece_element in skin_element.findall('piece'):
                piece = {}
                area_crop = piece_element.find('area_crop').attrib
                piece['area_crop'] = (
                    int(area_crop['left']),
                    int(area_crop['top'])
                )
                area_size = piece_element.find('size').attrib
                piece['size'] = (
                    int(area_size['width']),
                    int(area_size['height'])
                )
                align = piece_element.find('align').attrib
                piece['align_x'] = align.get('x')
                piece['align_y'] = align.get('y')
                pieces.append(piece)
            self.skins[name] = Skin(name, img_path, pieces)

    def load_layout(self):
        tree = etree.parse('ui/menu_layout.xml')
        root = tree.getroot()
        widgets = root.findall('widget')

        for widget_element in widgets:
            w_attrib = widget_element.attrib
            w_name = w_attrib['name']
            w_position = (int(w_attrib['left']), int(w_attrib['top']))
            w_size = (int(w_attrib['width']), int(w_attrib['height']))
            w_caption_data = widget_element.find('caption').attrib
            self.add_widget(w_name, w_size, w_position, w_caption_data)

    def load_fonts(self):
        self.fonts['btn_caption'] = pygame.font.Font('ui/iceland.ttf', 40)

    def create_bg_surface(self):
        bg_sprite = pygame.image.load(self.fader_bg_path)
        self.bg_surface = pygame.transform.scale(bg_sprite, DISPLAY_SIZE)

    def add_widget(self, name, size, pos, caption_data):
        w = Widget(self, name, size, pos, caption_data)
        self.widgets[name] = w

    def get_widget(self, name):
        return self.widgets.get(name)

    def get_absolute_position(self):
        return self.position

    def show(self):
        pygame.mouse.set_visible(True)
        self.bg_surface.blit(self.surface, self.position)
        self.display.blit(self.bg_surface, (0,0))
        for w in self.widgets.values():
            w.draw()
        pygame.display.update(((0,0), DISPLAY_SIZE))

    def draw(self, surface=None, dest=(0,0), rect=None):
        if not surface:
            surface = self.surface
        self.display.blit(surface, dest, rect)
        update_size = rect and (rect.width, rect.height) or DISPLAY_SIZE
        pygame.display.update((dest, update_size))

    def process(self):
        mouse_pos = pygame.mouse.get_pos()
        for w in self.widgets.values():
            if w.is_mouse_on_wiget(mouse_pos):
                if not w.is_hovered:
                    w.set_on_hover()
                else:
                    mouse_left_pressed = pygame.mouse.get_pressed()[0]
                    if mouse_left_pressed:
                        w.on_mouse_pressed()
            else:
                if w.is_hovered:
                    w.reset_hover()
