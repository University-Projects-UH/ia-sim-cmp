import pandas as pd
from .asset import Asset
from .bots import Bot, GridBot, SmartBot, RebalanceBot

def filter_by_date(data, start_date, end_date):
    new_data = data.loc[data['Date'] >= start_date]
    return new_data.loc[data['Date'] <= end_date]

# date format: YYYY-MM-DD
# method for get the common range of data
def format_assets_data(assetA, assetB):
    start_date = max(assetA.start_date, assetB.start_date)
    end_date = min(assetA.end_date, assetB.end_date)

    assert start_date <= end_date, "There is not a common range between the assets"
    return start_date, end_date

def apply_division_arrays(arr1, arr2):
    assert len(arr1) == len(arr2), "Not equal length"
    return [arr1[i] / arr2[i] for i in range(len(arr1))]

# we have:
# assetA / usd
# assetB / usd
# then => assetA / assetB
def build_AB_assets_combination(assetA, assetB):
    start_date, end_date = format_assets_data(assetA, assetB)
    assetA.asset_data = filter_by_date(assetA.asset_data, start_date, end_date)
    assetB.asset_data = filter_by_date(assetB.asset_data, start_date, end_date)
    min_len = min(len(assetA.asset_data.index), len(assetB.asset_data.index))
    assetA.asset_data = assetA.asset_data.iloc[:min_len,:]
    assetB.asset_data = assetB.asset_data.iloc[:min_len,:]
    assetA.asset_data.reset_index(drop=True, inplace=True)
    assetB.asset_data.reset_index(drop=True, inplace=True)

    open_priceAB = apply_division_arrays(assetA.asset_data['Open'], assetB.asset_data['Open'])
    close_priceAB = apply_division_arrays(assetA.asset_data['Close'], assetB.asset_data['Close'])
    low_priceAB = apply_division_arrays(assetA.asset_data['Low'], assetB.asset_data['Low'])
    high_priceAB = apply_division_arrays(assetA.asset_data['High'], assetB.asset_data['High'])
    df_AB = pd.DataFrame({ 'Date': assetA.asset_data['Date'], 'Open': open_priceAB, 'Close': close_priceAB, 'Low': low_priceAB, 'High': high_priceAB })
    print(df_AB)
    return Asset(assetA.name + "/" + assetB.name, None, df_AB)
