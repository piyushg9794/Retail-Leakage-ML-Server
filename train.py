import pickle
from data import Data
from model import pipe

# dev
data1 = Data(2, 500000, 500)
df = data1.Generate()
y_train= df['Demand']
x_train= df.drop(columns='Demand')

# prod
# fetch data from sql


pipe.fit(x_train, y_train)
pickle.dump(pipe, open('final_model.sav', 'wb'))