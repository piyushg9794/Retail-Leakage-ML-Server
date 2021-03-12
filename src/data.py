import numpy as np
import pandas as pd

class Data:

    total_districts = 20

    def __init__(self, years, mean_bplpop=1700000, mean_demand=500, mean_literacy=.73, var_bplpop=7000, var_demand=10, var_literacy=0.07):

        self.years = years
        self.mean_bplpop = mean_bplpop
        self.mean_demand = mean_demand
        self.mean_literacy = mean_literacy
        self.var_bplpop = var_bplpop
        self.var_demand = var_demand
        self.var_literacy = var_literacy

    def Generate_dist(self, dis):

        index = range(12*self.years*(dis-1)+1,(12*self.years*dis)+1)
        month= np.array([i for i in range(1,13)]*self.years)
        bplpop = np.random.normal(self.mean_bplpop, self.var_bplpop, 12*self.years)
        dist = np.array([dis]*12*self.years)
        demand = np.random.gumbel(self.mean_demand, self.var_demand, 12)
        for i in range(0,self.years-1):
            demand = np.append(demand, [x+np.random.randint(2,6) for x in demand])
        literacy = np.random.normal(self.mean_literacy, self.var_literacy, 12*self.years)
        fertland = np.random.randint(1600, 3600, 12*self.years)
        crisis = np.random.randint(0, 2, 12*self.years)

        data = {
                'Dist': dist,
                'Month': month,
                'BPLPop': bplpop,
                'fertileLand': fertland,
                'Crisis': crisis,
                'Literacy': literacy,
                'Demand': demand
               }

        df = pd.DataFrame(data=data, index=pd.date_range("2019", freq="M", periods=len(data['Demand'])))
        return df

    def Generate(self):

        df = self.Generate_dist(1)
        for i in range(self.years, Data.total_districts+1):
            temp_df= self.Generate_dist(i)
            df= df.append(temp_df)

        return df

