from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.app import App

class MainScreen(Screen):
    accepted_debt = 10
    def __init__(self, data_manager, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.data_manager = data_manager

        layout = BoxLayout(orientation='vertical')
        self.add_widget(layout)
        
        # Layout for the alphabet buttons
        alphabet_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.3))
        layout.add_widget(alphabet_layout)

        # Add alphabet buttons
        alphabet_grid = GridLayout(rows=3, spacing=3)
        alphabet_layout.add_widget(alphabet_grid)

        for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
            letter_button = Button(text=letter, size_hint=(1, 1), background_color=(0.8, 0.8, 0.8, 1))
            letter_button.bind(on_press=self.filter_users_by_letter)
            alphabet_grid.add_widget(letter_button)
            letter_button.font_size = '26sp'
            letter_button.spacing = (3, 3)
            letter_button.halign = 'center'
        
        # add another option "all" to show all users
        all_button = Button(text='Rank', size_hint=(1, 1), background_color=(0.8, 0.8, 0.8, 1))
        all_button.bind(on_press=self.update_user_list)
        alphabet_grid.add_widget(all_button)
        all_button.font_size = '26sp'
        all_button.spacing = (3, 3)            

        # Button to contribute
        contribute_button = Button(text='Contribute', size_hint=(1, 0.1), background_color=(0.4, 0.6, 1, 1), height=20)
        contribute_button.bind(on_press=self.go_to_contribute_screen)
        layout.add_widget(contribute_button)
        
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

    
    def get_users_with_total_scores(self):
        users = self.data_manager.get_users_recently_consumed()
        cleanings = self.data_manager.get_recent_cleanings()

        # Create a dictionary to map users to their total credit from cleanings
        user_credits = {}
        for user, _, credit in cleanings:
            if user in user_credits:
                user_credits[user] += credit
            else:
                user_credits[user] = credit

        # Add credit to the score for each user
        users_with_total_scores = []
        for user, score, debt in users:
            debt = max(debt, 0) # no money for users who only clean but do not drink 
            total_score = score + user_credits.get(user, 0)  # Add the credit to the score
            users_with_total_scores.append([user, total_score, debt])

        users_with_total_scores.sort(key=lambda x: x[1], reverse=True)
        users_with_total_scores = [x + [y,] for x, y in zip(users_with_total_scores, range(1, len(users_with_total_scores) + 1))]
        return users_with_total_scores

    def filter_users_by_letter(self, instance):
        selected_letter = instance.text
        users = self.get_users_with_total_scores()
        filtered_users = []
        for user_row in users: 
            if user_row[0].startswith(selected_letter):
                filtered_users.append(user_row)

        self.user_layout.clear_widgets()
        for user, score, debt, rank in filtered_users:
            button_color = (0.6, 0.4, 1, 1) if debt < self.accepted_debt else (1, 0.4, 0.6, 1)
            button_text = f'{user} \n Rank {rank} - Two Week Score: {score:.2f} - Debt: {debt:.2f} '
            if debt >= self.accepted_debt: 
                button_text += " - Pay up!"
            user_button = Button(text=button_text, 
                size_hint_y=None, 
                height=80,
                font_size='30sp',
                bold=True,
                halign='center',
                valign='middle',
                padding=(15, 15),
                background_color=button_color)
            user_button.bind(on_press=self.on_user_button_press)
            self.user_layout.add_widget(user_button)

    def on_pre_enter(self):
        self.update_user_list()

    def update_user_list(self, instance=None):
        self.user_layout.clear_widgets()
        users = self.get_users_with_total_scores()
        for user, score, debt, rank in users:
            button_color = (0.6, 0.4, 1, 1) if debt < self.accepted_debt else (1, 0.4, 0.6, 1)
            button_text = f'{user} \n Rank {rank} - Two Week Score: {score:.2f} - Debt: {debt:.2f} ' 
            if debt >= self.accepted_debt: 
                button_text += " - Pay up!"
            user_button = Button(text=button_text, 
                size_hint_y=None, 
                height=80,
                font_size='30sp',
                bold=True,
                halign='center',
                valign='middle',
                padding=(15, 15),
                background_color=button_color)
            user_button.bind(on_press=self.on_user_button_press)
            self.user_layout.add_widget(user_button)
    
    def on_user_button_press(self, instance):
        selected_user = instance.text.split(' \n')[0]
        print(f"Selected user: {selected_user}")

        # Retrieve data 
        users = self.get_users_with_total_scores()
        user_data = next((u for u in users if u[0] == selected_user), None)

        if not user_data:
            return

        user, score, debt, rank = user_data

        # If debt > high 
        if debt > 10:
            self.show_payment_popup(lambda: self.on_user_button_press_after(selected_user))

        if debt > 12:
            for i in range(int(debt - 12)):
                self.show_payment_popup_lvl2(lambda: self.on_user_button_press_after(selected_user), exclamation_mark=i + 1)

        # Personalized Message
        #if selected_user == '5TR':
        #    App.get_running_app().show_global_emoji("Hello 5TR!")


        self.on_user_button_press_after(selected_user)

    def on_user_button_press_after(self, selected_user):
        app = App.get_running_app()
        app.sm.current = 'select_coffee'
        app.sm.get_screen('select_coffee').set_selected_user(selected_user)

    def go_to_add_user_screen(self, instance):
        self.manager.current = 'new_user'

    def go_to_contribute_screen(self, instance):
        self.manager.current = 'contribute_screen'


    def show_payment_popup(self, on_dismiss_callback):

        label = Label(
            text='Looks like your caffeine karma is a bit off balance. Toss a coin to your coffee crew and pay up!',
            font_size='20sp',
            halign='center',
            valign='middle'
        )

        label.bind(size=lambda instance, value: setattr(instance, 'text_size', (value[0], None)))


        content = BoxLayout(orientation='vertical', spacing=10, padding=10)
        content.add_widget(label)

        btn = Button(text='Got it!', size_hint=(1, 0.4), font_size='20sp')
        content.add_widget(btn)

        popup = Popup(title='Friendly Bean Reminder',
                    content=content,
                    size_hint=(0.7, 0.4),
                    auto_dismiss=False)

        btn.bind(on_press=lambda instance: self.dismiss_popup_and_continue(popup, on_dismiss_callback))
        popup.open()

    
    def show_payment_popup_lvl2(self, on_dismiss_callback, exclamation_mark):

        label = Label(
            text=f'Bro, your caffeine karma is severely out of balance{"!"*exclamation_mark} You better pay up.',
            font_size=f'{22 + 2 * exclamation_mark}sp',
            halign='center',
            valign='middle'
        )

        label.bind(size=lambda instance, value: setattr(instance, 'text_size', (value[0], None)))


        content = BoxLayout(orientation='vertical', spacing=10, padding=10)
        content.add_widget(label)

        btn = Button(text='Got it!', size_hint=(1, 0.4), font_size='20sp')
        content.add_widget(btn)

        popup = Popup(title='Not so Friendly Bean Reminder',
                    content=content,
                    size_hint=(0.7, 0.4),
                    auto_dismiss=False)

        btn.bind(on_press=lambda instance: self.dismiss_popup_and_continue(popup, on_dismiss_callback))
        popup.open()


    def dismiss_popup_and_continue(self, popup, callback):
        popup.dismiss()
        callback()