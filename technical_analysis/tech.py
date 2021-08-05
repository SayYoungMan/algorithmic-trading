import yfinance as yf
import pandas as pd
from pathlib import Path
import datetime

def bollinger(ticker, period):
    # Import Closing Price data for the ticker
    data = yf.Ticker(ticker).history(period='2mo')['Close']

    # Select only "period" number of rows for the series
    data = data.iloc[data.size - period:]
    
    # Calculate SMA and STD for the period defined
    sma = data.mean()
    std = data.std()

    # Calculate upper and lower Bollinger Bands
    upper_bb = sma + std * 2
    lower_bb = sma - std * 2

    # Last price
    last = data.iloc[-1:].values[0]

    return upper_bb, lower_bb, last

def generate_nasdaq():
    # Get Path of the ticker dataset
    root_path = Path(__file__).parent.parent
    nasdaq_path = root_path / 'dataset' / 'nasdaq100_constituents.csv'

    # Read Ticker dataset
    nasdaq_tickers = pd.read_csv(nasdaq_path)['Symbol']

    # Initialise arrays to store buy, sell positions
    buy = []
    sell = []

    # Loop over all the tickers
    for i, v in nasdaq_tickers.iteritems():
        # Get the bollinger bands for each ticker
        try:
            up, low, last = bollinger(v, 25)
        # Catch the case where the ticker is nolonger available
        except IndexError:
            continue
        
        # Append the tuple of data to sell or buy if the last price was out of Bollinger Band
        if last >= up:
            over = ((last - up) / up) * 100
            sell.append((v, last, up, over))
        
        elif last <= low:
            under = ((low - last) / low) * 100
            buy.append((v, last, low, under))
        
    # Transform buy and sell into dataframes
    buy = pd.DataFrame(buy, columns=['Ticker', 'Last Price', 'Lower Bollinger Band', 'Percentage'])
    sell = pd.DataFrame(sell, columns=['Ticker', 'Last Price', 'Upper Bollinger Band', 'Percentage'])

    # Sort values by the percentage
    buy = buy.sort_values('Percentage', ascending=False)
    sell = sell.sort_values('Percentage', ascending=False)

    # Today's date for file naming
    today = datetime.datetime.today().strftime('%Y-%m-%d')

    # Save the dataframe into csv
    buy.to_csv(f'./results/{today} NASDAQ100 Buy List.csv')
    sell.to_csv(f'./results/{today} NASDAQ100 Sell List.csv')

def generate_snp():
    # Get Path of the ticker dataset
    root_path = Path(__file__).parent.parent
    snp_path = root_path / 'dataset' / 'snp500_constituents.csv'

    # Read Ticker dataset
    snp_tickers = pd.read_csv(snp_path)['Symbol']
    
    # Initialise arrays to store buy, sell positions
    buy = []
    sell = []

    # Loop over all the tickers
    for i, v in snp_tickers.iteritems():
        # Get the bollinger bands for each ticker
        try:
            up, low, last = bollinger(v, 25)
        # Catch the case where the ticker is nolonger available
        except IndexError:
            continue
        
        # Append the tuple of data to sell or buy if the last price was out of Bollinger Band
        if last >= up:
            over = ((last - up) / up) * 100
            sell.append((v, last, up, over))
        
        elif last <= low:
            under = ((low - last) / low) * 100
            buy.append((v, last, low, under))
        
    # Transform buy and sell into dataframes
    buy = pd.DataFrame(buy, columns=['Ticker', 'Last Price', 'Lower Bollinger Band', 'Percentage'])
    sell = pd.DataFrame(sell, columns=['Ticker', 'Last Price', 'Upper Bollinger Band', 'Percentage'])

    # Sort values by the percentage
    buy = buy.sort_values('Percentage', ascending=False)
    sell = sell.sort_values('Percentage', ascending=False)

    # Today's date for file naming
    today = datetime.datetime.today().strftime('%Y-%m-%d')

    # Save the dataframe into csv
    buy.to_csv(f'./results/{today} S&P500 Buy List.csv')
    sell.to_csv(f'./results/{today} S&P500 Sell List.csv')

if __name__ == "__main__":
    generate_nasdaq()
    generate_snp()