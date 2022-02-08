import datetime
import pandas as pd
import numpy as np

class Portfolio():
    def __init__(self, name, date, assets_array):
        self.name = name
        self.date = date
        self.assets_array = assets_array


    def get_lower_date(self):
        low_date = self.assets_array[0].start_date
        for asset in self.assets_array[1:]:
            low_date = min(low_date, asset.start_date)

        return low_date

    def create_new_df(self, low_date):
        new_df = { }
        for asset in self.assets_array:
            new_df[asset.name] = []
        while(low_date <= self.date):
            for asset in self.assets_array:
                price_at_date = asset.get_close_price_by_date(low_date)
                new_df[asset.name].append(price_at_date)

            low_date += datetime.timedelta(days = 1)

        df = pd.DataFrame(new_df)
        self.daily_returns = df.pct_change()

    # Function for computing portfolio return
    def portfolio_returns(self, weights):
        return (np.sum(self.daily_returns.mean() * weights)) * 253

    # Function for computing standard deviation of portfolio returns
    def portfolio_sd(self, weights):
        return np.sqrt(np.transpose(weights) @ (self.daily_returns.cov() * 253) @ weights)

