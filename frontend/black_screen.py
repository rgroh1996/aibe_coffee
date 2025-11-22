from kivy.uix.screenmanager import Screen
from kivy.graphics import Color, Rectangle
from backend.touch_activity_tracker import TouchActivityTracker

class BlackScreen(Screen):
    def __init__(self, **kwargs):
        super(BlackScreen, self).__init__(**kwargs)
        
        # Ensure the background is black
        with self.canvas.before:
            Color(0, 0, 0, 1)  # Black
            self.rect = Rectangle(size=self.size, pos=self.pos)
            
        self.bind(size=self._update_rect, pos=self._update_rect)
        
    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size
        
    def on_touch_down(self, touch):
        """Handle any touch to wake up from screen off"""
        # Get the activity tracker and wake up
        tracker = TouchActivityTracker.get_instance()
        if tracker:
            tracker.wake_from_screen_off()
        
        return True  # Consume the touch event
