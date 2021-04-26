import yfinance as yf
from sklearn.linear_model import LinearRegression
from matplotlib import pyplot as plt
import seaborn as sns
import numpy as np

class indexLinReg:
    def __init__(self):
        # Graph Plot Settings
        sns.set_theme()
        plt.rcParams['xtick.bottom'] = False
        plt.rcParams['xtick.labelbottom'] = False

        # Initialise the tickers
        self.snp = yf.Ticker("^GSPC")
        self.ftse = yf.Ticker("^FTSE")

        # Data Process
        self._get_data()
        self._linear_regress()
        self._volatility()

    def _get_data(self):
        # Get last one year's data
        self.snp_data = self.snp.history(period='3mo', interval='1d')
        self.ftse_data = self.ftse.history(period='3mo', interval='1d')
        self.snp_data = self.snp_data.reset_index()
        self.ftse_data = self.ftse_data.reset_index()
        # print("Successfully fetched the data!")

    def _linear_regress(self):
        # Reshape the date values
        self.snp_date_val = self.snp_data.index.values.reshape(-1, 1)
        self.ftse_date_val = self.ftse_data.index.values.reshape(-1, 1)

        # Fit straight line through the data points
        self.snp_reg = LinearRegression().fit(self.snp_date_val, self.snp_data['Close'])
        self.ftse_reg = LinearRegression().fit(self.ftse_date_val, self.ftse_data['Close'])
        # print("Regression model generated!")

        # Add data points
        self.snp_data['LinReg'] = self.snp_reg.predict(self.snp_date_val)
        self.ftse_data['LinReg'] = self.ftse_reg.predict(self.ftse_date_val)

    def _volatility(self):
        # Get deviation of the data points from the model
        self.snp_data['dev'] = abs(self.snp_data['LinReg'] - self.snp_data['Close'])
        self.ftse_data['dev'] = abs(self.ftse_data['LinReg'] - self.ftse_data['Close'])


    def show(self):
        fig, axs = plt.subplots(2)
        
        axs[0].plot(self.snp_data.index, self.snp_data['Close'])
        axs[0].plot(self.snp_data.index, self.snp_data['LinReg'])
        axs[0].plot(self.snp_data.index, self.snp_data['LinReg'] + 2 * self.snp_data['dev'].std(), '--')
        axs[0].plot(self.snp_data.index, self.snp_data['LinReg'] - 2 * self.snp_data['dev'].std(), '--')
        snp_accuracy = round(self.snp_reg.score(self.snp_date_val, self.snp_data['Close']), 3)
        axs[0].set_title(f"S&P500 R^2 = {snp_accuracy}")

        axs[1].plot(self.ftse_data.index, self.ftse_data['Close'])
        axs[1].plot(self.ftse_data.index, self.ftse_data['LinReg'])
        axs[1].plot(self.ftse_data.index, self.ftse_data['LinReg'] + 2 * self.ftse_data['dev'].std(), '--')
        axs[1].plot(self.ftse_data.index, self.ftse_data['LinReg'] - 2 * self.ftse_data['dev'].std(), '--')
        ftse_accuracy = round(self.ftse_reg.score(self.ftse_date_val, self.ftse_data['Close']), 3)
        axs[1].set_title(f"FTSE100 R^2 = {ftse_accuracy}")

        plt.show()

    def tomorrow(self):
        # Predict tomorrow's data using the model
        snp_pred = self.snp_reg.predict(np.array([len(self.snp_data) + 1]).reshape(-1, 1))[0]
        ftse_pred = self.ftse_reg.predict(np.array([len(self.ftse_data) + 1]).reshape(-1, 1))[0]

        print(f"Sell S&P 500 at : {snp_pred + 2 * self.snp_data['dev'].std():.1f}")
        print(f"Buy S&P 500 at : {snp_pred - 2 * self.snp_data['dev'].std():.1f}\n")

        print(f"Sell FTSE 100 at : {ftse_pred + 2 * self.ftse_data['dev'].std():.1f}")
        print(f"Buy FTSE 100 at : {ftse_pred - 2 * self.ftse_data['dev'].std():.1f}")

if __name__ == "__main__":
    linreg = indexLinReg()
    linreg.tomorrow()
    linreg.show()