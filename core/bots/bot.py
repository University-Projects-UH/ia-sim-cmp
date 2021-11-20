from prettytable import PrettyTable

class Bot:
    def __init__(self, name, take_profit, stop_loss, investment):
        self.name = name
        self.take_profit = take_profit
        self.stop_loss = stop_loss
        self.investment = investment
        self.profit = 0
        self.operation_history = []

    # price: price at the moment of execute the operation
    # operation_type:
    #    - sell
    #    - buy
    def insert_operation(self, time, price, operation_type, volumen, asset):
        self.operation_history.append([time, price, operation_type, volumen, asset])

    def print_bot_info(self):
        print("Name: " + self.name)
        print("Investment: " + str(self.investment))
        print("Take profit: " + str(self.take_profit))
        print("Stop Lost: " + str(self.take_profit))
        print("Profit: " + str(self.profit))

    def print_operation_history(self):
        table = PrettyTable(["Time", "Price", "Operation", "Volumen", "Asset"])
        for row in self.operation_history:
            table.add_row(row)
        print(table.get_string())

