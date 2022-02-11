from .bot import Bot
from .order import Order
import datetime
coin_base = "USDT"

class SmartBot(Bot):
    def __init__(self, name, stop_loss, take_profit, investment, assets_array, stacking = False):
        super().__init__(name, stop_loss, take_profit, investment, assets_array)
        self.opened_orders = []
        self.profit = 0
        self.max_open_orders = 10 # fix

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
            diff_percent = diff / self.get_open_price_at_date(date)

            if(diff_percent < 0):
                loss.append(-diff_percent)
                gain.append(0)
            elif(diff_percent > 0):
                gain.append(diff_percent)
                loss.append(0.0)
            else:
                gain.append(0)
                loss.append(0)

            date -= datetime.timedelta(days = 1)
            count -= 1

        sum_gain = sum(gain)
        sum_loss = max(sum(loss),10**(-10))
        len_gain = len(gain)
        len_loss = len(loss)

        # (sum(gain) / len(gain)) / (sum(loss) / len(loss))
        return (sum_gain * len_loss) / (sum_loss * len_gain)

    # Relative Strength Index
    # RSI = 100 - (100 / (1 + RS))
    def get_RSI(self, date, period = 14):
        return 100 - (100 / (1 + self.get_RS(date, period)))

    # close all orders pending
    def close_bot_at_price(self, date, price):
        for order in self.opened_orders:

            sell_order = Order(date,price,order.volumen,order.name,'sell')
            self.append_order_to_history(sell_order)

            self.profit += order.volumen * (price - order.price)

        self.opened_orders.clear()

    # check stop loss and take profit
    def verify_sl_and_tp(self, price):
        if(price >= self.take_profit):
            return True
        elif(price <= self.stop_loss):
            return True
        return False

    def print_summary(self, start_date, max_date):
        #self.print_operation_history()
        print("Start date: " + str(start_date))
        print("End date: " + str(max_date))
        percent_profit = (self.profit * 100) / self.investment
        print("Profit: " + str(self.profit) + " | " + str(percent_profit) + "%")

    def buy(self, date):
        price_at_date = self.get_close_price_at_date(date)
        volumen_by_order = self.investment / self.max_open_orders
        _volumen = volumen_by_order / price_at_date
        asset_pair = self.assets_array[1].name if len(self.assets_array) == 2 else coin_base
        asset_pair = self.assets_array[0].name + '/' + asset_pair

        buy_order = Order(date,price_at_date,_volumen,asset_pair,'buy')
        self.append_order_to_history(buy_order)

        self.opened_orders.append(buy_order)

    def sell(self, date):
        buy_order = self.opened_orders[-1]

        price_at_date = self.get_close_price_at_date(date)

        sell_order = Order(date,price_at_date,buy_order.volumen,buy_order.name,'sell')
        self.append_order_to_history(sell_order)

        self.profit += sell_order.price * sell_order.volumen - buy_order.volumen * buy_order.price

        self.opened_orders.pop()

    def price_compare(self, price_ini, price_fin, percent):
        change = price_fin - price_ini
        change_percent = change / price_ini * 100

        if(percent < 0):
            if(change_percent < percent):
                return True
        elif(change_percent > percent): # and percent >= 1
            return True
        return False

    def operate(self, date):
        rsi = self.get_RSI(date)
        ma = self.get_simple_MA(date,20)

        price_act = self.get_close_price_at_date(date) #  - datetime.timedelta(days = 1)

        can_buy = can_sell = False

        if(rsi >= 70.0 and price_act > ma):
            can_sell = True
        if(rsi <= 30.0 and price_act < ma):
            can_buy = True

        while(can_buy or can_sell):
            if(len(self.opened_orders) > 0):
                price_last_order = self.opened_orders[-1].price
                
                # not price up +5%
                if(can_sell and not self.price_compare(price_last_order,price_act,5)): 
                    can_sell = False
                
                # not price down -10% or limit maximum orders
                if(not self.price_compare(price_last_order,price_act,-10) 
                    or len(self.opened_orders) == self.max_open_orders):
                    can_buy = False
            else:
                can_sell = False

            if(can_sell):
                self.sell(date)
            if(can_buy):
                self.buy(date)

    def start_bot(self, date = None):
        if(date is None):
            date = self.get_lower_date()
        start_date = date
        max_date = self.get_upper_date()
        while date <= max_date:
            price = self.get_close_price_at_date(date)
            if(self.verify_sl_and_tp(price)):
                self.close_bot_at_price(date, price)
                break
            
            self.operate(date)

            date += datetime.timedelta(days = 1)

        # price = self.get_close_price_at_date(date - datetime.timedelta(days = 1))
        # self.close_bot_at_price(date,price)
        self.print_summary(start_date, max_date)
