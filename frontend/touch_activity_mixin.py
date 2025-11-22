from backend.touch_activity_tracker import TouchActivityTracker


class TouchActivityMixin:
    """
    Mixin class to add touch activity tracking to any screen
    """
    
    def on_touch_down(self, touch):
        """Override to track touch activity"""
        # Notify activity tracker
        tracker = TouchActivityTracker.get_instance()
        if tracker:
            tracker.on_touch_activity()
        
        # Call parent implementation
        return super().on_touch_down(touch)
    
    def on_touch_move(self, touch):
        """Override to track touch activity"""
        # Notify activity tracker
        tracker = TouchActivityTracker.get_instance()
        if tracker:
            tracker.on_touch_activity()
        
        # Call parent implementation
        return super().on_touch_move(touch)
    
    def on_touch_up(self, touch):
        """Override to track touch activity"""
        # Notify activity tracker
        tracker = TouchActivityTracker.get_instance()
        if tracker:
            tracker.on_touch_activity()
        
        # Call parent implementation
        return super().on_touch_up(touch)