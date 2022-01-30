from .bot import Bot
import datetime

class SmartBot(Bot):
    def __init__(self, name, stop_loss, take_profit, investment, assets_array, stacking = False):
        super().__init__(name, stop_loss, take_profit, investment, assets_array)
        self.opened_orders = []
        self.profit = 0

    def print_bot_info(self):
        super().print_bot_info()
        print("Pair: " + " | ".join(self.assets_array))
        super().print_operation_history()

    # get how many assets B are needed to buy 1 assetA at a date
    def get_close_price_at_date(self, date):
        assetA_price = self.assets_array[0].get_close_price_by_date(date)
        if(len(self.assets_array) == 1):
            return assetA_price
        assetB_price = self.assets_array[1].get_close_price_by_date(date)
        return assetA_price / assetB_price

    def get_open_price_at_date(self, date):
        assetA_price = self.assets_array[0].get_open_price_by_date(date)
        if(len(self.assets_array) == 1):
            return assetA_price
        assetB_price = self.assets_array[1].get_open_price_by_date(date)
        return assetA_price / assetB_price

    def get_simple_MA(self, date, days = 20):
        count = days
        price_sum = 0
        while count > 0:
            price_at_date = self.get_close_price_at_date(date)
            price_sum += price_at_date
            count -= 1
            date -= datetime.timedelta(days = 1)

        return price_sum / days

    # Exponential Moving Average
    # EMA = close_price * multiplier + EMA(previous_day) * (1 - multiplier)
    # multiplier = smoothing / (1 + period)
    # commonly smoothing is equal to 2
    def get_EMA(self, price_func, date, count = 10, period = 10, smoothing = 2):
        multiplier = smoothing / (1 + period)
        ema_today = price_func(date) * multiplier
        if(count == 0):
            return ema_today

        date -= datetime.timedelta(days = 1)
        return ema_today + self.get_EMA(count - 1, date, period) * (1 - multiplier)

    # Moving Average Convergence / Divergence
    def get_MACD(self, date):
        return self.get_EMA(self.get_close_price_at_date,12, date, 12) \
            - self.get_EMA(self.get_close_price_at_date, 26, date, 26)

    # Signal Line is an EMA with macd and period equal to 9
    def get_signal_line(self, date):
        return self.get_EMA(self.get_MACD, 9, date, 9)

    # Relative Strength
    # RS = Avg Gain / Avg Loss
    def get_RS(self, date, period):
        count = period
        gain = []
        loss = []
        while count > 0:
            diff = self.get_close_price_at_date(date) - self.get_open_price_at_date(date)
            if(diff < 0):
                loss.append(diff)
            else:
                gain.append(diff)
            date += datetime.timedelta(days = 1)
        return (sum(gain) / len(gain)) / (-1 * sum(loss)/ len(loss))

    # Relative Strength Index
    # RSI = 100 - (100 / (1 + RS))
    def get_RSI(self, date, period = 14):
        return 100 - (100 / (1 + self.get_RS(date, period)))

    def close_bot_at_price(self, price):
        for order in self.opened_orders:
            self.investment += order.volumen * (1 + price - order.price)

    # check stop loss and take profit
    def verify_sl_and_tp(self, price):
        if(price >= self.take_profit):
            self.close_bot_at_price(self.take_profit)
        elif(price <= self.stop_loss):
            self.close_bot_at_price(self.stop_loss)
        return price <= self.stop_loss or price >= self.take_profit

    def print_summary(self, start_date, max_date):
        #self.print_operation_history()
        print("Start date: " + str(start_date))
        print("End date: " + str(max_date))
        percent_profit = (self.profit * 100) / self.investment
        print("Profit: " + str(self.profit) + " | " + str(percent_profit) + "%")

    def start_bot(self, date = None):
        if(date is None):
            date = self.get_lower_date()
        start_date = date
        max_date = self.get_upper_date()
        while date <= max_date:
            price = self.get_close_price_at_date(date)
            if(self.verify_sl_and_tp(price)):
                break

            date += datetime.timedelta(days = 1)

        price = self.get_close_price_at_date(date - datetime.timedelta(days = 1))
        self.close_bot_at_price(price)
        self.print_summary(start_date, max_date)

