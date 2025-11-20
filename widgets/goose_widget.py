from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.animation import Animation
from kivy.core.window import Window
from kivy.clock import Clock
import random
class GooseOverlay(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None,None)
       # self.size = (1,1) #Window.size
        self.window_size = Window.size
        print("Window.size",Window.size)
        self.opacity = 0
        self.disabled = True

        # Liste deiner Watschel-Frames
        self.frames = [
            'goose_0.png',
            'goose_1.png',
            'goose_2.png',
            'goose_1.png',  # zurück für smooth loop
        ]
        self.current_frame = 0
        self._anim_ev = None  # Clock-Event für Framewechsel

        self.goose = Image(
            source=self.frames[0],
            size=(self.window_size[0]*0.2, self.window_size[1]*0.2),
        )
        self.add_widget(self.goose)

    def _next_frame(self, dt):
        self.current_frame = (self.current_frame + 1) % len(self.frames)
        self.goose.source = self.frames[self.current_frame]
    def walk_across(self, duration=2, fps=8):
        """Lässt die Gans watschelnd über DIESES Layout laufen."""

        # Falls das Layout noch nicht gemessen ist (width == 0),
        # Animation auf den nächsten Frame verschieben.
        
        if self.width == 0:
            Clock.schedule_once(lambda dt: self.walk_across(duration, fps), 0)
            return

        self.opacity = 1
        self.disabled = False

        self.current_frame = 0
        self.goose.source = self.frames[0]

        # make start and end random
        # y position can vary between 0.2 and 0.8
        self.goose.y = self.window_size[1] * (0.2 + 0.6 * random.random())
        target_y = self.window_size[1] * (0.2 + 0.6 * random.random())

        target_x = -self.goose.width
        self.goose.x = self.window_size[0]

        # Frame-Animation starten
        if self._anim_ev:
            self._anim_ev.cancel()
        self._anim_ev = Clock.schedule_interval(self._next_frame, 1.0 / fps)

        anim = Animation(x=target_x, y=target_y, duration=duration)

        def _on_done(*args):
            if self._anim_ev:
                self._anim_ev.cancel()
                self._anim_ev = None
            self.opacity = 0
            self.disabled = True

        anim.bind(on_complete=_on_done)
        anim.start(self.goose)