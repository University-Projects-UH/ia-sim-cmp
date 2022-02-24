import numpy as np
from core import RebalanceBot

EPS = 1e-7

class RebalanceBotSimulation:
    def __init__(self, assets_array, rebalance_ratio = 0.4, start_date = None, max_date = None):
        self.assets_array = assets_array
        self.start_date = start_date
        self.max_date = max_date
        self.rebalance_ratio = rebalance_ratio

    def get_random_portfolios(self, assets_len, count = 300):
        portfolios = []
        for _ in range(count):
            weights = np.random.random(size = assets_len)
            weights /= np.sum(weights)
            portfolios.append(weights)

        return portfolios

    def get_random_rebalance_ratios(self, rebalance_ratio, neighborhood = 0.2, count = 1):
        lower_bound = max(0.01, rebalance_ratio - neighborhood)
        upper_bound = min(0.95, rebalance_ratio + neighborhood)
        rebalance_ratios = [rebalance_ratio]
        while(len(rebalance_ratios) < count):
            rebalance_ratios.append(np.random.uniform(low=lower_bound, high=upper_bound))

        return rebalance_ratios

    def run_bot(self, assets_array, portfolio, rebalance_ratio):
        rebalance_bot = RebalanceBot("", -1000, 1000, 100, assets_array, rebalance_ratio, portfolio)
        return rebalance_bot.start_bot(date=self.start_date, show_info = False)

    def get_best_rebalance_ratio(self, assets_array, rebalance_ratio):
        portfolios = self.get_random_portfolios(len(assets_array), 5)
        rebalance_ratios = self.get_random_rebalance_ratios(rebalance_ratio, 0.2, 5)
        profits = []
        for portfolio in portfolios:
            for ratio in rebalance_ratios:
                profit = self.run_bot(self.assets_array, portfolio, ratio)
                profits.append((profit, ratio))

        percent = 0.3
        profits = sorted(profits, reverse=True)
        profits = profits[:max(int(len(profits) * percent), 1)]
        best_freq = 0
        best_ratio = -1
        for _, ratio_a in profits:
            freq = 0
            for _, ratio_b in profits:
                if(abs(ratio_a - ratio_b) < EPS):
                    freq += 1
            if(freq > best_freq):
                best_freq = freq
                best_ratio = ratio_a

        return best_ratio

    def approximate_portfolios(self, portfolio_a, portfolio_b, assets_array, rebalance_ratio):
        profit_a = self.run_bot(assets_array, portfolio_a, rebalance_ratio)
        profit_b = self.run_bot(assets_array, portfolio_b, rebalance_ratio)
        runs = 20
        while(abs(profit_a - profit_b) > 0.01 and runs > 0):
            portfolio_c = (portfolio_a + portfolio_b) / 2.0
            profit_c = self.run_bot(assets_array, portfolio_c, rebalance_ratio)
            if(profit_a > profit_b):
                profit_b = profit_c
                portfolio_b = portfolio_c
            else:
                profit_a = profit_c
                portfolio_a = portfolio_c

            runs -= 1

        return portfolio_a, profit_a

    def get_best_portfolio(self, assets_array, rebalance_ratio):
        COUNT_PORTFOLIOS = 15
        portfolios = self.get_random_portfolios(len(assets_array), COUNT_PORTFOLIOS)
        profits = []
        for i, portfolio in enumerate(portfolios):
            profit = self.run_bot(assets_array, portfolio, rebalance_ratio)
            profits.append((profit, i))

        profits = sorted(profits, reverse=True)[:4]
        for i in range(4):
            profits[i] = (profits[i][0], portfolios[i])

        best_portfolio = None
        best_profit = -100000
        for i, (profit, portfolio_a) in enumerate(profits):
            j = i + 1
            if(profit > best_profit):
                best_profit = profit
                best_portfolio = portfolio_a
            while(j < len(profits)):
                portfolio_b = profits[j][1]
                portfolio_c, profit_c = self.approximate_portfolios(portfolio_a, portfolio_b,\
                                                                     assets_array, rebalance_ratio)
                if(profit_c > best_profit):
                    best_profit = profit_c
                    best_portfolio = portfolio_c
                j += 1

        return best_portfolio, best_profit


    def get_best_rebalance_bot(self):
        best_rebalance_ratio = self.get_best_rebalance_ratio(self.assets_array, self.rebalance_ratio)
        best_portfolio, _ = self.get_best_portfolio(self.assets_array, best_rebalance_ratio)
        return RebalanceBot("BestRebalanceBot", -1000, 1000, 100, self.assets_array, best_rebalance_ratio,\
                            best_portfolio)



