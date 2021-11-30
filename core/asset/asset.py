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

