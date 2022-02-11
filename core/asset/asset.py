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
        self.asset_data.dropna(inplace=True)
        self.asset_data.reset_index(inplace=True)
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

    # get the row by date with lower bound
    def get_row_by_date(self, date):
        if(date < self.start_date):
            return 0

        dates = self.asset_data['Date']
        l, r = 0, len(self.asset_data)
        while(l < r):
            mid = (l + r) >> 1
            if(date < dates[mid]):
                r = mid
            else:
                l = mid + 1
        return l - 1

    def get_open_price_by_index(self, index):
        return self.asset_data['Open'][index]

    def get_close_price_by_index(self, index):
        return self.asset_data['Close'][index]

    def get_close_price_by_date(self, date):
        index_row = self.get_row_by_date(date)
        return self.get_close_price_by_index(index_row)

    def get_open_price_by_date(self, date):
        index_row = self.get_row_by_date(date)
        return self.get_open_price_by_index(index_row)

