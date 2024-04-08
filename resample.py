import pandas as pd
from tqdm import tqdm
import argparse

def create_dollar_bars(df, dollar_threshold):
    cumulative_sum = 0
    bars = []
    temp_data = []

    for index, row in tqdm(df.iterrows(), total=df.shape[0]):
        temp_data.append(row)
        cumulative_sum += row['quote_av']
        
        # resample
        if cumulative_sum >= dollar_threshold:
            open_time = temp_data[0]['timestamp']
            open_price = temp_data[0]['open']
            high_price = max([x['high'] for x in temp_data])
            low_price = min([x['low'] for x in temp_data])
            close_price = temp_data[-1]['close']

            new_bar = {
                'open_time': open_time,
                'open': open_price,
                'high': high_price,
                'low': low_price,
                'close': close_price,
                'volume': sum([x['volume'] for x in temp_data]),
                'quote_av': cumulative_sum
            }

            bars.append(new_bar)

            cumulative_sum = 0
            temp_data = []

    resample_bars = pd.DataFrame(bars)
    return resample_bars

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--ticker', type=str, default="ETHUSDT")
    parser.add_argument('--threshold', type=int, default=10000000)

    args = parser.parse_args()
    coin = args.ticker
    threshold = args.threshold

    file_path = f'./data/{coin}_1m.csv'
    data = pd.read_csv(file_path)

    resample_bars = create_dollar_bars(data, threshold)

    output_file_path = f'./resample/{coin}_vol_{threshold}.csv'
    resample_bars.to_csv(output_file_path, index=False)
    
