import yfinance as yf
from sklearn.linear_model import LinearRegression
from matplotlib import pyplot as plt
import seaborn as sns

class indexLinReg:
    def __init__(self):
        # Graph Plot Settings
        sns.set_theme()
        plt.rcParams['xtick.bottom'] = False
        plt.rcParams['xtick.labelbottom'] = False

        # Initialise the tickers
        self.snp = yf.Ticker("^GSPC")
        self.ftse = yf.Ticker("^FTSE")

        self._get_data()
        self._linear_regress()

    def _get_data(self):
        # Get last one year's data
        self.snp_data = self.snp.history(period='3mo', interval='1d')
        self.ftse_data = self.ftse.history(period='3mo', interval='1d')
        self.snp_data = self.snp_data.reset_index()
        self.ftse_data = self.ftse_data.reset_index()
        print("Successfully fetched the data!")

    def _linear_regress(self):
        # Reshape the date values
        self.snp_date_val = self.snp_data.index.values.reshape(-1, 1)
        self.ftse_date_val = self.ftse_data.index.values.reshape(-1, 1)

        # Fit straight line through the data points
        self.snp_reg = LinearRegression().fit(self.snp_date_val, self.snp_data['Close'])
        self.ftse_reg = LinearRegression().fit(self.ftse_date_val, self.ftse_data['Close'])
        print("Regression model generated!")

    def show(self):  
        fig, axs = plt.subplots(2)
        
        axs[0].plot(self.snp_data.index, self.snp_data['Close'])
        axs[0].plot(self.snp_data.index, self.snp_reg.predict(self.snp_date_val))
        snp_accuracy = round(self.snp_reg.score(self.snp_date_val, self.snp_data['Close']), 3)
        axs[0].set_title(f"S&P500 R^2 = {snp_accuracy}")

        axs[1].plot(self.ftse_data.index, self.ftse_data['Close'])
        axs[1].plot(self.ftse_data.index, self.ftse_reg.predict(self.ftse_date_val))
        ftse_accuracy = round(self.ftse_reg.score(self.ftse_date_val, self.ftse_data['Close']), 3)
        axs[1].set_title(f"FTSE100 R^2 = {ftse_accuracy}")

        plt.show()

if __name__ == "__main__":
    linreg = indexLinReg()
    linreg.show()