#!/usr/bin/env python3

import os
import sys

# Disable Kivy's argument parser and set up environment
os.environ['KIVY_NO_ARGS'] = '1'

# Import mock dependencies first
import mock_dependencies

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.config import Config

# Import our screensaver components
from frontend.screensaver_screen import ScreensaverScreen
from backend.touch_activity_tracker import TouchActivityTracker

# Set window to be smaller for testing
Config.set('graphics', 'width', '400')
Config.set('graphics', 'height', '300')
Config.write()

class ScreensaverTestApp(App):
    def build(self):
        # Create screen manager
        self.sm = ScreenManager()
        
        # Add a simple main screen
        from kivy.uix.screenmanager import Screen
        from kivy.uix.boxlayout import BoxLayout
        from kivy.uix.button import Button
        
        main_screen = Screen(name='main')
        layout = BoxLayout(orientation='vertical')
        
        title = Label(text='Screensaver Test App\nScreensaver will activate in 10 seconds', 
                     font_size='20sp', halign='center')
        layout.add_widget(title)
        
        button = Button(text='Touch me to reset timer', size_hint_y=0.3)
        button.bind(on_press=self.on_button_press)
        layout.add_widget(button)
        
        main_screen.add_widget(layout)
        self.sm.add_widget(main_screen)
        
        # Add screensaver screen
        self.sm.add_widget(ScreensaverScreen(name='screensaver'))
        
        # Initialize touch tracker with short timeout for testing
        self.tracker = TouchActivityTracker.get_instance()
        self.tracker.set_timeout_duration(10)  # 10 seconds for testing
        
        return self.sm
    
    def on_button_press(self, instance):
        # Simulate touch activity
        if self.tracker:
            self.tracker.on_touch_activity()

if __name__ == '__main__':
    ScreensaverTestApp().run()