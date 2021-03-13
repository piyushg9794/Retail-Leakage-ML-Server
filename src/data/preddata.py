import datetime
import pandas as pd
import numpy as np

class PredData:

    total_districts = 20

    def __init__(self, months, mean_bplpop=1700000, mean_literacy=.73, var_bplpop=7000, var_literacy=0.07):

        self.months = months
        self.mean_bplpop = mean_bplpop
        self.mean_literacy = mean_literacy
        self.var_bplpop = var_bplpop
        self.var_literacy = var_literacy

    def Generate_dist(self, dis):


        dist = np.array([dis]*self.months)
        bplpop = np.random.normal(self.mean_bplpop, self.var_bplpop, self.months)
        literacy = np.random.normal(self.mean_literacy, self.var_literacy, self.months)
        fertland = np.random.randint(1600, 3600, self.months)
        crisis = np.random.randint(0, 2, self.months)

        today = datetime.date.today()
        start = datetime.date(today.year, today.month+2, 1) - datetime.timedelta(days=1)
        month= np.array([i for i in range (today.month+1, today.month+self.months+1)])

        data = {
                'Dist': dist,
                'Month': month,
                'BPLPop': bplpop,
                'fertileLand': fertland,
                'Crisis': crisis,
                'Literacy': literacy
                }


        df = pd.DataFrame(data=data, index=pd.date_range(start, freq="M", periods=len(data['Dist'])))
        return df

    def Generate(self):

        df = self.Generate_dist(1)
        for i in range(2, PredData.total_districts+1):
            temp_df= self.Generate_dist(i)
            df= df.append(temp_df)

        return df

data1 = PredData(3, 500000, 500)
df = data1.Generate()