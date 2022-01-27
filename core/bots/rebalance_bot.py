from .bot import Bot
from .order import Order
import datetime
import functools
EPS = 0.0000001

class RebalanceBot(Bot):
    # stop lost and take profit by ratio
    # for example if the bot has stop lost of 15% and
    # the loss on usdt reach to that percent, the bot will
    # be closet, analogously for take profit
    def __init__(self, name, stop_loss, take_profit, investment, assets_array, rebalance_ratio=0.2, percent_array=None):
        super().__init__(name, stop_loss, take_profit, investment)
        assert rebalance_ratio >= 0, "Rebalance value has to be at least equal to zero"
        assert len(assets_array) >= 2, "Rebalance bot require at least two assets"
        self.assets_array = assets_array
        self.rebalance_ratio = rebalance_ratio
        self.assets_count = len(self.assets_array)
        self.percent_array = percent_array
        if(percent_array is None):
            self.percent_array = [1.0 / self.assets_count] * self.assets_count

    def print_bot_info(self):
        print("Assets: " + " | ".join(map(lambda asset: asset.name, self.assets_array)))
        print("Rebalance ratio: " + str(self.rebalance_ratio))
        super().print_bot_info()

    # given a date returns the value of the asset calculated with
    # the volumen of orders and the price at that date
    def get_asset_value(self, asset_index, date):
        price_at_date = self.assets_array[asset_index].get_close_price_by_date(date)
        value = 0
        for order in self.investment_by_asset[asset_index]:
            value += order.volumen * price_at_date
        return value

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

    # total_value is the value of the bot on usd at today
    def asset_sell_percent(self, asset_index, percent, total_value, date):
        orders_array = self.investment_by_asset[asset_index]
        price_at_date = self.assets_array[asset_index].get_close_price_by_date(date)
        asset_name = self.assets_array[asset_index].name
        while(len(orders_array) > 0 and percent > EPS):
            order = orders_array[-1]
            order_value = price_at_date * order.volumen
            order_percent = order_value / total_value
            # order_percent is the percent relation between the order and the total value
            if(order_percent <= percent):
                self.append_order_to_history(Order(date, price_at_date, order.volumen, asset_name, "sell"))
                orders_array.pop()
                percent -= order_percent
            else:
                subtract_volumen = (percent * total_value) / price_at_date
                self.append_order_to_history(Order(date, price_at_date, subtract_volumen, asset_name, "sell"))
                orders_array[-1].volumen -= subtract_volumen
                percent = 0

    def asset_buy_percent(self, asset_index, percent, date):
        asset_name = self.assets_array[asset_index].name
        total_volumen = functools.reduce(lambda acc, order: acc + order.volumen, \
                                         self.investment_by_asset[asset_index], 0)
        price_at_date = self.assets_array[asset_index].get_close_price_by_date(date)
        buy_order = Order(date, price_at_date, total_volumen * percent, asset_name)
        self.investment_by_asset[asset_index].append(buy_order)
        self.append_order_to_history(buy_order)

    def rebalance_assets(self, assets_percent, total_value, date):
        do_not_rebalance = True
        for i in range(self.assets_count):
            ratio_condition = abs(assets_percent[i]) < self.percent_array[i]
            do_not_rebalance = do_not_rebalance and ratio_condition

        if(do_not_rebalance):
            return
        for i in range(self.assets_count):
            if(assets_percent[i] > 0):
                self.asset_sell_percent(i, assets_percent[i], total_value, date)
            else:
                self.asset_buy_percent(i, assets_percent[i] * -1, date)

    def start_bot(self, date = None):
        if(date is None):
            date = self.get_lower_date()
        self.investment_by_asset = []
        for asset in self.assets_array:
            price_at_date = asset.get_close_price_by_date(date)
            volumen = (self.investment / self.assets_count) / price_at_date
            initial_order = Order(date, price_at_date, volumen, asset.name)
            self.append_order_to_history(initial_order)
            self.investment_by_asset.append([initial_order])

        max_date = self.get_upper_date()
        while(date <= max_date):
            assets_values = [self.get_asset_value(i, date) for i in range(len(self.investment_by_asset))]
            total_profit = (sum(assets_values) - self.investment) / 100
            #check take profit and stop loss
            if(total_profit >= self.take_profit):
                break
            if(total_profit <= self.stop_loss):
                break

            total_value = sum(assets_values)
            assets_percent = []
            for i in range(self.assets_count):
                percent = (assets_values[i] / total_value) - self.percent_array[i]
                assets_percent.append(percent)

            self.rebalance_assets(assets_percent, sum(assets_values), date)

            date += datetime.timedelta(days = 1)
