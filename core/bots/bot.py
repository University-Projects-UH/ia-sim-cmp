from prettytable import PrettyTable

class Bot:
    def __init__(self, name, stop_loss, take_profit, investment):
        self.name = name
        self.take_profit = take_profit
        self.stop_loss = stop_loss
        self.investment = investment
        self.opened_orders = []
        self.operation_history = []

    def append_order_to_history(self, order):
        self.operation_history.append(order)

    def print_bot_info(self):
        print("Name: " + self.name)
        print("Investment: " + str(self.investment) + "$")
        print("Take profit: " + str(self.take_profit))
        print("Stop Lost: " + str(self.take_profit))

    def print_operation_history(self):
        table = PrettyTable(["Date", "Price", "Volumen", "Asset", "Volumen USD", "Type"])
        for order in self.operation_history:
            table.add_row([order.date, order.price, order.volumen, order.name,\
                           order.price * order.volumen, order.order_type])
        print(table.get_string())

