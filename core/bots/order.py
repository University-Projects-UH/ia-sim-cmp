class Order:
    def __init__(self, date, price, volumen, name, order_type = "buy"):
        self.price = price
        self.volumen = volumen
        self.name = name
        self.date = date
        self.order_type = order_type
