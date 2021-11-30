from .bot import Bot

class Order:
    def __init__(self, price, volumen):
        self.price = price
        self.volumen = volumen

class SmartBot(Bot):
    def __init__(self, name, stop_loss, take_profit, investment, assetAB, stacking = False):
        super().__init__(name, stop_loss, take_profit, investment)
        self.assetAB = assetAB
        self.opened_orders = []
        self.count_rows = len(assetAB.asset_data.index)

    def print_bot_info(self):
        super().print_bot_info()
        print("Pair: " + self.assetAB.name)
        super().print_operation_history()

    def get_simple_MA(self, days = 20, position = None):
        if position is None:
            position = len(self.asset_data.index) - 1
        count = days
        price_sum = 0
        close_prices = self.asset_data['Close']
        while count > 0 and position > 0:
            price_sum += close_prices[position]
            count -= 1
            position -= 1

        return price_sum / days

    # Exponential Moving Average
    # EMA = close_price * multiplier + EMA(previous_day) * (1 - multiplier)
    # multiplier = smoothing / (1 + period)
    # commonly smoothing is equal to 2
    def get_EMA(self, count = 10, position = 0, period = 10):
        multiplier = 2 / (1 + period)
        ema_today = self.assetAB.asset_data['Close'] * multiplier
        if(position == 0 or count == 0):
            return ema_today
        return ema_today + self.get_EMA(count - 1, position - 1, period) * (1 - multiplier)

    def start_bot(self, position = 0):
        while position < self.count_rows:
           day_prices = self.assetAB.get_day_prices(position)
           position += 1
