from .bot import Bot

class GridBot(Bot):
    # asset_pair: array with two assets
    # assetA / assetB
    # the investment represents the quantity of assetB
    def __init__(self, name, take_profit, stop_loss, investment, grids, limit_high, limit_low, assetAB):
        super().__init__(name, take_profit, stop_loss, investment)
        self.grids = [None] * grids
        self.limit_low = limit_low
        self.limit_high = limit_high
        self.grid_len = (limit_high - limit_low) / grids
        self.investment_per_grid = investment / grids
        self.assetAB = assetAB
        self.count_rows = len(self.assetAB.asset_data.index)

    def print_bot_info(self):
        super().print_bot_info()
        print("Pair: " + self.assetAB.name)
        print("Limit low: " + str(self.limit_low))
        print("Limit high: " + str(self.limit_high))

        self.print_operation_history()

    def get_floor_grid(self, price):
        if(price < self.limit_low):
            return None
        diff = price - self.limit_low
        return diff / self.grid_len

    def get_ceil_grid(self, price):
        if(price > self.limit_high):
            return None
        diff = (price + self.grid_len) - self.limit_low
        return diff / self.grid_len

    def initialize_bot(self, pos = 0):
        start_grid = self.get_ceil_grid(self.assetAB['Open'][0])
        self.grid_pointer = start_grid
        while (start_grid < len(self.grids)):
            self.grids[start_grid] = True
            start_grid += 1

    def get_day_prices(self, pos):
        day_prices = [self.assetAB['Open'][pos], self.assetAB['Low'][pos],
                      self.assetAB['High'][pos], self.assetAB['Close'][pos]]
        # the price dropped
        if(day_prices[0] > day_prices[-1]):
            day_prices[1], day_prices[2] = day_prices[2], day_prices[1]

        return day_prices

    def start_bot(self, pos = 0):
        self.initialize_bot()
        last_price = self.assetAB['Open'][0]
        while pos < self.count_rows:
            day_prices = self.get_day_prices(pos)
            pos += 1


