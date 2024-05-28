from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from frontend.main_screen import MainScreen
from frontend.select_coffee_screen import SelectCoffeeScreen
from frontend.payment_screen import PaymentScreen
from frontend.new_user_screen import NewUserScreen

from backend.data_manager import DataManager

class CoffeeListApp(App):
    def build(self):

        # initialize the data manager
        self.data_manager = DataManager("database/aibe_coffee.db")

        sm = ScreenManager()
        sm.add_widget(MainScreen(name='main', data_manager=self.data_manager))
        sm.add_widget(SelectCoffeeScreen(name='select_coffee', data_manager=self.data_manager))
        sm.add_widget(PaymentScreen(name='payment', data_manager=self.data_manager))
        sm.add_widget(NewUserScreen(name='new_user', data_manager=self.data_manager))
        return sm

if __name__ == '__main__':
    CoffeeListApp().run()
