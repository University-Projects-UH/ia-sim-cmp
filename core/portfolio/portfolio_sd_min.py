from .portfolio import Portfolio
import datetime
import pandas as pd
import numpy as np
import scipy.optimize as sco

class PortfolioSdMin(Portfolio):
    def __init__(self, name, date, assets_array):
        super().__init__(name, date, assets_array)

    def min_sd_portfolio(self):
        # We use an anonymous lambda function
        constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})

        # This creates asset_len tuples of (0, 1), all of which exist within a container tuple
        # We essentially create a sequence of (min, max) pairs
        bounds = tuple((0, 1) for _ in range(len(self.assets_array)))

        # Repeat the list with the value (1 / asset_len) asset_len times, and convert list to array
        equal_weights = np.array([1 / len(self.assets_array)] * len(self.assets_array))

        min_sd_results = sco.minimize(
          # Objective function
          fun = self.portfolio_sd,
          # Initial guess, which is the equal weight array
          x0 = equal_weights,
          method = 'SLSQP',
          bounds = bounds,
          constraints = constraints
        )
        return min_sd_results["x"]

    def run(self):
        low_date = self.get_lower_date()
        self.create_new_df(low_date)

        min_sd_vector = self.min_sd_portfolio()
        return min_sd_vector

