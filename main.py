import os
import sys

# Disable Kivy's argument parser before importing Kivy
os.environ['KIVY_NO_ARGS'] = '1'

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager
from frontend.main_screen import MainScreen
from frontend.select_coffee_screen import SelectCoffeeScreen
from frontend.payment_screen import PaymentScreen
from frontend.new_user_screen import NewUserScreen
from frontend.user_profile_screen import UserProfileScreen
from frontend.cleaning_screen import CleaningScreen
from frontend.contribute_screen import ContributeScreen
from frontend.screensaver_screen import ScreensaverScreen
from frontend.black_screen import BlackScreen
from kivy.config import Config
from kivy.uix.label import Label
from kivy.clock import Clock

from backend.data_manager import DataManager
from widgets.goose_widget import GooseOverlay
from backend.touch_activity_tracker import TouchActivityTracker

# Set configuration for full screen mode
#Config.set('graphics', 'fullscreen', 'auto')

Config.set('graphics', 'fullscreen', '0')  # Fullscreen deaktivieren
Config.set('graphics', 'width', '800')     # Fensterbreite
Config.set('graphics', 'height', '600')    # Fensterhöhe

Config.write()

class CoffeeListApp(App):
    def build(self):
        # Root-Layout:  overlays screens and emoji
        self.root_layout = FloatLayout()
        # initialize the data manager
        self.data_manager = DataManager("database/aibe_coffee.db")

        # ScreenManager remains unchanged 
        self.sm = ScreenManager()
        self.sm.add_widget(MainScreen(name='main', data_manager=self.data_manager))
        self.sm.add_widget(SelectCoffeeScreen(name='select_coffee', data_manager=self.data_manager))
        self.sm.add_widget(PaymentScreen(name='payment', data_manager=self.data_manager))
        self.sm.add_widget(NewUserScreen(name='new_user', data_manager=self.data_manager))
        self.sm.add_widget(UserProfileScreen(name='user_profile', data_manager=self.data_manager))
        self.sm.add_widget(CleaningScreen(name='cleaning', data_manager=self.data_manager))
        self.sm.add_widget(ContributeScreen(name='contribute_screen'))
        self.sm.add_widget(ScreensaverScreen(name='screensaver'))
        self.sm.add_widget(BlackScreen(name='black_screen'))

        # Initialize touch activity tracker after screen manager is ready
        self.touch_tracker = TouchActivityTracker.get_instance()

        # add ScreenManager to Layout 
        self.root_layout.add_widget(self.sm)

        # Emoji-Label on top  
        self.emoji_label = Label(
            text='',
            font_size='64sp',
            pos_hint={'center_x': 0.5, 'center_y': 0.85},
            size_hint=(None, None)
        )
        self.root_layout.add_widget(self.emoji_label)

        self.goose_overlay = GooseOverlay()
        self.root_layout.add_widget(self.goose_overlay)

        return self.root_layout
    
    def show_global_emoji(self, emoji, duration=3):
        self.emoji_label.text = emoji
        Clock.schedule_once(lambda dt: self.hide_global_emoji(), duration)

    def hide_global_emoji(self):
        self.emoji_label.text = ''


    def walk_goose(self):
        if hasattr(self, 'goose_overlay'):
            self.goose_overlay.walk_across()


if __name__ == '__main__':
    CoffeeListApp().run()
