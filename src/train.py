import pickle
from data.data import Data
import pandas as pd
from model import pipe
from getdb import Db

# dev
data1 = Data(2, 500000, 500)
df = data1.Generate()

# prod

db = Db()
cursor = db.connect(True)

query = ("SELECT * FROM data")
cursor.execute(query)

db.disconnect()


columns = cursor.column_names
columns_cnt = len(columns)
d = [[] for _ in range(columns_cnt)]

for x in cursor:
    temp =[]
    for i,j in zip(range(columns_cnt, x)):
        d[i].append(j)

data = {}
ind = d[0]
for i in range(columns_cnt):
    data[columns[i]] = d[i+1]

df = pd.DataFrame(data=data, index=ind)
y_train= df['Demand']
x_train= df.drop(columns='Demand')


pipe.fit(x_train, y_train)
pickle.dump(pipe, open('final_model.sav', 'wb'))