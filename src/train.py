from getdb import Db
import pickle
from data.data import Data
import pandas as pd
from model import pipe


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
    for i,j in zip(range(columns_cnt), x):
        d[i].append(j)

data = {}
ind = d[0]
for i in range(columns_cnt-1):
    data[columns[i+1]] = d[i+1]

df = pd.DataFrame(data=data, index=ind)
y_train= df['Demand']
x_train= df.drop(columns='Demand')

print(x_train.head())
print(y_train.head())
pipe.fit(x_train, y_train)
pickle.dump(pipe, open('final_model.sav', 'wb'))