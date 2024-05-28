from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup


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

        self.label = Label(text='Enter New User Name:', bold=True, height=90, size_hint_y=None, font_size=24)
        main_layout.add_widget(self.label)

        self.name_input = TextInput(
            hint_text='Name',
            multiline=False,
            readonly=True,
            background_color=(1, 1, 1, 1),  # White background
            foreground_color=(0, 0, 0, 1),  # Black text color
            font_size=24,
            padding_y=(10, 10),
            padding_x=(10, 10),
            cursor_color=(0, 0, 0, 1),  # Black cursor color
            size_hint_y=None,
            height=100,
            background_normal='',  # Remove the default background
            background_active=''  # Remove the active background
        )
        self.name_input.bind(focus=self.on_focus)
        main_layout.add_widget(self.name_input)

        self.keyboard_layout = self.create_keyboard()
        main_layout.add_widget(self.keyboard_layout)

        confirm_button = Button(text='Create User', size_hint_y=None, height=50, background_color=(1, 0.6, 0.4, 1))
        confirm_button.bind(on_press=self.show_confirmation_popup)
        main_layout.add_widget(confirm_button)

        self.add_widget(main_layout)
    
    def go_back(self, instance):
        self.manager.current = 'main'

    def on_focus(self, instance, value):
        if value:
            self.name_input.background_color = (0.9, 0.9, 0.9, 1)  # Light gray when focused
        else:
            self.name_input.background_color = (1, 1, 1, 1)  # White when unfocused

    def create_keyboard(self):
        keyboard_layout = GridLayout(cols=10, size_hint_y=None, height=300)

        keys = [
            '1','2','3','4','5','6','7','8','9','0',
            'Q','W','E','R','T','Y','U','I','O','P',
            'A','S','D','F','G','H','J','K','L',
            'Z','X','C','V','B','N','M',
            'Space', 'Backspace'
        ]

        for key in keys:
            button = Button(text=key)
            button.bind(on_press=self.on_key_press)
            keyboard_layout.add_widget(button)

        return keyboard_layout
    
    def on_pre_enter(self):
        self.name_input.text = ''

    def on_key_press(self, instance):
        current_text = self.name_input.text
        key = instance.text

        if key == 'Backspace':
            self.name_input.text = current_text[:-1]
        elif key == 'Space':
            self.name_input.text += ' '
        else:
            self.name_input.text += key

    def confirm_user_name(self, user_name):
        self.data_manager.add_new_user(user_name)
        self.popup.dismiss()
        self.manager.current = 'main'

    def show_confirmation_popup(self, instance):
        user_name = self.name_input.text.strip()
        if user_name:
            if self.data_manager.check_user_exists(user_name):
                self.show_user_exists_popup(user_name)
            else:
                self.show_confirm_user_popup(user_name)

    def show_user_exists_popup(self, user_name):
        content = BoxLayout(orientation='vertical', spacing=10, padding=10)
        content.add_widget(Label(text=f'The username "{user_name}" already exists.'))

        ok_button = Button(text='OK', size_hint_y=None, height=50)
        ok_button.bind(on_press=lambda x: self.popup.dismiss())
        content.add_widget(ok_button)

        self.popup = Popup(title='User Exists', content=content, size_hint=(None, None), size=(400, 200))
        self.popup.open()

    def show_confirm_user_popup(self, user_name):
        content = BoxLayout(orientation='vertical', spacing=10, padding=10)
        content.add_widget(Label(text=f'Create user {user_name}?'))

        buttons_layout = BoxLayout(size_hint_y=None, height=50)
        yes_button = Button(text='Yes', on_press=lambda x: self.confirm_user_name(user_name))
        no_button = Button(text='No', on_press=lambda x: self.popup.dismiss())
        buttons_layout.add_widget(yes_button)
        buttons_layout.add_widget(no_button)

        content.add_widget(buttons_layout)

        self.popup = Popup(title='Confirm User Name', content=content, size_hint=(None, None), size=(400, 200))
        self.popup.open()