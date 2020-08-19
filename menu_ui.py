from lxml import etree
import pygame


from common import X, Y, load_image, DISPLAY_SIZE
from widget import Skin, Widget, Button


SKINS_PATH = 'ui/skins.xml'
FONT_PATH = 'ui/iceland.ttf'


class MenuUI:
    '''
        Base class of menu with layout and widgets with skins
    '''
    fader_bg_path = 'fader_bg'
    width = 400
    height = 500
    layout_path = None

    def __init__(self, display, parent):
        self.skins = {}
        self.load_skins()
        self.fonts = {}
        self.load_fonts()
        self.display = display
        self.parent = parent
        self.create_bg_surface()
        size = self.width, self.height
        self.surface = pygame.Surface(size, pygame.SRCALPHA, 32)
        self.position = (0,0)
        self.widgets = {}

    def load_skins(self):
        '''
            Parse skins and parameters from common skins xml file
        '''
        tree = etree.parse(SKINS_PATH)
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
        '''
            Parse layout from self layout xml file
        '''
        tree = etree.parse(self.layout_path)
        root = tree.getroot()
        widgets = root.findall('widget')

        for widget_element in widgets:
            w_attrib = widget_element.attrib
            w_name = w_attrib['name']
            w_type = w_attrib.get('type')
            w_skin = w_attrib.get('skin')
            w_visible = w_attrib.get('visible')
            w_position = (int(w_attrib['left']), int(w_attrib['top']))
            w_size = (int(w_attrib['width']), int(w_attrib['height']))
            w_caption_data = widget_element.find('caption').attrib
            self.add_widget(
                w_name, w_type, w_size, w_position,
                w_caption_data, w_skin, w_visible
            )

    def load_fonts(self):
        self.fonts['btn_caption'] = pygame.font.Font(FONT_PATH, 40)

    def create_bg_surface(self):
        '''
            Create background fader
        '''
        bg_sprite = load_image(self.fader_bg_path)
        self.bg_surface = pygame.transform.scale(bg_sprite, DISPLAY_SIZE)

    def add_widget(self, name, type_, size, pos,
                  caption_data, skin, visible):
        if type_ == 'button':
            w = Button(self, name, size, pos, caption_data, skin, visible)
        else:
            w = Widget(self, name, size, pos, caption_data, skin, visible)
        self.widgets[name] = w

    def get_widget(self, name: str)-> Widget:
        return self.widgets.get(name)

    def get_absolute_position(self):
        '''
            Need to calculate absolute position of child widgets
        '''
        return self.position

    def set_position(self, pos):
        self.position = pos

    def show(self):
        '''
            Load layout if needed and draw widgets on display
        '''
        if not self.widgets:
            self.load_layout()
        pygame.mouse.set_visible(True)
        self.bg_surface.blit(self.surface, self.position)
        self.display.blit(self.bg_surface, (0,0))
        for w in self.widgets.values():
            w.draw()
        pygame.display.update(((0,0), DISPLAY_SIZE))

    def hide(self):
        '''
            Redraw parent's surface to display and hide mouse cursor
        '''
        pygame.mouse.set_visible(False)
        self.display.blit(self.parent.surface, (0, 0))
        pygame.display.update(((0,0), DISPLAY_SIZE))

    def draw(self, surface=None, dest=(0,0), rect=None):
        '''
            Draw widget's surface or redraw self
        '''
        if not surface:
            surface = self.surface
        self.display.blit(surface, dest, rect)
        update_size = rect and (rect.width, rect.height) or DISPLAY_SIZE
        pygame.display.update((dest, update_size))

    def update(self):
        self.process_widgets()
        pygame.display.update()

    def process_widgets(self):
        '''
            Update widgets after user actions
        '''
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


class MenuPause(MenuUI):
    layout_path = 'ui/menu_layout.xml'


class MenuEnd(MenuUI):
    layout_path = 'ui/end_screen_layout.xml'
