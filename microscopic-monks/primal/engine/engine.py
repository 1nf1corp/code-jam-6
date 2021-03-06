from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.widget import Widget

from .screen import Screen


class Engine(Widget):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        # bind the keyboard and its callbacks
        self.keyboard = Window.request_keyboard(self.on_keyboard_closed, self)
        self.keyboard.bind(on_key_down=self.on_keyboard_down)
        self.keyboard.bind(on_key_up=self.on_keyboard_up)
        Window.set_system_cursor("crosshair")

        self.window_size = 1, 1
        Window.bind(on_resize=self.on_resize)

        Window.bind(mouse_pos=self.update_mouse_pos)
        Window.bind(on_touch_down=self.update_mouse_down)
        # Window.bind(on_touch_up=self.update_mouse_up)

        self.pressed_keys = set()
        self.just_pressed_keys = set()
        self.mouse_keys = set()

        self.mouse_position = 0, 0

        # list of screens to update
        self.screen = None
        self.overlay = None

        # call the update method every frame
        Clock.schedule_interval(self.update, 1.0 / 60.0)

    def update_mouse_pos(self, _, n):
        self.mouse_position = n

    def on_resize(self, _, width, height):
        self.window_size = width, height

    def update_mouse_down(self, _, touch):
        self.mouse_keys.add(touch.button)

    def update_mouse_up(self, _, touch):
        self.mouse_keys.discard(touch.button)
        print(touch.button)

    def set_screen(self, screen: Screen) -> None:
        """Add the sprite to the internal list and add the widget."""
        if self.screen is not None:
            self.remove_widget(self.screen)

        screen.set_engine(self)
        self.screen = screen
        self.add_widget(screen)

    def set_overlay(self, screen: Screen) -> None:
        if self.overlay is not None:
            self.remove_widget(self.overlay)

        screen.set_engine(self)
        self.overlay = screen
        self.add_widget(screen)

    def remove_overlay(self) -> None:
        if self.overlay is not None:
            self.remove_widget(self.overlay)
        self.overlay = None

    def update(self, dt: float) -> None:
        """Call update and render on each screen """
        if self.overlay is not None:
            self.overlay.update(dt)
        elif self.screen is not None:
            self.screen.update(dt)
        self.just_pressed_keys = set()

    def on_keyboard_closed(self) -> None:
        self.keyboard.unbind(on_key_down=self.on_keyboard_down)
        self.keyboard.unbind(on_key_up=self.on_keyboard_down)
        self.keyboard = None

    def on_keyboard_down(self, _, key, *args) -> None:
        self.pressed_keys.add(key[0])
        self.just_pressed_keys.add(key[0])

    def on_keyboard_up(self, _, key, *args) -> None:
        self.pressed_keys.discard(key[0])
