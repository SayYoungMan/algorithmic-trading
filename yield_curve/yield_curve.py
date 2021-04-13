import urllib.request
import xml.etree.ElementTree as ET
from matplotlib import pyplot as plt
import seaborn as sns
import requests
import lxml.html as lh
import pandas as pd

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

        # UK Yield Curve Related Parameters
        self.uk_url = 'https://markets.ft.com/data/bonds'
        self.uk_interval_quant = [1/12, 3/12, 6/12, 1, 2, 3, 4, 5, 7, 8, 9, 10, 15, 20, 30]

        
    
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

    def get_uk_data(self):
        response = requests.get(self.uk_url)
        doc = lh.fromstring(response.content)
        tr_elems = doc.xpath('//tr')

        col = []
        i = 0

        for t in tr_elems[0]:
            i += 1
            name = t.text_content()
            col.append((name, []))

        for j in range(1, 16):
            T = tr_elems[j]
            if len(T) != 5:
                raise ValueError("Not valid length of row.")
            i = 0
            for t in T.iterchildren():
                data = t.text_content()
                if i in [1, 3, 4]:
                    data = float(data.rstrip('%'))
                col[i][1].append(data)
                i += 1
            
        df = {title:column for (title, column) in col}
        df = pd.DataFrame(df)

        plt.plot(self.uk_interval_quant, df['Yield'], 'x-')
        plt.plot(self.uk_interval_quant, df['1 week ago'], 'x-')
        plt.plot(self.uk_interval_quant, df['1 month ago'], 'x-')
        plt.xlabel('Time from Today / Years')
        plt.ylabel('Yield Curve Rate / %')
        plt.title('UK Daily Yield Curve Rates')
        plt.legend(['Today', 'Week Ago', 'Month Ago'])
        plt.show()


if __name__ == '__main__':
    ycg = yieldCurveGenerator()
    ycg.get_us_data()
    ycg.get_uk_data()