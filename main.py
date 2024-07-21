from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from frontend.main_screen import MainScreen
from frontend.select_coffee_screen import SelectCoffeeScreen
from frontend.payment_screen import PaymentScreen
from frontend.new_user_screen import NewUserScreen
from frontend.cleaning_screen import CleaningScreen
from kivy.config import Config

import threading
import argparse

from backend.data_manager import DataManager
from backend.shelly_log import log_voltage_main, test_connection

# Set configuration for full screen mode
Config.set('graphics', 'fullscreen', 'auto')
Config.write()

class CoffeeListApp(App):
    def build(self):

        # initialize the data manager
        self.data_manager = DataManager("database/aibe_coffee.db")

        sm = ScreenManager()
        sm.add_widget(MainScreen(name='main', data_manager=self.data_manager))
        sm.add_widget(SelectCoffeeScreen(name='select_coffee', data_manager=self.data_manager))
        sm.add_widget(PaymentScreen(name='payment', data_manager=self.data_manager))
        sm.add_widget(NewUserScreen(name='new_user', data_manager=self.data_manager))
        sm.add_widget(CleaningScreen(name='cleaning', data_manager=self.data_manager))
        return sm

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Start the Coffee List App with optional voltage logging.')
    parser.add_argument('--noshelly', action='store_true', help='Do not start the smart plug voltage logging.')
    args = parser.parse_args()

    # Signal for background thread to stop
    stop_signal = threading.Event()

    stop_if_no_shelly = not args.noshelly
    if not test_connection() and stop_if_no_shelly:
        raise ValueError("Shelly not connected")

    # Create and start the thread
    thread = threading.Thread(target=log_voltage_main, args=(stop_signal,))
    # Start the thread
    thread.start()
    
    # Run the coffee list app
    CoffeeListApp().run()
    
    stop_signal.set()
    # Wait for the thread to finish
    thread.join()
