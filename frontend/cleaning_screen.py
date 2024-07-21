from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.popup import Popup

import json

class CleaningScreen(Screen):
    def __init__(self, data_manager, **kwargs):
        super(CleaningScreen, self).__init__(**kwargs)
        self.data_manager = data_manager
        self.selected_user = None

        self.load_products()
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

    def load_products(self):
        with open('cleaning.json', 'r') as file:
            self.products_data = json.load(file)['cleaning']
        self.products = {product['name']: product for product in self.products_data}

    def create_layout(self):
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

        # Label for products
        product_label = Label(text='Products', size_hint=(None, None), height=30, color=(1, 1, 1, 1), font_size=20, bold=True)
        self.main_layout.add_widget(product_label)        

        # Product selection grid layout
        self.product_grid_layout = GridLayout(cols=1, rows=len(self.products), spacing=10, padding=10)
        self.update_product_list()

        self.add_widget(self.main_layout)

    def update_product_list(self):
        needs_cleaning = False
        for product_name in self.products.keys():
            if self.data_manager.get_cleanings_in_current_window(self.products[product_name]["name"], self.products[product_name]["downtime"]) == []:
                print("Need cleaning")
                price = "{:.2f}".format(-1 * self.products[product_name]['price'])  # Format the price with two decimal places
                btn = Button(
                    text=product_name + f' - Credit: ' + price + '€',  # Use the formatted price
                    size_hint=(None, None),
                    size=(650, 75),
                    font_size='26sp',
                )
                btn.bind(on_release=self.select_product)

                needs_cleaning = True
                self.product_grid_layout.add_widget(btn)
        self.main_layout.add_widget(self.product_grid_layout)

        # Add a message if no cleaning is necessary
        if not needs_cleaning:
            no_cleaning_label = Label(
                text="No cleaning necessary",
                size_hint=(None, None), 
                height=30, 
                color=(1, 1, 1, 1), 
                font_size=40, 
                bold=True,
                pos_hint={'center_x': 0.5, 'center_y': 0.5}  # Center the label
                )
            self.main_layout.add_widget(no_cleaning_label)

        if needs_cleaning: 
            # Confirmation button
            confirm_button = Button(
                text='Confirm Selection',
                size_hint=(None, None),
                size=(225, 60),
                pos_hint={'center_x': 0.5},
                font_size='26sp'
            )
            confirm_button.bind(on_press=self.show_confirmation_popup)
            self.main_layout.add_widget(confirm_button)

    def go_back(self, instance):
        self.manager.current = 'main'

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

    def reset_layout(self):
        self.main_layout.clear_widgets()
        self.create_layout()

    def confirm_selection(self, button):
        if self.selected_product is not None:
            # update database
            selected_product_data = self.products[self.selected_product.split(' - ')[0]]
            total_price = selected_product_data['price']
            self.data_manager.add_cleaning(self.selected_user, self.selected_product.split(' - ')[0], total_price)

            # clear widgets
            self.reset_layout()
            self.manager.get_screen('select_coffee').reset_layout() # turn button grey

            # return to main
            self.manager.current = 'main'
            self.popup.dismiss()

        
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
        
    def show_confirmation_popup(self, button):
        if self.selected_product is not None:
            summary = f'User: {self.selected_user}\n'
            summary += f'Cleaning Type: {self.selected_product.split(" - ")[0]}\n'
            summary += f'Debt will never be negative.'
            selected_product_data = self.products[self.selected_product.split(' - ')[0]]
            total_price = selected_product_data['price']
            summary += f'\nCredit: {-1 * total_price:.2f}€'
            
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
        