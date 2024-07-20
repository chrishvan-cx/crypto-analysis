import pandas as pd
import requests


def fetch_mark_price_klines():
    url = 'https://testnet.binancefuture.com/fapi/v1/markPriceKlines'
    params = {
        'symbol': 'BTCUSDT',
        'interval': '15m',
        'limit': 5
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        klines = response.json()
        # Process the klines data as needed
        for kline in klines:
            print(kline)
    else:
        print(f"Error: {response.status_code} - {response.text}")



def check_last_three_candles(csv_file):
    df = pd.read_csv(csv_file)
    # Ensure the DataFrame is sorted by time in ascending order
    df = df.sort_values(by='time')
    last_three_candles = df.tail(3).copy()
    # Calculate if each candle is going up or down
    last_three_candles['direction'] = last_three_candles.apply(lambda row: 'up' if row['close'] > row['open'] else 'down', axis=1)
    all_up = all(last_three_candles['direction'] == 'up')
    all_down = all(last_three_candles['direction'] == 'down')
    
    # Check the additional condition
    open_3rd_candle = last_three_candles.iloc[0]['open']
    close_last_candle = last_three_candles.iloc[2]['close']
    price_difference = abs(close_last_candle - open_3rd_candle) > 300
    
    if all_up:
        if price_difference:
            print("up greater than 300.")
        else:
            print("up not greater than 300.")
    elif all_down:
        if price_difference:
            print("down greater than 300.")
        else:
            print("down not greater than 300.")
    else:
        print("The last three candles are not consistently going in one direction.")


