import pandas as pd
import datetime

class Asset:
    # asset_data contains:
    # Open: open price
    # High: high price
    # Low: low price
    # Close: close price
    # Date: data date
    def __init__(self, name, path_file, data_frame = None):
        self.name = name
        self.asset_data = pd.read_csv(path_file) if data_frame is None else data_frame
        self.format_date()
        self.start_date = self.asset_data['Date'][0]
        self.end_date = self.asset_data['Date'][len(self.asset_data.index) - 1]

    def parse_date(self, date):
        if(type(date) is not str):
            return date
        dateA = [int(c) for c in date.split("-")]
        return datetime.datetime(dateA[0], dateA[1], dateA[2])

    def format_date(self):
        self.asset_data['Date'] = self.asset_data['Date'].apply(self.parse_date)

    def get_day_prices(self, pos):
        day_prices = [self.asset_data['Open'][pos], self.asset_data['Low'][pos],
                      self.asset_data['High'][pos], self.asset_data['Close'][pos]]
        # the price dropped
        if(day_prices[0] > day_prices[-1]):
            day_prices[1], day_prices[2] = day_prices[2], day_prices[1]

        return day_prices

    def get_open_price(self, pos):
        return self.asset_data['Open'][pos]

    def get_close_price(self, pos):
        return self.asset_data['Close'][pos]

