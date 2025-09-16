# Simple stub for testing purposes
class MockQRCode:
    def __init__(self, *args, **kwargs):
        pass
    
    def add_data(self, *args, **kwargs):
        pass
    
    def make(self, *args, **kwargs):
        pass
    
    def make_image(self, *args, **kwargs):
        class MockImage:
            def save(self, *args, **kwargs):
                pass
        return MockImage()

def make(*args, **kwargs):
    class MockQR:
        def save(self, *args, **kwargs):
            pass
    return MockQR()

class MockConstants:
    ERROR_CORRECT_L = 1
    ERROR_CORRECT_M = 2
    ERROR_CORRECT_Q = 3
    ERROR_CORRECT_H = 4

# Mock the qrcode module
import sys
import types

qrcode_module = types.ModuleType('qrcode')
qrcode_module.make = make
qrcode_module.QRCode = MockQRCode
qrcode_module.constants = MockConstants()
sys.modules['qrcode'] = qrcode_module

# Mock pandas
pandas_module = types.ModuleType('pandas')
sys.modules['pandas'] = pandas_module