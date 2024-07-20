import pandas as pd
import requests
import schedule
import time

def main_script():
    fetch_mark_price_klines()

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
        check_last_three_candles(klines)
    else:
        print(f"Error: {response.status_code} - {response.text}")

def check_last_three_candles(data):
    # Define column names
    columns = ['time', 'open', 'high', 'low', 'close']
    
    # Create a DataFrame from the provided data
    df = pd.DataFrame(data, columns=columns + ['extra']*7).iloc[:, :5]
    
    # Convert the relevant columns to numeric types
    df['open'] = pd.to_numeric(df['open'])
    df['high'] = pd.to_numeric(df['high'])
    df['low'] = pd.to_numeric(df['low'])
    df['close'] = pd.to_numeric(df['close'])

    # Ensure the DataFrame is sorted by time in ascending order
    df = df.sort_values(by='time')
    print(df)
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


main_script()
# Schedule the function to run every 15 minutes
schedule.every(2).seconds.do(main_script)

print("Script is running, press Ctrl+C to stop.")
# Keep the script running
while True:
    schedule.run_pending()
    time.sleep(1)