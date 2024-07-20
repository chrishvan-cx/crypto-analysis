# !! ALL RESULT = 0 MEANING LOST, IGNORE IT !!#

import pandas as pd
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

he_so = 1 # If price too small, need to multiply with he_so to correct the "i" loop below
ETH = 3500 * he_so

# Load the dataset
data = pd.read_csv('data/ETH_15M.csv')
unit_price = round(ETH / 200) # 0.5% of current price
min_probability = 55 # input accept win rate %
num_candle = 3 # input number of candle same color
scale_price = list(range(unit_price, unit_price * 10, unit_price))

# Add a 'color' column to indicate the color of the candle
data['color'] = data.apply(lambda row: 'green' if row['close'] > row['open'] else 'red', axis=1)

# Initialize variables
max_total_series_3 = 0
max_color_change_count = 0
max_no_color_change_count = 0
max_percentage = 0
max_diff_price = 0
max_win = 0
max_balance = 0

# Iterate over each price in the price list
for diff_price in scale_price:
    total_series_3 = 0
    color_change_count = 0
    no_color_change_count = 0
    total_appear = 0
    percentage = 0
    win = 0
    usdt = 0
   

    # Iterate through the DataFrame to find sequences of three consecutive candles of the same color
    for i in range(1, len(data) - 3):
        candle_1 = i
        candle_2 = i + 1
        candle_3 = i + 2
        candle_4 = i + 3
        # 3 cây cùng màu + cây bắt đầu và cây trước đó phải khác màu
        if data['color'][candle_1] == data['color'][candle_2] == data['color'][candle_3] and data['color'][i] != data['color'][i-1]:           
            
            total_series_3 += 1
            price_3col = abs(data['close'][candle_3] - data['close'][candle_1]) * he_so
            if price_3col > diff_price:
                
                candle_4th_vol = abs(data['open'][candle_4] - data['close'][candle_4]) * he_so
                # IF WON
                
                if data['color'][candle_4] != data['color'][candle_1]:
                    color_change_count += 1
                    price_high = (data['high'][candle_4] - data['open'][candle_4]) * he_so
                    price_low = (data['open'][candle_4] - data['low'][candle_4] ) * he_so
                    is_buy = data['color'][i+num_candle-1] == "red"
                    if is_buy:
                        if price_low > unit_price:
                            usdt -= unit_price/2
                        else:
                            usdt += candle_4th_vol
                    else:
                        if price_high > unit_price:
                            usdt -= unit_price/2
                        else:
                            usdt += candle_4th_vol
                # IF LOST
                else:
                    no_color_change_count += 1
                    if candle_4th_vol > price_3col:
                        usdt -= unit_price/2
                    else:
                        usdt -= candle_4th_vol
    
    total_appear = color_change_count + no_color_change_count
    win = color_change_count - no_color_change_count
    # Calculate the probability
    if total_appear > 0:
        probability = color_change_count * 100 / total_appear
    else:
        probability = 0
    # Update the maximum percentage and corresponding values if the current probability is higher
    if win > 0 and probability > min_probability and usdt > max_balance:
        max_win = win
        max_percentage = probability
        max_total_series_3 = total_series_3
        max_color_change_count = color_change_count
        max_no_color_change_count = no_color_change_count
        max_diff_price = diff_price
        max_balance = usdt

# Print the results
print(f'Tổng số lần 3 cây nến cùng màu: ' + Fore.YELLOW + f'{max_total_series_3}')
print(f'Mua với đk tổng giá 3 cột > {max_diff_price / he_so}: ' + Fore.GREEN + f'{max_color_change_count}')
print(f'Bán với đk tổng giá 3 cột > {max_diff_price / he_so}: ' + Fore.RED + f'{max_no_color_change_count}')
print(f'Tỷ lệ lệnh thắng: ' + Fore.YELLOW + f'{max_percentage:.2f}' + '%')
print(f'Kết quả tốt nhất: ' + Fore.YELLOW + f'{max_balance:.2f}'+' USDT' + Style.RESET_ALL)
