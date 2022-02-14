from .portfolio import Portfolio
import numpy as np
import scipy.optimize as sco

class PortfolioSharpeRatio(Portfolio):
    def __init__(self, date, assets_array):
        super().__init__(date, assets_array)

    # User defined Sharpe ratio function
    # Negative sign to compute the negative value of Sharpe ratio
    def sharpe_fun(self, weights):
      return - (self.portfolio_returns(weights) / self.portfolio_sd(weights))

    def max_sharpe_ratio_portfolio(self):
        # We use an anonymous lambda function
        constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})

        # This creates asset_len tuples of (0, 1), all of which exist within a container tuple
        # We essentially create a sequence of (min, max) pairs
        bounds = tuple((0, 1) for _ in range(len(self.assets_array)))

        # Repeat the list with the value (1 / asset_len) asset_len times, and convert list to array
        equal_weights = np.array([1 / len(self.assets_array)] * len(self.assets_array))

        # Minimization results
        max_sharpe_results = sco.minimize(
          # Objective function
          fun = self.sharpe_fun,
          # Initial guess, which is the equal weight array
          x0 = equal_weights,
          method = 'SLSQP',
          bounds = bounds,
          constraints = constraints
        )

        # Extract the weight composition array
        return max_sharpe_results["x"]

    def run(self):
        low_date = self.get_lower_date()
        self.create_new_df(low_date)

        max_sharpe_ratio_vector = self.max_sharpe_ratio_portfolio()
        return max_sharpe_ratio_vector

