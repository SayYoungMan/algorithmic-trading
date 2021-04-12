import urllib.request
import xml.etree.ElementTree as ET
from matplotlib import pyplot as plt
import seaborn as sns

class yieldCurveGenerator:
    def __init__(self):
        # Graph Plot Settings
        sns.set_theme()

        # US Yield Curve Related Parameters
        self.us_url = 'https://data.treasury.gov/feed.svc/DailyTreasuryYieldCurveRateData?$filter=month(NEW_DATE)%20eq%204%20and%20year(NEW_DATE)%20eq%202021'
        self.us_interval_name = [
            'BC_1MONTH', 'BC_2MONTH', 'BC_3MONTH', 'BC_6MONTH',
            'BC_1YEAR', 'BC_2YEAR', 'BC_3YEAR', 'BC_5YEAR', 'BC_7YEAR', 'BC_10YEAR', 'BC_20YEAR', 'BC_30YEAR'
            ]
        self.us_interval_quant = [1/12, 2/12, 3/12, 6/12, 1, 2, 3, 5, 7, 10, 20, 30]
        
    
    def get_us_data(self):
        response = urllib.request.urlopen(self.us_url)
        df = ET.parse(response)
        root = df.getroot()[-1]
        us_yield = []
        for interval in self.us_interval_name:
            data = root.find('.//{http://schemas.microsoft.com/ado/2007/08/dataservices}' + interval)
            us_yield.append(data.text)
        plt.plot(self.us_interval_quant, us_yield, 'x-')
        plt.xlabel('Time from Today / Years')
        plt.ylabel('Yield Curve Rate / %')
        plt.title('US Daily Treasury Yield Curve Rates')
        plt.show()


if __name__ == '__main__':
    ycg = yieldCurveGenerator()
    ycg.get_us_data()