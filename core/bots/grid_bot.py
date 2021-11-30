from .bot import Bot

class GridBot(Bot):
    # asset_pair: array with two assets
    # assetA / assetB
    # the investment represents the quantity of assetB
    def __init__(self, name, stop_loss, take_profit, investment, grids, limit_low, limit_high, assetAB):
        super().__init__(name, take_profit, stop_loss, investment)
        assert stop_loss < limit_low, "Stop loss must be less than limit low"
        assert take_profit > limit_high, "Take profit must be greater than limit low"
        self.grids = [None] * grids
        self.limit_low = limit_low
        self.limit_high = limit_high
        self.grid_len = (limit_high - limit_low) / grids
        self.investment_per_grid = investment / grids
        self.assetAB = assetAB
        self.count_rows = len(self.assetAB.asset_data.index)
        self.profit_per_grid = self.investment_per_grid * self.grid_len
        self.profit = 0

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
        return int(diff // self.grid_len)

    def get_ceil_grid(self, price):
        if(price > self.limit_high):
            return None
        diff = (price + self.grid_len) - self.limit_low
        return int(diff // self.grid_len)

    def initialize_bot(self, pos = 0):
        start_grid = self.get_ceil_grid(self.assetAB.asset_data['Open'][0])
        self.grid_pointer = start_grid
        while (start_grid < len(self.grids)):
            self.grids[start_grid] = True
            start_grid += 1

    def get_day_prices(self, pos):
        day_prices = [self.assetAB.asset_data['Open'][pos], self.assetAB.asset_data['Low'][pos],
                      self.assetAB.asset_data['High'][pos], self.assetAB.asset_data['Close'][pos]]
        # the price dropped
        if(day_prices[0] > day_prices[-1]):
            day_prices[1], day_prices[2] = day_prices[2], day_prices[1]

        return day_prices

    def verify_sl_and_tp(self, last_price):
        if(last_price <= self.stop_loss or last_price >= self.take_profit):
            price = self.limit_low
            for i in range(len(self.grids)):
                if(self.grids[i]):
                    self.profit += self.investment_per_grid * (self.stop_loss - price)
                price += self.grid_len
            return True
        return False


    def start_bot(self, pos = 0):
        self.initialize_bot()
        last_price = self.assetAB.asset_data['Open'][0]
        close_bot = False
        while not close_bot and pos < self.count_rows:
            day_prices = self.get_day_prices(pos)
            for price in day_prices:
                if(price > last_price):
                    floor_grid = self.get_floor_grid(price)
                    while(self.grid_pointer < floor_grid):
                        if(self.grids[self.grid_pointer]):
                            self.profit += self.profit_per_grid
                            self.grids[self.grid_pointer] = False
                        self.grid_pointer += 1
                        self.grids[self.grid_pointer] = True
                else:
                    ceil_grid = self.get_ceil_grid(price)
                    while(self.grid_pointer > ceil_grid):
                        self.grid_pointer -= 1
                        self.grids[self.grid_pointer] = True
                last_price = price
                close_bot = self.verify_sl_and_tp(last_price)
                if(close_bot):
                    break

            pos += 1
        print(self.profit)

