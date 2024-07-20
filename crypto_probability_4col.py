import pandas as pd
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# Load the dataset
data = pd.read_csv('BTCUSD_5M.csv')
price = list(range(100, 1600, 100))
min_probability = 60 # input accept win rate
num_candle = 4 # input number of candle same color

# Add a 'color' column to indicate the color of the candle
data['color'] = data.apply(lambda row: 'green' if row['close'] > row['open'] else 'red', axis=1)

# Initialize variables
max_total_series_3 = 0
max_color_change_count = 0
max_no_color_change_count = 0
max_percentage = 0
max_diff_price = 0
max_win = 0

# Iterate over each price in the price list
for diff_price in price:
    total_series_3 = 0
    color_change_count = 0
    no_color_change_count = 0
    total_appear = 0
    percentage = 0
    win = 0

    # Iterate through the DataFrame to find sequences of three consecutive candles of the same color
    for i in range(len(data) - num_candle):
        if data['color'][i] == data['color'][i+1] == data['color'][i+2] == data['color'][i+3]:
            total_series_3 += 1
            if abs(data['close'][i+num_candle-1] - data['close'][i]) > diff_price:
                if data['color'][i+num_candle] != data['color'][i]:
                    color_change_count += 1
                else:
                    no_color_change_count += 1

    total_appear = color_change_count + no_color_change_count
    win = color_change_count - no_color_change_count
    # Calculate the probability
    if total_appear > 0:
        probability = color_change_count * 100 / total_appear
    else:
        probability = 0
    
    # Update the maximum percentage and corresponding values if the current probability is higher
    if win > 0 and probability > min_probability and win > max_win:
        max_win = win
        max_percentage = probability
        max_total_series_3 = total_series_3
        max_color_change_count = color_change_count
        max_no_color_change_count = no_color_change_count
        max_diff_price = diff_price

# Print the results
print(f'Giá thay đổi lớn hơn: ' + Fore.YELLOW + f'{max_diff_price}')
print(f'Tổng số lần 3 cây nến cùng màu: ' + Fore.YELLOW + f'{max_total_series_3}')
print(f'Số lần nến thứ 4 đổi màu: ' + Fore.GREEN + f'{max_color_change_count}')
print(f'Số lần nến thứ 4 KO đổi màu: ' + Fore.RED + f'{max_no_color_change_count}')
print(f'Tỉ lệ %: ' + Fore.YELLOW + f'{max_percentage:.2f}' + '%' + Style.RESET_ALL)
