import yfinance as yf
from sklearn.linear_model import LinearRegression
from matplotlib import pyplot as plt
import seaborn as sns
import numpy as np

class indexLinReg:
    def __init__(self, ticker, period='3mo', interval='1d'):
        # Graph Plot Settings
        sns.set_theme()
        plt.rcParams['xtick.bottom'] = False
        plt.rcParams['xtick.labelbottom'] = False

        # Take in the settings
        self.period = period
        self.interval = interval

        # Initialise the tickers
        self.name = ticker
        self.ticker = yf.Ticker(ticker)

        # Data Process
        self._get_data()
        self._linear_regress()
        self._volatility()

    def _get_data(self):
        # Get the recent data
        self.data = self.ticker.history(period=self.period, interval=self.interval)
        self.data = self.data.reset_index()

    def _linear_regress(self):
        # Reshape the date values
        self.date_val = self.data.index.values.reshape(-1, 1)

        # Fit straight line through the data points
        self.reg = LinearRegression().fit(self.date_val, self.data['Close'])

        # Add data points
        self.data['LinReg'] = self.reg.predict(self.date_val)

    def _volatility(self):
        # Get deviation of the data points from the model
        self.data['dev'] = abs(self.data['LinReg'] - self.data['Close'])

    def show(self):
        plt.plot(self.data.index, self.data['Close'])
        plt.plot(self.data.index, self.data['LinReg'])
        plt.plot(self.data.index, self.data['LinReg'] + 2 * self.data['dev'].std(), '--')
        plt.plot(self.data.index, self.data['LinReg'] - 2 * self.data['dev'].std(), '--')
        self.accuracy = round(self.reg.score(self.date_val, self.data['Close']), 3)
        plt.title(f"{self.name} R^2 = {self.accuracy}")

        plt.show()

    def tomorrow(self):
        # Predict tomorrow's data using the model
        pred = self.reg.predict(np.array([len(self.data) + 1]).reshape(-1, 1))[0]

        print(f"Sell {self.name} at : {pred + 2 * self.data['dev'].std():.1f}")
        print(f"Buy {self.name} at : {pred - 2 * self.data['dev'].std():.1f}\n")

if __name__ == "__main__":
    linreg = indexLinReg("^FTSE")
    linreg.tomorrow()
    linreg.show()