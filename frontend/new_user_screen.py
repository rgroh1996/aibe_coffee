from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.popup import Popup
from kivy.app import App
from frontend.touch_activity_mixin import TouchActivityMixin

LAB_CHOICES = [
    'IDEA', 'AIMI', 'ANKI', 'SPARC', 'NSQUARED', 'NEUROTECH',
    'HEX', 'MAD', 'CIL', 'MIRA', 'BIONETS', 'HTA-IT', 'AIROB',
    'ADMIN', 'OTHER'
]


class NewUserScreen(TouchActivityMixin, Screen):
    def __init__(self, data_manager, **kwargs):
        super(NewUserScreen, self).__init__(**kwargs)
        self.data_manager = data_manager
        self.active_input = None

        main_layout = BoxLayout(orientation='vertical', padding=(15, 10, 15, 10))

        # Top bar with back button
        top_bar = BoxLayout(orientation='horizontal', size_hint_y=None, height=40)
        back_button = Button(text='< Cancel', size_hint_x=None, width=130, font_size='16sp',
                             background_color=(0.6, 0.6, 0.6, 1), color=(1, 1, 1, 1))
        back_button.bind(on_press=self.go_back)
        top_bar.add_widget(back_button)
        top_bar.add_widget(Label())  # spacer
        main_layout.add_widget(top_bar)

        # Title
        self.label = Label(text='Create New User', bold=True, height=40, size_hint_y=None, font_size='20sp')
        main_layout.add_widget(self.label)

        main_layout.add_widget(self._spacer(5))

        # First Name row
        self.first_name_row, self.fn_label, self.first_name_input = self._create_input_row('First Name:', 'First Name')
        self.first_name_input.bind(focus=self.on_focus)
        main_layout.add_widget(self.first_name_row)

        main_layout.add_widget(self._spacer(8))

        # Last Name row
        self.last_name_row, self.ln_label, self.last_name_input = self._create_input_row('Last Name:', 'Last Name')
        self.last_name_input.bind(focus=self.on_focus)
        main_layout.add_widget(self.last_name_row)

        main_layout.add_widget(self._spacer(8))

        # Lab spinner row
        lab_row = BoxLayout(orientation='horizontal', size_hint_y=None, height=50, spacing=8)
        lab_label = Label(text='Lab:', size_hint_x=None, width=110, font_size='16sp',
                          color=(0.6, 0.6, 0.6, 1), halign='right', valign='middle')
        lab_label.bind(size=lab_label.setter('text_size'))
        lab_row.add_widget(lab_label)
        self.lab_spinner = Spinner(
            text='Select Lab',
            values=LAB_CHOICES,
            size_hint_y=None,
            height=44,
            font_size='18sp',
            background_color=(0.4, 0.6, 1, 1),
            color=(1, 1, 1, 1),
            bold=True
        )
        lab_row.add_widget(self.lab_spinner)
        main_layout.add_widget(lab_row)

        main_layout.add_widget(self._spacer(8))

        # Keyboard
        self.keyboard_layout = self.create_keyboard()
        main_layout.add_widget(self.keyboard_layout)

        main_layout.add_widget(self._spacer(8))

        # Confirm button
        confirm_button = Button(text='Create User', size_hint_y=None, height=55, font_size='22sp', bold=True,
                                background_color=(1, 0.6, 0.4, 1), color=(1, 1, 1, 1))
        confirm_button.bind(on_press=self.show_confirmation_popup)
        main_layout.add_widget(confirm_button)

        self.add_widget(main_layout)

        # Default active input
        self.active_input = self.first_name_input

    def _spacer(self, h):
        return Label(size_hint_y=None, height=h)

    def _create_input_row(self, label_text, hint_text):
        row = BoxLayout(orientation='horizontal', size_hint_y=None, height=50, spacing=8)
        label = Label(text=label_text, size_hint_x=None, width=110, font_size='16sp',
                      color=(0.6, 0.6, 0.6, 1), halign='right', valign='middle')
        label.bind(size=label.setter('text_size'))
        row.add_widget(label)
        ti = TextInput(hint_text=hint_text, multiline=False, readonly=True,
                       background_color=(1, 1, 1, 1), foreground_color=(0, 0, 0, 1),
                       font_size='20sp', padding=(10, 8), cursor_color=(0, 0, 0, 1),
                       size_hint_y=None, height=44, background_normal='', background_active='')
        row.add_widget(ti)
        return row, label, ti

    def go_back(self, instance):
        App.get_running_app().sm.current = 'main'

    def on_focus(self, instance, value):
        if value:
            self._set_active_field(instance)

    def _set_active_field(self, field_input):
        self.active_input = field_input
        # Reset all
        for lbl, inp in [(self.fn_label, self.first_name_input), (self.ln_label, self.last_name_input)]:
            lbl.color = (0.6, 0.6, 0.6, 1)
            inp.background_color = (1, 1, 1, 1)
        # Highlight active
        if field_input == self.first_name_input:
            self.fn_label.color = (1, 0.6, 0.4, 1)
            self.first_name_input.background_color = (1, 0.97, 0.94, 1)
        elif field_input == self.last_name_input:
            self.ln_label.color = (1, 0.6, 0.4, 1)
            self.last_name_input.background_color = (1, 0.97, 0.94, 1)

    def create_keyboard(self):
        keyboard_layout = BoxLayout(orientation='vertical', size_hint_y=None, height=200, spacing=2)

        rows = [
            list('QWERTYUIOP'),
            list('ASDFGHJKL'),
            list('ZXCVBNM'),
        ]

        for row_keys in rows:
            row = BoxLayout(orientation='horizontal', spacing=2)
            # Add spacer for centering shorter rows
            if len(row_keys) < 10:
                row.add_widget(Label(size_hint_x=(10 - len(row_keys)) / 2 / 10))
            for key in row_keys:
                btn = Button(text=key, font_size='18sp', bold=True,
                             background_color=(0.35, 0.35, 0.4, 1), color=(1, 1, 1, 1))
                btn.key_value = key
                btn.bind(on_press=self.on_key_press)
                row.add_widget(btn)
            if len(row_keys) < 10:
                row.add_widget(Label(size_hint_x=(10 - len(row_keys)) / 2 / 10))
            keyboard_layout.add_widget(row)

        # Space + Backspace row
        bottom_row = BoxLayout(orientation='horizontal', spacing=2)
        bottom_row.add_widget(Label(size_hint_x=1))
        space_btn = Button(text='_______', font_size='18sp', bold=True, size_hint_x=3,
                           background_color=(0.45, 0.45, 0.5, 1), color=(1, 1, 1, 1))
        space_btn.key_value = 'Space'
        space_btn.bind(on_press=self.on_key_press)
        bottom_row.add_widget(space_btn)
        bksp_btn = Button(text='<--', font_size='18sp', bold=True, size_hint_x=2,
                          background_color=(0.7, 0.35, 0.35, 1), color=(1, 1, 1, 1))
        bksp_btn.key_value = 'Backspace'
        bksp_btn.bind(on_press=self.on_key_press)
        bottom_row.add_widget(bksp_btn)
        bottom_row.add_widget(Label(size_hint_x=1))
        keyboard_layout.add_widget(bottom_row)

        return keyboard_layout

    def on_pre_enter(self):
        self.first_name_input.text = ''
        self.last_name_input.text = ''
        self.lab_spinner.text = 'Select Lab'
        self._set_active_field(self.first_name_input)

    def on_key_press(self, instance):
        if self.active_input is None:
            return
        current_text = self.active_input.text
        key = instance.key_value

        if key == 'Backspace':
            self.active_input.text = current_text[:-1]
        elif key == 'Space':
            self.active_input.text += ' '
        else:
            self.active_input.text += key

    def confirm_user_name(self, first_name, last_name, lab):
        self.data_manager.add_new_user(first_name, last_name, lab)
        self.popup.dismiss()
        app = App.get_running_app()
        app.sm.get_screen('main').mark_stale()
        app.sm.current = 'main'

    def show_confirmation_popup(self, instance):
        first_name = self.first_name_input.text.strip()
        last_name = self.last_name_input.text.strip()
        lab = self.lab_spinner.text

        if not first_name or not last_name:
            self._show_error('Please enter both first and last name.')
            return
        if lab == 'Select Lab':
            self._show_error('Please select a lab.')
            return

        if self.data_manager.check_user_exists(first_name, last_name):
            self.show_user_exists_popup(first_name, last_name)
        else:
            self.show_confirm_user_popup(first_name, last_name, lab)

    def _show_error(self, message):
        content = BoxLayout(orientation='vertical', spacing=10, padding=10)
        content.add_widget(Label(text=message))
        ok_button = Button(text='OK', size_hint_y=None, height=50)
        content.add_widget(ok_button)
        popup = Popup(title='Error', content=content, size_hint=(None, None), size=(400, 200))
        ok_button.bind(on_press=lambda x: popup.dismiss())
        popup.open()

    def show_user_exists_popup(self, first_name, last_name):
        content = BoxLayout(orientation='vertical', spacing=10, padding=10)
        content.add_widget(Label(text=f'User "{first_name} {last_name}" already exists.'))

        ok_button = Button(text='OK', size_hint_y=None, height=50)
        ok_button.bind(on_press=lambda x: self.popup.dismiss())
        content.add_widget(ok_button)

        self.popup = Popup(title='User Exists', content=content, size_hint=(None, None), size=(400, 200))
        self.popup.open()

    def show_confirm_user_popup(self, first_name, last_name, lab):
        display_name = f"{first_name} {last_name} ({lab})"
        content = BoxLayout(orientation='vertical', spacing=10, padding=10)
        content.add_widget(Label(text=f'Create user {display_name}?'))

        buttons_layout = BoxLayout(size_hint_y=None, height=50)
        yes_button = Button(text='Yes', on_press=lambda x: self.confirm_user_name(first_name, last_name, lab))
        no_button = Button(text='No', on_press=lambda x: self.popup.dismiss())
        buttons_layout.add_widget(yes_button)
        buttons_layout.add_widget(no_button)

        content.add_widget(buttons_layout)

        self.popup = Popup(title='Confirm New User', content=content, size_hint=(None, None), size=(400, 200))
        self.popup.open()
