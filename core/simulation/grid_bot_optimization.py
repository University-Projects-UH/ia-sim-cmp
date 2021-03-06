from core import GridBot
import datetime
import random
from math import inf

def get_asset_bounds(assets):

    max_value = -inf
    min_value = inf

    lower_date = assets[0].start_date
    for asset in assets[1:]:
        low_date = min(low_date, asset.start_date)

    upper_date = assets[0].end_date
    for asset in assets[1:]:
        upper_date = min(upper_date, asset.end_date)

    while lower_date <= upper_date:

        day_value = assets[0].get_close_price_by_date(lower_date)
        max_value = max(max_value, day_value)
        min_value = min(min_value, day_value)

        lower_date += datetime.timedelta(days = 1)

    return min_value, max_value


def bots_variation(bot):

    range = bot.limit_high - bot.limit_low
    v = random.uniform(range / 20, range / 10)

    bot1 = GridBot('high_plus', bot.stop_loss, max(bot.take_profit, bot.limit_high + v + 1), bot.investment, bot.grids_count - 1, bot.limit_low, bot.limit_high + v, bot.assets_array)
    bot2 = GridBot('high_minus', bot.stop_loss, max(bot.take_profit, bot.limit_high), bot.investment, bot.grids_count - 1, bot.limit_low, bot.limit_high - v, bot.assets_array)

    bot3 = GridBot('low_plus', min(bot.stop_loss, bot.limit_low) , bot.take_profit, bot.investment, bot.grids_count - 1, bot.limit_low + v, bot.limit_high, bot.assets_array)
    bot4 = GridBot('low_minus', min(bot.stop_loss, bot.limit_low - v - 1), bot.take_profit, bot.investment, bot.grids_count - 1 , bot.limit_low - v, bot.limit_high, bot.assets_array)

    bot5 = GridBot('grids_augmented', bot.stop_loss, bot.take_profit, bot.investment, bot.grids_count, bot.limit_low, bot.limit_high, bot.assets_array)

    if bot.grids_count - 2 > 0:

        bot6 = GridBot('grids_reduced', bot.stop_loss, bot.take_profit, bot.investment, bot.grids_count - 2, bot.limit_low, bot.limit_high, bot.assets_array)
        return [bot1, bot2, bot3, bot4, bot5, bot6]

    return [bot1, bot2, bot3, bot4, bot5]

def evaluate_bots_variation(bot_list):

    best = None
    profit = -inf

    for bot in bot_list:

         bot.start_bot()

         if bot.profit > profit:

            best = bot
            profit = bot.profit

    return best, profit

def print_bot_configuration(bot):

    print("#######################\n")
    print("BOT CONFIGURATION\n")

    print("profit: " + str(bot.profit))
    print("stop loss: " + str(bot.stop_loss))
    print("take profit: " + str(bot.take_profit))
    print("investment: " + str(bot.investment))
    print("grids: " + str(bot.grids_count - 1))
    print("limit low: " + str(bot.limit_low))
    print("limit high: " + str(bot.limit_high))
    print("assets files:")

    for a in bot.assets_array:
        print("\t" + str(a.name))

    print("\n#######################")

def grid_bot_optimization(assets, investment = 100, exploration_count = 15, explotation_count = 15):

    min_value, max_value = get_asset_bounds(assets)
    mid_value = (max_value + min_value) / 2

    ### Exploration of the metaheuristic

    best_global_profit = -inf
    best_global_bot = None

    for i in range(exploration_count):

        local_min = random.uniform(min_value, mid_value)
        local_max = random.uniform(mid_value, max_value)
        local_grids = random.randint(5,15)

        bot = GridBot('bot', min_value - local_min/2, max_value + local_max/2, investment, local_grids, local_min, local_max, assets)
        bot.start_bot()

        best_local_profit = bot.profit
        best_local_bot = bot

        ### Explotation of the metaheuristic

        for j in range(explotation_count):

            new_bots = bots_variation(best_local_bot)
            best, profit = evaluate_bots_variation(new_bots)
            #print("profit: " + str(profit))

            if profit > best_local_profit:

                best_local_bot = best
                best_local_profit = profit

        #print("\nbest_local_profit: " + str(best_local_profit) + "\n")

        if best_local_profit > best_global_profit:

            best_global_bot = best_local_bot
            best_global_profit = best_local_profit

            #print("\nbest_global_profit: " + str(best_global_profit) + "\n")

    print_bot_configuration(best_global_bot)

    return best_global_bot

