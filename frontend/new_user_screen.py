from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.app import App


class NewUserScreen(Screen):
    def __init__(self, data_manager, **kwargs):
        super(NewUserScreen, self).__init__(**kwargs)
        self.data_manager = data_manager

        main_layout = BoxLayout(orientation='vertical')
        # Add the back button at the top
        back_button = Button(
            text='Back to main screen',
            size_hint_y=None,
            height=40,
            background_color=(0.6, 0.6, 0.6, 1),  # Gray color for the back button
            color=(1, 1, 1, 1)  # White text color
        )
        back_button.bind(on_press=self.go_back)
        main_layout.add_widget(back_button)

        self.label = Label(text='Enter First Name and Surname:', bold=True, height=90, size_hint_y=None, font_size=24)
        main_layout.add_widget(self.label)

        # First Name Input
        first_name_label = Label(text='First Name *', bold=True, size_hint_y=None, height=40, font_size=18, halign='left')
        first_name_label.bind(size=first_name_label.setter('text_size'))
        main_layout.add_widget(first_name_label)
        
        self.first_name_input = TextInput(
            hint_text='First Name (required)',
            multiline=False,
            readonly=True,
            background_color=(1, 1, 1, 1),  # White background
            foreground_color=(0, 0, 0, 1),  # Black text color
            font_size=24,
            padding_y=(10, 10),
            padding_x=(10, 10),
            cursor_color=(0, 0, 0, 1),  # Black cursor color
            size_hint_y=None,
            height=80,
            background_normal='',  # Remove the default background
            background_active=''  # Remove the active background
        )
        self.first_name_input.bind(focus=self.on_focus)
        main_layout.add_widget(self.first_name_input)

        # Surname Input  
        surname_label = Label(text='Surname *', bold=True, size_hint_y=None, height=40, font_size=18, halign='left')
        surname_label.bind(size=surname_label.setter('text_size'))
        main_layout.add_widget(surname_label)

        self.surname_input = TextInput(
            hint_text='Surname (required)',
            multiline=False,
            readonly=True,
            background_color=(1, 1, 1, 1),  # White background
            foreground_color=(0, 0, 0, 1),  # Black text color
            font_size=24,
            padding_y=(10, 10),
            padding_x=(10, 10),
            cursor_color=(0, 0, 0, 1),  # Black cursor color
            size_hint_y=None,
            height=80,
            background_normal='',  # Remove the default background
            background_active=''  # Remove the active background
        )
        self.surname_input.bind(focus=self.on_focus)
        main_layout.add_widget(self.surname_input)

        # Keep track of which input is currently active
        self.active_input = None

        self.keyboard_layout = self.create_keyboard()
        main_layout.add_widget(self.keyboard_layout)

        confirm_button = Button(text='Create User', size_hint_y=None, height=50, background_color=(1, 0.6, 0.4, 1))
        confirm_button.bind(on_press=self.show_confirmation_popup)
        main_layout.add_widget(confirm_button)

        self.add_widget(main_layout)
    
    def go_back(self, instance):
        App.get_running_app().sm.current = 'main'

    def on_focus(self, instance, value):
        if value:
            instance.background_color = (0.9, 0.9, 0.9, 1)  # Light gray when focused
            self.active_input = instance
        else:
            instance.background_color = (1, 1, 1, 1)  # White when unfocused

    def create_keyboard(self):
        keyboard_layout = GridLayout(cols=10, size_hint_y=None, height=300)

        keys = [
            '1','2','3','4','5','6','7','8','9','0',
            'Q','W','E','R','T','Y','U','I','O','P',
            'A','S','D','F','G','H','J','K','L',
            'Z','X','C','V','B','N','M',
            'Space', 'Next Field', 'Backspace'
        ]

        for key in keys:
            button = Button(text=key)
            button.bind(on_press=self.on_key_press)
            keyboard_layout.add_widget(button)

        return keyboard_layout
    
    def on_pre_enter(self):
        self.first_name_input.text = ''
        self.surname_input.text = ''
        self.active_input = self.first_name_input
        self.first_name_input.focus = True

    def on_key_press(self, instance):
        if not self.active_input:
            self.active_input = self.first_name_input
        
        current_text = self.active_input.text
        key = instance.text

        if key == 'Backspace':
            self.active_input.text = current_text[:-1]
        elif key == 'Space':
            self.active_input.text += ' '
        elif key == 'Next Field':
            # Switch between fields
            if self.active_input == self.first_name_input:
                self.active_input = self.surname_input
                self.surname_input.focus = True
            else:
                self.active_input = self.first_name_input
                self.first_name_input.focus = True
        else:
            self.active_input.text += key

    def confirm_user_name(self, first_name, surname):
        try:
            self.data_manager.add_new_user(first_name, surname)
            self.popup.dismiss()
            App.get_running_app().sm.current = 'main'
        except Exception as e:
            # Handle database constraint errors
            self.show_error_popup("Error creating user: " + str(e))

    def show_confirmation_popup(self, instance):
        first_name = self.first_name_input.text.strip()
        surname = self.surname_input.text.strip()
        
        # Validate required fields
        if not first_name:
            self.show_error_popup("First Name is required!")
            return
        
        if not surname:
            self.show_error_popup("Surname is required!")
            return
            
        # Check if user already exists
        if self.data_manager.check_user_exists(first_name, surname):
            self.show_user_exists_popup(first_name, surname)
        else:
            self.show_confirm_user_popup(first_name, surname)

    def show_error_popup(self, message):
        content = BoxLayout(orientation='vertical', spacing=10, padding=10)
        content.add_widget(Label(text=message, text_size=(350, None), halign='center'))

        ok_button = Button(text='OK', size_hint_y=None, height=50)
        ok_button.bind(on_press=lambda x: self.popup.dismiss())
        content.add_widget(ok_button)

        self.popup = Popup(title='Error', content=content, size_hint=(None, None), size=(400, 200))
        self.popup.open()

    def show_user_exists_popup(self, first_name, surname):
        content = BoxLayout(orientation='vertical', spacing=10, padding=10)
        content.add_widget(Label(text=f'A user with the name "{first_name} {surname}" already exists.\nPlease choose a different name.', 
                                text_size=(350, None), halign='center'))

        ok_button = Button(text='OK', size_hint_y=None, height=50)
        ok_button.bind(on_press=lambda x: self.popup.dismiss())
        content.add_widget(ok_button)

        self.popup = Popup(title='User Already Exists', content=content, size_hint=(None, None), size=(400, 250))
        self.popup.open()

    def show_confirm_user_popup(self, first_name, surname):
        content = BoxLayout(orientation='vertical', spacing=10, padding=10)
        content.add_widget(Label(text=f'Create user "{first_name} {surname}"?', 
                                text_size=(350, None), halign='center'))

        buttons_layout = BoxLayout(size_hint_y=None, height=50)
        yes_button = Button(text='Yes', on_press=lambda x: self.confirm_user_name(first_name, surname))
        no_button = Button(text='No', on_press=lambda x: self.popup.dismiss())
        buttons_layout.add_widget(yes_button)
        buttons_layout.add_widget(no_button)

        content.add_widget(buttons_layout)

        self.popup = Popup(title='Confirm User Creation', content=content, size_hint=(None, None), size=(400, 200))
        self.popup.open()