from . import Bot

class SmartBot(Bot):
    def __init__(self, name, stop_loss, take_profit, investment, assetAB, stacking = False):
        super().__init__(name, stop_loss, take_profit, investment)
        self.assetAB = assetAB
        self.count_rows = len(assetAB.asset_data.index)

    def print_bot_info(self):
        super().print_bot_info()
        print("Pair: " + self.assetAB.name)
        super().print_operation_history()

    def get_simple_MA(self, days = 20, position = None):
        if position is None:
            position = len(self.assetAB.asset_data.index) - 1
        count = days
        price_sum = 0
        close_prices = self.assetAB.asset_data['Close']
        while count > 0 and position > 0:
            price_sum += close_prices[position]
            count -= 1
            position -= 1

        return price_sum / days

    def get_close_price(self, position = 0):
        return self.assetAB.asset_data['Close'][position]

    # Exponential Moving Average
    # EMA = close_price * multiplier + EMA(previous_day) * (1 - multiplier)
    # multiplier = smoothing / (1 + period)
    # commonly smoothing is equal to 2
    def get_EMA(self, price_func, count = 10, position = 0, period = 10, smoothing = 2):
        multiplier = smoothing / (1 + period)
        ema_today = price_func(position) * multiplier
        if(position == 0 or count == 0):
            return ema_today
        return ema_today + self.get_EMA(count - 1, position - 1, period) * (1 - multiplier)

    # Moving Average Convergence / Divergence
    def get_MACD(self, position = 0):
        return self.get_EMA(self.get_close_price ,12, position, 12) - self.get_EMA(self.get_close_price, 26, position, 26)

    # Signal Line is an EMA with macd and period equal to 9
    def get_signal_line(self, position = 0):
        return self.get_EMA(self.get_MACD, 9, position, 9)

    # Relative Strength
    # RS = Avg Gain / Avg Loss
    def get_RS(self, position, period):
        if(position < period):
            return None
        count = period
        gain = []
        loss = []
        while count > 0:
            diff = self.assetAB.asset_data['Close'] - self.assetAB.asset_data['Open']
            if(diff < 0):
                loss.append(diff)
            else:
                gain.append(diff)
        return (sum(gain) / len(gain)) / (-1 * sum(loss)/ len(loss))

    # Relative Strength Index
    # RSI = 100 - (100 / (1 + RS))
    def get_RSI(self, period = 14, position = 0):
        return 100 - (100 / (1 + self.get_RS(position, period)))

    def close_bot(self, price):
        for order in self.opened_orders:
            self.investment += order.volumen * (1 + price - order.price)

    def start_bot(self, position = 0):
        last_day_price = -1
        while position < self.count_rows:
           day_price = self.assetAB.get_open_price(position)
           position += 1
           if(last_day_price == -1):
               pass

           # close bot if it hit the take profit line
           if(day_price >= self.take_profit):
               self.close_bot(self.take_profit)
           # close bot if it fall below the stop loss line
           if(day_price <= self.stop_loss):
               self.close_bot(self.stop_loss)

