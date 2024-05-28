from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label

class PaymentScreen(Screen):
    def __init__(self, data_manager,**kwargs):
        super(PaymentScreen, self).__init__(**kwargs)
        self.data_manager = data_manager

        layout = BoxLayout(orientation='vertical')

        self.label = Label(text='Confirm Payment:')
        layout.add_widget(self.label)

        confirm_button = Button(text='Pay Now')
        confirm_button.bind(on_press=self.confirm_payment)
        layout.add_widget(confirm_button)

        self.add_widget(layout)

    def confirm_payment(self, instance):
        # Logic to handle payment
        self.manager.current = 'main'