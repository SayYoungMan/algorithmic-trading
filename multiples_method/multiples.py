import yfinance as yf
from matplotlib import pyplot as plt
import seaborn as sns
import numpy as np

class Multiples:
    def __init__(self) -> None:
        # Graph Plot Settings
        sns.set_theme()
        plt.rcParams['xtick.bottom'] = False
        plt.rcParams['xtick.labelbottom'] = False

    def compare_price(self, tick1, tick2, period='6mo', interval='1d'):
        # Import ticker data
        data1 = yf.Ticker(tick1).history(period=period, interval=interval)
        data2 = yf.Ticker(tick2).history(period=period, interval=interval)

        # Calculation correlation between two trends
        corr = np.corrcoef(data1['Close'], data2['Close'])[0][1]
        print(f'The correlation between {tick1} and {tick2} is {corr}')

        # Calculate ratio between two close values
        ratio = data1['Close'] / data2['Close']

        # Plot ratio
        plt.plot(data1.index, ratio)
        plt.hlines(ratio.mean(), data1.index[0], data1.index[-1], 'r')
        plt.hlines(ratio.mean() + ratio.std()*2, data1.index[0], data1.index[-1], 'black', '--')
        plt.hlines(ratio.mean() - ratio.std()*2, data1.index[0], data1.index[-1], 'black', '--')
        plt.title(f"Correlation of {tick1} and {tick2} = {corr}")
        plt.show()

if __name__ == '__main__':
    mul = Multiples()
    mul.compare_price('AAPL', 'AMZN')

