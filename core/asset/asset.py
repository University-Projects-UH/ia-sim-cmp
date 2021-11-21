import pandas as pd

class Asset:
    def __init__(self, name, path_file):
        self.name = name
        self.asset_data = pd.read_csv(path_file)
        print(self.asset_data)
        self.start_date = self.asset_data['Date'][0]
        self.end_date = self.asset_data['Date'][len(self.asset_data.index) - 1]

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

    def convert_to_usd(self, volumen, position = None):
        if position is None:
            position = len(self.asset_data.index) - 1
        assert(position > 0 and position < len(self.asset_data.index))

        return volumen * self.asset_data['Close'][position]


btc = Asset("BTC", "BTC-USD.csv")
print(btc.get_simple_MA())
print(btc.convert_to_usd(1))
