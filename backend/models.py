class User:
    def __init__(self, name, debt=0.0):
        self.name = name
        self.debt = debt

    def add_debt(self, amount):
        self.debt += amount

    def pay_debt(self):
        self.debt = 0.0

    def __repr__(self):
        return f"User(name={self.name}, debt={self.debt})"


class Coffee:
    def __init__(self, coffee_type, milk=False, sugar=False):
        self.coffee_type = coffee_type
        self.milk = milk
        self.sugar = sugar
        self.price = self.calculate_price()

    def calculate_price(self):
        base_price = 2.5  # base price for a coffee
        if self.milk:
            base_price += 0.5
        if self.sugar:
            base_price += 0.2
        return base_price

    def __repr__(self):
        return f"Coffee(coffee_type={self.coffee_type}, milk={self.milk}, sugar={self.sugar}, price={self.price})"
