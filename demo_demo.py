import pandas as pd
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# Load the dataset
data = pd.read_csv('BTCUSD_DEMO.csv')
price = list(range(100, 200, 100))
min_probability = 10 # input accept win rate %
num_candle = 3 # input number of candle same color

# Add a 'color' column to indicate the color of the candle
data['color'] = data.apply(lambda row: 'green' if row['close'] > row['open'] else 'red', axis=1)
print(f'data: {data}')

# Initialize variables
max_total_series_3 = 0
max_color_change_count = 0
max_no_color_change_count = 0
max_percentage = 0
max_diff_price = 0
max_win = 0
balance = 0

# Iterate over each price in the price list
for diff_price in price:
    total_series_3 = 0
    color_change_count = 0
    no_color_change_count = 0
    total_appear = 0
    percentage = 0
    win = 0
    usdt = 0
   

    # Iterate through the DataFrame to find sequences of three consecutive candles of the same color
    for i in range(len(data) - 3):
        
        if data['color'][i] == data['color'][i+1] == data['color'][i+2] and i>2 and data['color'][i] != data['color'][i-1]:
            
            total_series_3 += 1
            price_3col = abs(data['close'][i+num_candle-1] - data['close'][i])
            if price_3col > diff_price:
                if data['color'][i+num_candle] != data['color'][i]:
                    color_change_count += 1
                    up_or_down = data['close'][i+num_candle] - data['close'][i+num_candle-1]
                    if up_or_down>=0:
                        if data['close'][i+num_candle-1] - data['low'][i+num_candle] > 150:
                            usdt -= 100
                        else:
                            usdt += up_or_down
                    else:
                        abs_up_or_down = abs(up_or_down)
                        if price_3col > 150 and abs_up_or_down > 100:
                            usdt -= 100
                        else:
                            usdt -= up_or_down
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
    if win >= 0 and probability > min_probability and win >= max_win:
        print(f'data: {color_change_count}')
        max_win = win
        max_percentage = probability
        max_total_series_3 = total_series_3
        max_color_change_count = color_change_count
        max_no_color_change_count = no_color_change_count
        max_diff_price = diff_price
        balance = usdt

# Print the results
print(f'Giá thay đổi lớn hơn: ' + Fore.YELLOW + f'{max_diff_price}')
print(f'Tổng số lần 3 cây nến cùng màu: ' + Fore.YELLOW + f'{max_total_series_3}')
print(f'Số lần nến thứ 4 đổi màu: ' + Fore.GREEN + f'{max_color_change_count}')
print(f'Số lần nến thứ 4 KO đổi màu: ' + Fore.RED + f'{max_no_color_change_count}')
print(f'Tỉ lệ %: ' + Fore.YELLOW + f'{max_percentage:.2f}' + '%')
print(f'balance: ' + Fore.YELLOW + f'{balance:.2f}'+'usdt' + Style.RESET_ALL)
