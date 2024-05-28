from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label

class MainScreen(Screen):
    def __init__(self, data_manager, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.data_manager = data_manager

        layout = BoxLayout(orientation='vertical')
        self.add_widget(layout)
        
        # Scrollable list of user buttons
        scroll_view = ScrollView(size_hint=(1, 0.9))
        self.user_layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        self.user_layout.bind(minimum_height=self.user_layout.setter('height'))
        
        scroll_view.add_widget(self.user_layout)
        layout.add_widget(scroll_view)
        
        # Button to add new user
        add_user_button = Button(text='Add New User', size_hint=(1, 0.1), background_color=(1, 0.6, 0.4, 1), height=20)
        add_user_button.bind(on_press=self.go_to_add_user_screen)
        layout.add_widget(add_user_button)

    def on_pre_enter(self):
        self.update_user_list()

    def update_user_list(self):
        self.user_layout.clear_widgets()
        users = self.data_manager.load_users_and_debts()

        for user, debt in users:
            user_button = Button(text=f'{user} \n Debt: {debt}', 
                size_hint_y=None, 
                height=60,
                font_size='20sp',
                bold=True,
                halign='center',
                valign='middle',
                padding=(15, 15),
                background_color=(0.6, 0.4, 1, 1))
            user_button.bind(on_press=self.on_user_button_press)
            self.user_layout.add_widget(user_button)
    
    def on_user_button_press(self, instance):
        # Here you can handle passing the selected user's data to the coffee selection screen
        self.manager.current = 'select_coffee'
    
    def go_to_add_user_screen(self, instance):
        self.manager.current = 'new_user'
