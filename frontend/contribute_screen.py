from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image

import qrcode


class ContributeScreen(Screen):
    def __init__(self, **kwargs):
        super(ContributeScreen, self).__init__(**kwargs)
        self.repo_url = "https://github.com/rgroh1996/aibe_coffee"

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

        # Add a label
        contribute_label = Label(
            text='Contribute to our project by visiting the GitHub repository.\nScan the QR code below:',
            size_hint_y=None,
            height=60,
            color=(1, 1, 1, 1),
            font_size=16,
            text_size=(None, None),
            valign='middle',
            halign='center'
        )
        main_layout.add_widget(contribute_label)
        
        # Add spacer
        main_layout.add_widget(Label(size_hint_y=0.1))
        
        # Add contribution QR code
        qr_img_path = self.get_contribution_img_path(self.repo_url)
        qr_img = Image(
            source=qr_img_path,
            size_hint=(1, None),
            height=300
        )
        main_layout.add_widget(qr_img)
        
        # Add spacer
        main_layout.add_widget(Label(size_hint_y=0.1))

        self.add_widget(main_layout)
        
    def go_back(self, instance):
        self.manager.current = 'main'
    
    def get_contribution_img_path(self, url):
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
        path = "contribution_tmp.png"
        img.save(path)
        return path