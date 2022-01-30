from prettytable import PrettyTable

class Bot:
    def __init__(self, name, stop_loss, take_profit, investment, assets_array):
        self.name = name
        self.assets_array = assets_array
        self.take_profit = take_profit
        self.stop_loss = stop_loss
        self.investment = investment
        self.operation_history = []

    def append_order_to_history(self, order):
        self.operation_history.append(order)

    def get_lower_date(self):
        low_date = self.assets_array[0].start_date
        for asset in self.assets_array[1:]:
            low_date = min(low_date, asset.start_date)

        return low_date

    def get_upper_date(self):
        upper_date = self.assets_array[0].end_date
        for asset in self.assets_array[1:]:
            upper_date = min(upper_date, asset.end_date)

        return upper_date

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

