'''Jurassic Journalists'''
from kivy.app import App
from kivy.core.image import Image as CoreImage
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.widget import Widget
from PIL import ImageDraw
from PIL import Image as Im
from io import BytesIO
from kivy.properties import ListProperty, ObjectProperty, NumericProperty
from math import sin, cos, pi
from kivy.core.window import Window

# Global Variable so there is no magic number.
SCREEN_WIDTH = 720
SCREEN_HEIGHT = 720
PAPER_COLOR = (200, 200, 200, 0)
STARTING_Y = SCREEN_HEIGHT - 150


class JurassicJournalistApp(App):
    ''' App Class '''
    def build(self):
#        Window.borderless = True
        return MainScreen()


class MainScreen(ScreenManager):
    ''' ScreenManager '''


class RoomScreen(Screen):
    ''' Screen One '''


class PhoneScreen(Screen):
    ''' Screen Two '''


class TextPaper(Image):
    """
    mesh_points = ListProperty([])
    mesh_texture = ObjectProperty(None)
    radius = NumericProperty(200)
    offset_x = NumericProperty(.5)
    offset_y = NumericProperty(.5)
    sin_wobble = NumericProperty(0)
    sin_wobble_speed = NumericProperty(0)
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Creating Blank Paper image to type on.
        self.img = Im.new("RGBA", (SCREEN_WIDTH, SCREEN_HEIGHT), PAPER_COLOR)

        # Type writer does not type from the top rather type from the bottom.
        self.txt = self.img.copy()
        self.head = {'x': 0, 'y': STARTING_Y}

        """
        self.mesh_texture = CoreImage('paper.png').texture
        Clock.schedule_interval(self.update_points, 0)
        """

    def update(self):
        """ Update the paper """
        data = BytesIO()
        i = self.letters[-1]

        # Type on the paper
        self.type(i)

        # Save updated txt (image) in data var to update the CoreImage Texture.
        self.txt.save(data, format='png')
        data.seek(0)
        im = CoreImage(BytesIO(data.read()), ext='png')
        self.texture = im.texture

    def type(self, key):
        """ Type on the paper """
        # Drawing on the image
        ImageDraw.Draw(self.txt).text((self.head["x"], self.head["y"]),
                                      key.char, font=key.font, fill=key.color)
        # Scrolling up
        self.font_size = key.font.getsize("l")[1]
        self.char_size = key.get_kerning()[0]
        self.head["x"] += self.char_size

        if self.head["x"] + self.char_size >= SCREEN_WIDTH:
            self.head["x"] = 0
            self.head["y"] -= self.font_size

    def escaped(self):
        if not self.font_size:
            return
        if self.text[-2:] == '_b':
            self.head["x"] -= self.char_size
        elif self.text[-2:] == '_n':
            self.head['y'] -= self.font_size
            self.head['x'] = 0

class PhoneButtons(Label):
    ''' Phone Button/Label '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.register_event_type("on_button_touch_down")

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.dispatch("on_button_touch_down", touch)
        return super().on_touch_down(touch)

    def on_button_touch_down(self, touch):
        ''' Actual Widget Press '''
        if self.collide_point(*self.pos):
            if touch.is_double_tap:
                self.parent.typw2.text = self.parent.typw2.text[:-1] + self.text[1]
            elif touch.is_triple_tap:
                self.parent.typw2.text = self.parent.typw2.text[:-1] + self.text[2]
            else:
                self.parent.typw2.text += self.text[0]
        return True


JurassicJournalistApp().run()
