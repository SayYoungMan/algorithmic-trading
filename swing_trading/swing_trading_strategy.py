from numpy.core.defchararray import index
import yfinance as yf
import pandas as pd
import numpy as np
import json
import heapq
from typing import List

def swing(ticker: str, drop_thresh: float, up_thresh: float, budget: int, fee: float) -> int:
    # Initialise variables to measure performance
    profit = 0
    # Heap to maintain the increasing order of prices
    holding_shares = []
    # A list of dicts having {Action, Date, Price, Quantity} and will be transformed to DataFrame
    history = [] 

    # Get the DataFrame with recent 5 years' price data
    data = None
    while data is None:
        try:
            data = yf.Ticker(ticker).history(period="5y")
        except json.decoder.JSONDecodeError:
            print("JSONDecodeError has occured. Trying again...")
            pass
    data = data.reset_index() # Reset the index

    # Iterate from the sixth row to the last
    for i in range (5, len(data.index)): # len(df.index) is faster than df.shape[0] (https://stackoverflow.com/questions/15943769/how-do-i-get-the-row-count-of-a-pandas-dataframe)
    
        # week_high holds the highest 'Close' price from last week
        week_high = data.iloc[i-5:i]['Close'].max()
        
        # Calculate drop from week_high
        drop = (week_high - data.loc[i, 'Low']) / week_high
        
        # Check If have money to buy stock
        if len(holding_shares) <= 3:
            # If the drop is significant (more than drop_thresh), buy the stock
            if drop > drop_thresh:
                price = min(data.loc[i, 'Open'], (1 - drop_thresh) * week_high) # Price of purchase
                quant = budget // price # Quantity of shares bought
                heapq.heappush(holding_shares, (price, quant))
                # Append the history dict
                history.append({
                    "Action": 'Buy',
                    "Date": data.loc[i, 'Date'],
                    "Price": price,
                    "Quantity": quant
                })
                # Pay the fee
                profit -= fee

        # Check if holding any shares to sell
        if holding_shares:
            # If the most expensive stock held is more than the up_thresh, sell
            expensive = heapq.nlargest(1, holding_shares)[0]
            if ((data.loc[i, 'High'] - expensive[0]) / expensive[0]) > up_thresh:
                expensive = heapq.heappop(holding_shares)
                price = max(expensive[0] * (1 + up_thresh), data.loc[i, 'Open'])
                history.append({
                    "Action": 'Sell',
                    "Date": data.loc[i, 'Date'],
                    "Price": price,
                    "Quantity": quant
                })
                # Pay the Fee
                profit -= fee
                # Calculate profit from transaction
                profit += (price - expensive[0])

    # Transform history into DataFrame
    history = pd.DataFrame(history)

    print(f'Profit for {ticker} with strategy (drop_thresh: {drop_thresh}, up_thresh: {up_thresh}) is {profit}')

    # Calculate and return adjusted profit to make fair comparison with others
    growth = data.loc[len(data.index)-1, 'Close'] / data.loc[0, 'Close']
    adj_profit = profit / growth

    # print(f"Due to growth of {growth}, Adjusted profit is {adj_profit}")

    return profit

def find_best_strategy(ticker: str, drop: List[float], up: List[float]):
    if (len(drop) != 2 or len(up) != 2):
        raise TypeError('Please provide down and up in the form [LB, UP].')

    max_profit = 0

    for drop_thresh in np.arange(drop[0], drop[1], 0.001):
        for up_thresh in np.arange(up[0], up[1], 0.001):
            drop_thresh = round(drop_thresh, 4)
            up_thresh = round(up_thresh, 4)

            prof = swing(ticker, drop_thresh, up_thresh, 500, 0)
            if prof > max_profit:
                max_profit = prof
                best = (drop_thresh, up_thresh)

    print(f"Best Strategy for {ticker} is: drop_thresh {best[0]} and up_thresh {best[1]} with profit of {max_profit}")

    return best, max_profit

def DJ_strategy():
    df = []

    # dow_ticker holds a list of ticker strings
    dow_ticker = json.loads(open('./swing_trading/tickers.json').read())["DowJones"]['tickers']

    for tick in dow_ticker:
        best, profit = find_best_strategy(tick, [0.02, 0.05], [0.01, 0.03])
        df.append({
            "Name": tick,
            "Drop": best[0],
            "Up": best[1],
            "Profit": profit
        })

    print(df)
    df = pd.DataFrame(df)
    df.to_csv('./swing_trading/DowJonesResult.csv', index=False)

def get_price_today(df_path: str) -> None:
    try:
        df = pd.read_csv(df_path)
    except FileNotFoundError:
        print("Please check the file path and try again.")
        return
    
    df['Buy'] = ''
    
    for i in range(len(df.index)):
        data = yf.Ticker(df.loc[i, 'Name']).history(period="6d")
        week_high = data['Close'].max()
        df.loc[i, 'Buy'] = week_high * (1 - df.loc[i, 'Drop'])

    print(df)
    return

if __name__ == "__main__":
    # To make a strategy File
    # DJ_strategy()

    # To get the prices
    get_price_today('./swing_trading/DowJonesResult.csv')

    # =================== Error resolving test cases ==================
    # The Adj Profit is NaN for AAPL
    # find_best_strategy('AAPL', [0.03, 0.05], [0.01, 0.03])

    # JSONDecodeError for JNJ
    # find_best_strategy('JNJ', [0.03, 0.05], [0.01, 0.03])