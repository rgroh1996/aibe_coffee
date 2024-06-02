from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image

import qrcode

class PaymentScreen(Screen):
    def __init__(self, data_manager,**kwargs):
        super(PaymentScreen, self).__init__(**kwargs)
        self.data_manager = data_manager
        self.selected_user = None
        self.user_debt = 0

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

        # Add user label
        self.user_label = Label(
            text='Selected User: None',
            size_hint_y=None,
            height=40,
            color=(1, 1, 1, 1),
            font_size=22,
            text_size=(None, None),
            valign='middle',
            halign='center',
            bold=True
        )
        main_layout.add_widget(self.user_label)
        
        # Add label showing the debts
        self.debt_label = Label(
            text='Debt: 0.00 €',
            size_hint_y=None,
            height=40,
            color=(1, 1, 1, 1),
            font_size=22,
            text_size=(None, None),
            valign='middle',
            halign='center',
            bold=True
        )
        main_layout.add_widget(self.debt_label)
        
        paypal_name = '@coffeeataibe'
        paypal_name_label = Label(
            text=f'Please pay using PayPal: {paypal_name}\nor scan the QR code below',
            size_hint_y=None,
            height=40,
            color=(1, 1, 1, 1),
            font_size=16,
            text_size=(None, None),
            valign='middle',
            halign='center'
        )
        main_layout.add_widget(paypal_name_label)
        
        # Add spacer
        main_layout.add_widget(Label())
        
        # Add payment QR code
        payment_img_path = self.get_payment_img_path(0)
        payment_img = Image(
            source=payment_img_path,
            size_hint=(1, None),
            height=300
        )
        main_layout.add_widget(payment_img)
        
        # Add spacer
        main_layout.add_widget(Label())

        # Add payment confirmation button
        confirm_button = Button(
            text='Confirm Payment',
            size_hint_y=None,
            height=120,
            background_color=(0.6, 0.6, 0.6, 1),
            color=(1, 1, 1, 1)
        )
        confirm_button.bind(on_press=self.confirm_payment)
        main_layout.add_widget(confirm_button)
        
        self.add_widget(main_layout)
        
    def go_back(self, instance):
        self.manager.current = 'main'
    
    def update_user_label(self):
        if self.selected_user:
            self.user_label.text = f'Selected User: {self.selected_user}'
            
            # update debt
            self.user_debt = self.data_manager.get_user_debt(self.selected_user)
            self.debt_label.text = f'Debt: {self.user_debt:.2f} €'

    def set_selected_user(self, user_name):
        self.selected_user = user_name
        self.update_user_label()
    
    def get_payment_img_path(self, debt):
        url=f"paypal.me/coffeeataibe/{debt:.2f}"
        # Generate QR code
        qr = qrcode.QRCode(
            version=1,  # controls the size of the QR Code; 1 is the smallest, and it increases to hold more data
            error_correction=qrcode.constants.ERROR_CORRECT_L,  # controls the error correction used for the QR Code
            box_size=10,  # controls how many pixels each “box” of the QR code is
            border=4,  # controls how many boxes thick the border should be
        )
        qr.add_data(url)
        qr.make(fit=True)

        # Create an image from the QR Code instance
        img = qr.make_image(fill_color="black", back_color="white")

        # Save the image to a file
        path = "payment_tmp.png"
        img.save(path)
        return path 

    def confirm_payment(self, instance):
        # Pay debt and update debt in the database
        self.data_manager.pay_debt(self.selected_user, self.user_debt)
        
        # Back to main screen
        self.manager.current = 'main'