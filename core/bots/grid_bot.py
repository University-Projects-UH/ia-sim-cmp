from .bot import Bot
from .order import Order
import datetime

class GridBot(Bot):
    # asset_pair: array with two assets
    # assetA / assetB
    # the investment represents the quantity of assetB
    # limit_low and limit_high delimit the bot work range
    def __init__(self, name, stop_loss, take_profit, investment, grids, limit_low, limit_high, assets_array):
        super().__init__(name, take_profit, stop_loss, investment, assets_array)
        assert stop_loss < limit_low, "Stop loss must be less than limit low"
        assert take_profit > limit_high, "Take profit must be greater than limit high"
        assert len(assets_array) == 2 or len(assets_array) == 1, "grid bot works with one or two assets"
        self.grids_count = grids
        self.grids_orders = [None] * grids
        self.limit_low = limit_low
        self.limit_high = limit_high
        self.grid_len = (limit_high - limit_low) / grids
        self.investment_per_grid = investment / grids
        self.profit_per_grid = self.investment_per_grid * self.grid_len
        self.profit = 0

    def print_bot_info(self):
        super().print_bot_info()
        print("Pair: " + " | ".join(self.assets_array))
        print("Limit low: " + str(self.limit_low))
        print("Limit high: " + str(self.limit_high))

        self.print_operation_history()

    def get_floor_grid(self, price):
        if(price < self.limit_low):
            return None
        diff = price - self.limit_low
        return int(diff // self.grid_len)

    def get_ceil_grid(self, price):
        if(price > self.limit_high):
            return None
        diff = (price + self.grid_len) - self.limit_low
        return int(diff // self.grid_len)

    # get how many assets B are needed to buy 1 assetA at a date
    def get_price_at_date(self, date):
        assetA_price = self.assets_array[0].get_close_price_by_date(date)
        if(len(self.assets_array) == 1):
            return assetA_price
        assetB_price = self.assets_array[1].get_close_price_by_date(date)
        return assetA_price / assetB_price

    def initialize_bot(self, date):
        price = self.get_price_at_date(date)
        start_grid = self.get_ceil_grid(price) + 1
        while (start_grid < len(self.grids_orders)):
            asset_name = self.assets_array[0].name
            assetA_volumen = self.investment_per_grid / price
            order = Order(date, price, assetA_volumen, asset_name)
            self.append_order_to_history(order)
            self.grids_orders[start_grid] = order
            start_grid += 1

    # check stop loss and take profit
    def verify_sl_and_tp(self, price):
        if(price >= self.take_profit):
            self.close_bot_at_price(self.take_profit)
        elif(price <= self.stop_loss):
            self.close_bot_at_price(self.stop_loss)
        return price <= self.stop_loss or price >= self.take_profit

    def get_price_at_grid(self, grid):
        return self.limit_low + (self.grid_len * grid)

    def up_transition(self, last_price, price, date):
        low_grid = self.get_ceil_grid(last_price)
        high_grid = self.get_floor_grid(price)
        while(low_grid <= high_grid):
            if(self.grids_orders[low_grid] != None):
                price = self.get_price_at_grid(low_grid)
                order_opened = self.grids_orders[low_grid]
                self.profit += (price - order_opened.price) * order_opened.volumen
                sell_order = Order(date, price, order_opened.volumen, order_opened.name, "sell")
                self.append_order_to_history(sell_order)
            self.grids_orders[low_grid] = None
            low_grid += 1

    def down_transition(self, last_price, price, date):
        high_grid = self.get_floor_grid(last_price)
        low_grid = self.get_ceil_grid(price)
        asset_name = self.assets_array[0].name
        while(high_grid >= low_grid):
            price = self.get_price_at_grid(high_grid)
            # the price fall, open buy order
            volumen = self.investment_per_grid / price
            buy_order = Order(date, price, volumen, asset_name)
            self.append_order_to_history(buy_order)

            # open sell order behind the current grid if exist
            if(high_grid + 1 < self.grids_count):
                self.grids_orders[high_grid + 1] = buy_order
            high_grid -= 1

    def price_transition(self, last_price, price, date):
        if(last_price <= price):
            self.up_transition(last_price, price, date)
        else:
            self.down_transition(last_price, price, date)

    def close_bot_at_price(self, price):
        for i in range(self.grids_count):
            order_opened = self.grids_orders[i]
            if(order_opened is None):
                pass
            grid_price = self.get_price_at_grid(i)
            self.profit += (grid_price - order_opened.price) * order_opened.volumen


    def print_summary(self, start_date, max_date):
        #self.print_operation_history()
        print("Start date: " + str(start_date))
        print("End date: " + str(max_date))
        percent_profit = (self.profit * 100) / self.investment
        print("Profit: " + str(self.profit) + " | " + str(percent_profit) + "%")

    def start_bot(self, date = None):
        if(date is None):
            date = self.get_lower_date()
        self.initialize_bot(date)
        start_date = date
        max_date = self.get_upper_date()
        last_price = self.get_price_at_date(date)
        date += datetime.timedelta(days = 1)
        while date <= max_date:
            price_at_date = self.get_price_at_date(date)
            if(self.verify_sl_and_tp(price_at_date)):
                break

            self.price_transition(last_price, price_at_date, date)
            last_price = price_at_date

            date += datetime.timedelta(days = 1)

        self.close_bot_at_price(last_price)
        self.print_summary(start_date, max_date)

