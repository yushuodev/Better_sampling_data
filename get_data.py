import pandas as pd
import finlab_crypto
from datetime import timedelta
import argparse

def download_candlesticks(ticker):
    crawler = finlab_crypto.crawler
    ohlcv = crawler.get_all_binance(symbol=ticker, kline_size='1m')
    
    ohlcv.reset_index(inplace=True)
    ohlcv['Date'] = pd.to_datetime(ohlcv['timestamp']).dt.date

    ohlcv.set_index('Date', inplace=True)
    ohlcv.to_csv(f'./data/{ticker}_1m.csv')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--ticker', type=str, default="BTCUSDT", help="Symbol that will download")

    args = parser.parse_args()
    coin = args.ticker
    download_candlesticks(coin)
