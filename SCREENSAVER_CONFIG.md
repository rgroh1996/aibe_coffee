# Screensaver Feature Configuration

This file documents how to configure and customize the screensaver feature.

## Default Settings

- **Timeout Duration**: 3 minutes (180 seconds) of touch inactivity
- **Animation**: Floating coffee emoji with smooth transitions
- **Background**: Dark theme for power efficiency on touch screens
- **Wake-up**: Any touch event immediately returns to the last screen

## Configuring Timeout Duration

To change the screensaver timeout, modify the `TouchActivityTracker` initialization in `main.py`:

```python
# In main.py, after creating the touch_tracker
self.touch_tracker = TouchActivityTracker.get_instance()
self.touch_tracker.set_timeout_duration(300)  # 5 minutes instead of 3
```

Common timeout values:
- 120 seconds (2 minutes) - for high-activity environments
- 180 seconds (3 minutes) - default, good balance
- 300 seconds (5 minutes) - for lower-activity environments
- 600 seconds (10 minutes) - for very low-activity environments

## Customizing the Screensaver Screen

The screensaver appearance can be customized by modifying `frontend/screensaver_screen.py`:

### Changing Coffee Quotes
```python
self.coffee_quotes = [
    "Your custom quote here",
    "Another coffee saying",
    # Add more quotes as needed
]
```

### Modifying Colors
```python
# Coffee emoji color
color=(0.8, 0.6, 0.4, 1)  # Current brown color

# Title color
color=(0.7, 0.7, 0.7, 1)  # Current light gray

# Time display color
color=(0.6, 0.6, 0.6, 1)  # Current gray
```

### Changing Animation
The coffee emoji has a gentle floating animation. To modify it, edit the `start_coffee_animation()` method:

```python
# Adjust animation duration and positions
anim1 = Animation(pos_hint={'center_x': 0.52, 'center_y': 0.62}, duration=3)
anim2 = Animation(pos_hint={'center_x': 0.48, 'center_y': 0.58}, duration=3)
```

## Troubleshooting

### Screensaver Not Activating
1. Check that `TouchActivityTracker` is properly initialized in `main.py`
2. Verify all screens inherit from `TouchActivityMixin`
3. Ensure the timeout duration is reasonable for testing

### Touch Events Not Resetting Timer
1. Verify `TouchActivityMixin` is the first parent class in multiple inheritance
2. Check that `super().on_touch_*()` is called in custom touch handlers

### Animation Issues
1. Ensure the screensaver screen is properly added to the ScreenManager
2. Check that Kivy Animation imports are present
3. Verify OpenGL support for smooth animations

## Integration Notes

The screensaver feature is designed to work seamlessly with the existing coffee app:
- No data loss during transitions
- State preservation when returning from screensaver
- Automatic integration with all existing screens
- Minimal performance impact on touch responsiveness