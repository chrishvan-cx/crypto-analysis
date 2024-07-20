import pandas as pd
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# Load the dataset
data = pd.read_csv('BTCUSD_DEMO.csv')
diff_price =400  # Different of 1st candle close price with 3rd candle close price

# Add a 'color' column to indicate the color of the candle
data['color'] = data.apply(lambda row: 'green' if row['close'] > row['open'] else 'red', axis=1)

# Initialize counters
total_series_3 = 0
color_change_count = 0
no_color_change_count = 0
total_appear = 0

# Iterate through the DataFrame to find sequences of three consecutive candles of the same color
for i in range(len(data) - 3):
    if data['color'][i] == data['color'][i+1] == data['color'][i+2]:
        total_series_3 += 1
        if abs(data['close'][i+2] - data['close'][i]) > diff_price:
            if data['color'][i+3] != data['color'][i]:
                color_change_count += 1
            else:
                no_color_change_count += 1

total_appear = color_change_count + no_color_change_count
# Calculate the probability
if total_appear > 0:
    probability = color_change_count * 100 / total_appear
else:
    probability = 0

print(f'Mốc giá thay đổi: ' + Fore.YELLOW + f'{diff_price}')
print(f'Tổng số lần 3 cây nên cùng màu: ' + Fore.YELLOW + f'{total_series_3/3}')
print(f'Số lần nến thứ 4 đổi màu ' + Fore.GREEN + f'{color_change_count}')
print(f'Số lần nến thứ 4 KO đổi màu ' + Fore.RED + f'{no_color_change_count}')
print(f'Tỉ lệ %: ' + Fore.YELLOW + f'{probability:.2f}' + '%'  + Style.RESET_ALL)

# print(f'Total sequences of three consecutive candles of the same color: {total_series_3}')
# print(f'Number of times the fourth candle changed color with close price difference > 1000: {color_change_count}')
# print(f'Number of times the fourth candle did NOT change color with close price difference > 1000: {no_color_change_count}')
# print(f'Probability of the fourth candle changing color: {probability:.2f}')