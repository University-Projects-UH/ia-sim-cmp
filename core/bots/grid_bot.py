from .bot import Bot

class GridBot(Bot):
    # asset_pair: array with two assets
    def __init__(self, name, take_profit, stop_loss, investment, grids, limit_high, limit_low, asset_pair):
        super().__init__(name, take_profit, stop_loss, investment)
        self.grids = grids
        self.limit_low = limit_low
        self.limit_high = limit_high
        self.assetA = asset_pair[0]
        self.assetB = asset_pair[1]
        self.start_date, self.end_date = self.format_assets_data()
        self.assetA_data = self.filter_by_date(self.assetA.asset_data)
        self.assetB_data = self.filter_by_date(self.assetB.asset_data)

    def filter_by_date(self, data):
        new_data = data.loc[data['Date'] >= self.start_date]
        return new_data.loc[data['Date'] <= self.end_date]
        

    def print_bot_info(self):
        super().print_bot_info()
        print("Pair: " + "/".join([self.assetA.name, self.assetB.name]))
        print("Limit low: " + str(self.limit_low))
        print("Limit high: " + str(self.limit_high))
        print("Start Date: " + str(self.start_date))
        print("End Date: " + str(self.end_date))

        self.print_operation_history()

    # date format: YYYY-MM-DD
    # method for get the common range of data
    def format_assets_data(self):
        start_date = max(self.assetA.start_date, self.assetB.start_date)
        end_date = min(self.assetA.end_date, self.assetB.end_date)
        
        assert start_date <= end_date, "There is not a common range between the assets"
        return start_date, end_date

