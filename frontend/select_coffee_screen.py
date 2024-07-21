from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.popup import Popup

import json

class SelectCoffeeScreen(Screen):
    def __init__(self, data_manager, **kwargs):
        super(SelectCoffeeScreen, self).__init__(**kwargs)
        self.data_manager = data_manager
        self.selected_user = None

        self.load_products()
        self.load_cleanings()
        self.selected_product = None
        self.create_layout()
    
    def set_selected_user(self, user_name):
        self.selected_user = user_name
        self.update_user_label()
    
    def update_user_label(self):
        if self.selected_user:
            self.user_label.text = f'Selected User: {self.selected_user}'

    def on_pre_enter(self):
        self.load_products()
        self.selected_product = None
        self.on_selected_product_change()

    def load_cleanings(self):
        with open('cleaning.json', 'r') as file:
            self.cleaning_data = json.load(file)['cleaning']
        self.cleanings = {product['name']: product for product in self.cleaning_data}

    def load_products(self):
        with open('products.json', 'r') as file:
            self.products_data = json.load(file)['products']
        self.products = {product['name']: product for product in self.products_data}

    def cleanings_overdue(self): 
        for product in self.cleanings.keys(): 
            if self.data_manager.get_cleanings_in_current_window(self.cleanings[product]["name"], self.cleanings[product]["downtime"]) == []:
                return True
        return False
        
    def reset_layout(self):
        self.clear_widgets()
        self.create_layout()

    def create_layout(self):
        # cleaning condition 
        self.main_layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        # Add the back button at the top
        back_button = Button(
            text='Back to main screen',
            size_hint_y=None,
            height=40,
            background_color=(0.6, 0.6, 0.6, 1),  # Gray color for the back button
            color=(1, 1, 1, 1)  # White text color
        )
        back_button.bind(on_press=self.go_back)
        self.main_layout.add_widget(back_button)
        
        # User Label that should be aligned left
        self.user_label = Label(
            text='Selected User: None',
            size_hint_y=None,
            height=40,
            color=(1, 1, 1, 1),
            font_size=20,
            text_size=(None, None),
            valign='middle',
            halign='left'
        )
        self.main_layout.add_widget(self.user_label)
         
        cond = self.cleanings_overdue()

        # Horizontal BoxLayout for "Pay Debts" and "Start Cleaning" buttons
        button_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=50, spacing=10)
        
        # Button for paying debts
        pay_button = Button(
            text='Pay Debts',
            size_hint=(None, None),
            size=(150, 50),
            pos_hint={'center_x': 0.5} if not cond else {}
        )

        pay_button.bind(on_press=self.pay_debts)
        button_layout.add_widget(pay_button)        
            # Conditionally add the "Start Cleaning" button
        cleaning_background = (1, 0.4, 0.6, 1) if cond else (1,1,1,1) 
        start_cleaning_button = Button(
            text='Start Cleaning',
            background_color=cleaning_background,
            size_hint=(None, None),
            size=(150, 50)
        )
        start_cleaning_button.bind(on_press=self.go_to_start_cleaning_screen)
        button_layout.add_widget(start_cleaning_button)

        # Add the button layout to the main layout
        self.main_layout.add_widget(button_layout)

        # Label for products
        product_label = Label(text='Products', size_hint=(None, None), height=30, color=(1, 1, 1, 1), font_size=20, bold=True)
        self.main_layout.add_widget(product_label)        

        # Product selection grid layout
        self.product_grid_layout = GridLayout(cols=3, spacing=10, padding=10)
        for product_name in self.products.keys():
            price = "{:.2f}".format(self.products[product_name]['price'])  # Format the price with two decimal places
            btn = Button(
                text=product_name + f' - ' + price + '€',  # Use the formatted price
                size_hint=(None, None),
                size=(250, 75),
                font_size='26sp'
            )
            btn.bind(on_release=self.select_product)
            self.product_grid_layout.add_widget(btn)
        self.main_layout.add_widget(self.product_grid_layout)

        # Options layout
        options_label = Label(text='Options', size_hint=(None, None), height=30, color=(1, 1, 1, 1), font_size=20, bold=True)
        self.main_layout.add_widget(options_label)

        # box layout should be aligned top
        self.options_layout = BoxLayout(orientation='horizontal', padding=10, height=60, pos_hint={'top': 1}, size_hint=(1, None))
        self.main_layout.add_widget(self.options_layout)

        # Confirmation button
        confirm_button = Button(
            text='Confirm Selection',
            size_hint=(None, None),
            size=(225, 60),
            pos_hint={'center_x': 0.5},
            font_size='26sp'
        )
        confirm_button.bind(on_press=self.confirm_selection)
        self.main_layout.add_widget(confirm_button)

        self.add_widget(self.main_layout)

    def go_back(self, instance):
        self.manager.current = 'main'

    def go_to_start_cleaning_screen(self, instance):
        self.manager.get_screen('cleaning').set_selected_user(self.selected_user)
        self.manager.current = 'cleaning'

    def select_product(self, button):
        self.selected_product = button.text
        self.update_product_buttons_color()
        self.on_selected_product_change()

    def update_product_buttons_color(self):
        for child in self.product_grid_layout.children:
            if child.text == self.selected_product:
                child.background_color = (0, 1, 0, 1) # Selected color
            else:
                child.background_color = (1, 1, 1, 1)  # Default color

    def on_selected_product_change(self):
        self.load_products()
        self.update_product_buttons_color()
        self.create_options()

    def create_options(self):
        self.options_layout.clear_widgets()
        if self.selected_product:
            selected_product_data = self.products[self.selected_product.split(' - ')[0]]
            if 'options' in selected_product_data:
                for option in selected_product_data['options']:
                    if 'selected' not in option:
                        option['selected'] = False

                    btn = Button(
                        text=option['name'] + ' - ' + str(option['price']) + '€',
                        size_hint=(None, None),
                        size=(200, 60),
                        background_color=(1, 1, 1, 1),
                        font_size='26sp'
                    )
                    btn.bind(on_release=self.toggle_option)
                    self.options_layout.add_widget(btn)

    def toggle_option(self, button):
        button.background_color = (1, 1, 1, 1) if button.background_color == [0, 1, 0, 1] else [0, 1, 0, 1]

        selected_product = self.selected_product.split(' - ')[0]
        selected_product_data = self.products[selected_product]
        
        selected_option = button.text.split(' - ')[0]
        for option in selected_product_data['options']:
            if option['name'] == selected_option:
                # Toggle the selected state
                self.products[selected_product]['options'][selected_product_data['options'].index(option)]['selected'] = not option['selected']
            
    def show_confirmation_popup(self, button):
        if self.selected_product is not None:
            total_price = 0
            summary = f'User: {self.selected_user}\n'
            summary += f'Product: {self.selected_product}\n'
            selected_product_data = self.products[self.selected_product.split(' - ')[0]]
            total_price += selected_product_data['price']
            summary += 'Options:\n'
            if len(selected_product_data['options']) == 0:
                summary += '  - None\n'
            else:
                selected_options = [option for option in selected_product_data['options'] if option['selected']]
                if len(selected_options) == 0:
                    summary += '  - None\n'
                else:
                    for option in selected_options:
                        total_price += option['price']
                        summary += f'  - {option["name"]} - {option["price"]}€\n'
            summary += f'\nTotal Price: {total_price:.2f}€'
            
            content = BoxLayout(orientation='vertical', spacing=10, padding=10)
            content.add_widget(Label(text=summary))
            
            buttons_layout = BoxLayout(size_hint_y=None, height=50)
            yes_button = Button(text='Yes', on_press=self.confirm_selection)
            no_button = Button(text='No', on_press=lambda x: self.popup.dismiss())
            buttons_layout.add_widget(yes_button)
            buttons_layout.add_widget(no_button)
            
            content.add_widget(buttons_layout)
            
            self.popup = Popup(title='Confirm Selection', content=content, size_hint=(None, None), size=(400, 300))
            self.popup.open()
        

    def confirm_selection(self, button):
        if self.selected_product is not None:
            selected_product_data = self.products[self.selected_product.split(' - ')[0]]
            total_price = selected_product_data['price']
            for option in selected_product_data['options']:
                if option['selected']:
                    total_price += option['price']
                    
            selected_options = ','.join([option['name'] for option in selected_product_data['options'] if option['selected']])
            self.data_manager.add_consumed_product(self.selected_user, self.selected_product.split(' - ')[0], selected_options, total_price)
            self.manager.current = 'main'
        
    def pay_debts(self, button):
        # Get debt of the selected user
        debt = self.data_manager.get_user_debt(self.selected_user)
        if debt == 0:
            debt_message = 'No debt to pay'
            # Show a popup with the message
            content = BoxLayout(orientation='vertical', spacing=10, padding=10)
            content.add_widget(Label(text=debt_message))
            ok_button = Button(text='Ok', on_press=lambda x: self.popup.dismiss())
            content.add_widget(ok_button)
            self.popup = Popup(title='Debt Payment', content=content, size_hint=(None, None), size=(400, 300))
            self.popup.open()
        else:                
            self.manager.get_screen('payment').set_selected_user(self.selected_user)
            self.manager.current = 'payment'
        
    