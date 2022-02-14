import pandas as pd
from core import Asset
from datetime import datetime
import datetime as dt

def test_answer():
    data = {
        'Date': ["2022-01-01", "2022-01-02", "2022-01-03", "2022-01-04", "2022-01-06"],
        'Close': [1000, 1400, 1500, 1500, 1500]
    }
    testercoin = Asset(None, pd.DataFrame(data))

    expected_response = [1000, 1000, 1400, 1500, 1500, 1500, 1500, 1500]
    date_start = datetime.strptime("2021-12-31", "%Y-%m-%d")
    date_max = datetime.strptime("2022-01-7", "%Y-%m-%d")
    pos = 0
    while(date_start <= date_max):
        print(date_start)
        close_price_at_date = testercoin.get_close_price_by_date(date_start)
        assert expected_response[pos] == close_price_at_date
        pos += 1
        date_start += dt.timedelta(days = 1)

