from .bot import Bot
from .grid_bot import GridBot
import datetime
import random
from math import inf

def get_asset_bounds(assets, lower_date, upper_date):

    max_value = -inf
    min_value = inf

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

def evaluate_bots_variation(bot_list, lower_date, upper_date):

    best = None
    profit = -inf

    for bot in bot_list:
         
         bot.start_bot(date = lower_date, end_date = upper_date)

         if bot.profit > profit:

            best = bot
            profit = bot.profit

    return best, profit

def grid_bot_optimization(assets):

    ### The period of time for run the bot is (upper_date, lower_date)

    upper_date = assets[0].end_date
    for asset in assets[1:]:
        upper_date = min(upper_date, asset.end_date)

    td = datetime.timedelta(100)
    lower_date = upper_date - td

    min_value, max_value = get_asset_bounds(assets, lower_date, upper_date)
    mid_value = (max_value + min_value) / 2

    ### Exploration of the metaheuristic

    best_global_profit = -inf
    best_global_bot = None

    for i in range(15):

        local_min = random.uniform(min_value, mid_value)
        local_max = random.uniform(mid_value, max_value)
        local_grids = random.randint(5,15)

        bot = GridBot('bot', min_value - local_min/2, max_value + local_max/2, 100, local_grids, local_min, local_max, assets)
        bot.start_bot( date = lower_date, end_date = upper_date)

        best_local_profit = bot.profit
        best_local_bot = bot

        ### Explotation of the metaheuristic

        for j in range(10):

            new_bots = bots_variation(best_local_bot)
            best, profit = evaluate_bots_variation(new_bots, lower_date, upper_date)
            #print("profit: " + str(profit))

            if profit > best_local_profit:

                best_local_bot = best
                best_local_profit = profit

        #print("\nbest_local_profit: " + str(best_local_profit) + "\n")
        
        if best_local_profit > best_global_profit:

            best_global_bot = best_local_bot
            best_global_profit = best_local_profit

            #print("\nbest_global_profit: " + str(best_global_profit) + "\n")

    # print("\n\n")
    # print("profit: " + str(best_global_profit))
    # print("grids: " + str(best_global_bot.grids_count - 1))
    # print("high: " + str(best_global_bot.limit_high))
    # print("low: " + str(best_global_bot.limit_low))
    return best_global_bot



            











    