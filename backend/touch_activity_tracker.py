from kivy.clock import Clock
from kivy.app import App
from kivy.animation import Animation


class TouchActivityTracker:
    """
    Singleton service to track touch activity and manage screensaver activation
    """
    
    _instance = None
    
    def __init__(self):
        if TouchActivityTracker._instance is not None:
            raise Exception("TouchActivityTracker is a singleton!")
        
        TouchActivityTracker._instance = self
        self.timeout_duration = 180  # 3 minutes in seconds
        self.screen_off_duration = 3 * 60 * 60  # 3 hours in seconds
        self.timeout_event = None
        self.screen_off_event = None
        self.is_screensaver_active = False
        self.is_screen_off = False
        self.last_screen = 'main'  # Remember last active screen
        
        # Start initial timeout
        self.reset_timeout()
        
    @classmethod
    def get_instance(cls):
        """Get the singleton instance"""
        if cls._instance is None:
            cls._instance = TouchActivityTracker()
        return cls._instance
    
    def reset_timeout(self):
        """Reset the screensaver timeout"""
        # Cancel existing timeout
        if self.timeout_event:
            self.timeout_event.cancel()
        
        # Only set new timeout if screensaver is not active
        if not self.is_screensaver_active and not self.is_screen_off:
            self.timeout_event = Clock.schedule_once(self.activate_screensaver, self.timeout_duration)
            
        # Cancel existing screen off event
        if self.screen_off_event:
            self.screen_off_event.cancel()
            self.screen_off_event = None
    
    def activate_screensaver(self, dt=None):
        """Activate the screensaver"""
        if self.is_screensaver_active:
            return
            
        app = App.get_running_app()
        if app and hasattr(app, 'sm'):
            # Remember current screen
            self.last_screen = app.sm.current
            
            # Animate transition to screensaver
            self.is_screensaver_active = True
            
            # Fade out current screen
            current_screen = app.sm.get_screen(app.sm.current)
            fade_out = Animation(opacity=0, duration=0.5)
            fade_out.bind(on_complete=self._switch_to_screensaver)
            fade_out.start(current_screen)
            
            # Schedule screen off
            self.screen_off_event = Clock.schedule_once(self.activate_screen_off, self.screen_off_duration)
    
    def _switch_to_screensaver(self, animation, widget):
        """Switch to screensaver after fade out"""
        app = App.get_running_app()
        if app and hasattr(app, 'sm'):
            app.sm.current = 'screensaver'
            
            # Fade in screensaver
            screensaver_screen = app.sm.get_screen('screensaver')
            screensaver_screen.opacity = 0
            fade_in = Animation(opacity=1, duration=0.5)
            fade_in.start(screensaver_screen)
            
            # Reset opacity of previous screen
            widget.opacity = 1

    def activate_screen_off(self, dt=None):
        """Activate the black screen (simulated screen off)"""
        if self.is_screen_off:
            return
            
        app = App.get_running_app()
        if app and hasattr(app, 'sm'):
            self.is_screen_off = True
            app.sm.current = 'black_screen'
            
            # TODO: Execute system command to turn off screen
            # import os
            # os.system("vcgencmd display_power 0")
    
    def wake_from_screensaver(self):
        """Wake up from screensaver and return to last screen"""
        if not self.is_screensaver_active:
            return
            
        app = App.get_running_app()
        if app and hasattr(app, 'sm'):
            # Fade out screensaver
            screensaver_screen = app.sm.get_screen('screensaver')
            fade_out = Animation(opacity=0, duration=0.3)
            fade_out.bind(on_complete=lambda anim, widget: self._return_to_last_screen())
            fade_out.start(screensaver_screen)

    def wake_from_screen_off(self):
        """Wake up from black screen"""
        if not self.is_screen_off:
            return

        # TODO: Execute system command to turn on screen
        # import os
        # os.system("vcgencmd display_power 1")
            
        app = App.get_running_app()
        if app and hasattr(app, 'sm'):
            self.is_screen_off = False
            # Return to screensaver first, then wake from there or go directly to last screen?
            # Let's go directly to last screen for now, or we could go to screensaver.
            # Going to last screen seems more natural for "waking up".
            self._return_to_last_screen()
    
    def _return_to_last_screen(self):
        """Return to the last active screen after screensaver"""
        app = App.get_running_app()
        if app and hasattr(app, 'sm'):
            # Switch back to last screen
            app.sm.current = self.last_screen
            
            # Fade in the screen
            current_screen = app.sm.get_screen(self.last_screen)
            current_screen.opacity = 0
            fade_in = Animation(opacity=1, duration=0.3)
            fade_in.start(current_screen)
            
            # Reset screensaver screen opacity and mark as inactive
            screensaver_screen = app.sm.get_screen('screensaver')
            screensaver_screen.opacity = 1
            self.is_screensaver_active = False
            self.is_screen_off = False
            
            # Restart timeout
            self.reset_timeout()
    
    def on_touch_activity(self):
        """Called when any touch activity is detected"""
        if self.is_screensaver_active:
            # Wake from screensaver
            self.wake_from_screensaver()
        elif self.is_screen_off:
            self.wake_from_screen_off()
        else:
            # Reset timeout
            self.reset_timeout()
    
    def set_timeout_duration(self, duration):
        """Set the screensaver timeout duration in seconds"""
        self.timeout_duration = duration
        if not self.is_screensaver_active and not self.is_screen_off:
            self.reset_timeout()
    
    def pause_tracking(self):
        """Pause touch activity tracking (useful for popups, etc.)"""
        if self.timeout_event:
            self.timeout_event.cancel()
            self.timeout_event = None
        if self.screen_off_event:
            self.screen_off_event.cancel()
            self.screen_off_event = None
    
    def resume_tracking(self):
        """Resume touch activity tracking"""
        if not self.is_screensaver_active and not self.is_screen_off:
            self.reset_timeout()