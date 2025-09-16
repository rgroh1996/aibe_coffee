from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.animation import Animation
from datetime import datetime
import random


class ScreensaverScreen(Screen):
    def __init__(self, **kwargs):
        super(ScreensaverScreen, self).__init__(**kwargs)
        
        # Dark background layout for power efficiency
        self.layout = FloatLayout()
        self.add_widget(self.layout)
        
        # Create animated coffee logo/text
        self.coffee_label = Label(
            text='☕',
            font_size='120sp',
            color=(0.8, 0.6, 0.4, 1),  # Coffee brown color
            pos_hint={'center_x': 0.5, 'center_y': 0.6},
            size_hint=(None, None)
        )
        self.layout.add_widget(self.coffee_label)
        
        # App title
        self.title_label = Label(
            text='AIBE Coffee',
            font_size='40sp',
            color=(0.7, 0.7, 0.7, 1),  # Light gray
            pos_hint={'center_x': 0.5, 'center_y': 0.4},
            size_hint=(None, None)
        )
        self.layout.add_widget(self.title_label)
        
        # Time display
        self.time_label = Label(
            text='',
            font_size='30sp',
            color=(0.6, 0.6, 0.6, 1),  # Gray
            pos_hint={'center_x': 0.5, 'center_y': 0.2},
            size_hint=(None, None)
        )
        self.layout.add_widget(self.time_label)
        
        # Touch instruction
        self.instruction_label = Label(
            text='Touch anywhere to return',
            font_size='20sp',
            color=(0.5, 0.5, 0.5, 1),  # Dark gray
            pos_hint={'center_x': 0.5, 'center_y': 0.1},
            size_hint=(None, None)
        )
        self.layout.add_widget(self.instruction_label)
        
        # Animation and clock events
        self.coffee_animation = None
        self.time_clock = None
        
        # Coffee quotes for variety
        self.coffee_quotes = [
            "Life begins after coffee",
            "Coffee: because adulting is hard",
            "Espresso yourself",
            "Coffee is my love language",
            "But first, coffee",
            "Coffee time is the best time"
        ]
        
    def on_enter(self):
        """Called when screensaver becomes active"""
        # Update time display
        self.update_time()
        self.time_clock = Clock.schedule_interval(self.update_time, 1)
        
        # Start coffee emoji animation
        self.start_coffee_animation()
        
        # Occasionally show coffee quotes
        self.show_random_quote()
        
    def on_leave(self):
        """Called when leaving screensaver"""
        # Stop all animations and clocks
        if self.time_clock:
            self.time_clock.cancel()
        if self.coffee_animation:
            self.coffee_animation.stop(self.coffee_label)
            
    def update_time(self, dt=None):
        """Update the time display"""
        current_time = datetime.now().strftime('%H:%M:%S')
        self.time_label.text = current_time
        
    def start_coffee_animation(self):
        """Start subtle floating animation for coffee emoji"""
        # Create a gentle floating effect
        anim1 = Animation(pos_hint={'center_x': 0.52, 'center_y': 0.62}, duration=3)
        anim2 = Animation(pos_hint={'center_x': 0.48, 'center_y': 0.58}, duration=3)
        anim3 = Animation(pos_hint={'center_x': 0.5, 'center_y': 0.6}, duration=3)
        
        # Chain animations in a loop
        anim_sequence = anim1 + anim2 + anim3
        anim_sequence.repeat = True
        anim_sequence.start(self.coffee_label)
        self.coffee_animation = anim_sequence
        
    def show_random_quote(self):
        """Occasionally show a coffee quote instead of the title"""
        if random.random() < 0.3:  # 30% chance to show quote
            quote = random.choice(self.coffee_quotes)
            self.title_label.text = quote
            # Reset to original title after some time
            Clock.schedule_once(lambda dt: setattr(self.title_label, 'text', 'AIBE Coffee'), 5)
            
    def on_touch_down(self, touch):
        """Handle any touch to wake up from screensaver"""
        # Import here to avoid circular imports
        from backend.touch_activity_tracker import TouchActivityTracker
        
        # Get the activity tracker and wake up
        tracker = TouchActivityTracker.get_instance()
        if tracker:
            tracker.wake_from_screensaver()
        
        return True  # Consume the touch event