from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label

import json

class SelectCoffeeScreen(Screen):
    def __init__(self, data_manager, **kwargs):
        super(SelectCoffeeScreen, self).__init__(**kwargs)
        self.data_manager = data_manager

        self.load_products()
        self.selected_product = None
        self.create_layout()

    def on_pre_enter(self):
        self.load_products()
        self.selected_product = None
        self.on_selected_product_change()

    def load_products(self):
        with open('products.json', 'r') as file:
            self.products_data = json.load(file)['products']
        self.products = {product['name']: product for product in self.products_data}

    def create_layout(self):
        main_layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

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

        # Label for products
        product_label = Label(text='Products', size_hint=(None, None), height=30, color=(1, 1, 1, 1), font_size=20, bold=True)
        main_layout.add_widget(product_label)

        # Product selection grid layout
        self.product_grid_layout = GridLayout(cols=2, spacing=10, padding=10)
        for product_name in self.products.keys():
            btn = Button(
                text=product_name,
                size_hint=(None, None),
                size=(150, 50)
            )
            btn.bind(on_release=self.select_product)
            self.product_grid_layout.add_widget(btn)
        main_layout.add_widget(self.product_grid_layout)

        # Options layout
        options_label = Label(text='Options', size_hint=(None, None), height=30, color=(1, 1, 1, 1), font_size=20, bold=True)
        main_layout.add_widget(options_label)

        # box layout should be aligned top
        self.options_layout = BoxLayout(orientation='horizontal', padding=10, height=60, pos_hint={'top': 1}, size_hint=(1, None))
        main_layout.add_widget(self.options_layout)

        # Confirmation button
        confirm_button = Button(
            text='Confirm Selection',
            size_hint=(None, None),
            size=(200, 50),
            pos_hint={'center_x': 0.5}
        )
        confirm_button.bind(on_press=self.confirm_selection)
        main_layout.add_widget(confirm_button)

        self.add_widget(main_layout)

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
        self.create_options()

    def create_options(self):
        self.options_layout.clear_widgets()
        if self.selected_product:
            selected_product_data = self.products[self.selected_product]
            if 'options' in selected_product_data:
                for option in selected_product_data['options']:
                    if 'selected' not in option:
                        option['selected'] = False

                    btn = Button(
                        text=option['name'],
                        size_hint=(None, None),
                        size=(250, 50),
                        background_color=(1, 1, 1, 1)
                    )
                    btn.bind(on_release=self.toggle_option)
                    self.options_layout.add_widget(btn)

    def toggle_option(self, button):
        button.background_color = (1, 1, 1, 1) if button.background_color == [0, 1, 0, 1] else [0, 1, 0, 1]

        selected_product_data = self.products[self.selected_product]
        for option in selected_product_data['options']:
            if option['name'] == button.text:
                option['selected'] = not option['selected']
                break

    def confirm_selection(self, button):
        # Your logic to handle the confirmed selection
        pass