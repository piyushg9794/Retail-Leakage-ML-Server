import pickle
from data.preddata import PredData
import json
from getdb import Db



data1 = PredData(3, 500000, 500)
input_data = data1.Generate()

loaded_pipe = pickle.load(open('final_model.sav', 'rb'))
pred = loaded_pipe.predict(input_data)

add_prediction = ("INSERT INTO result "
               "(Dist, State, Month, Demand) "
               "VALUES (%s, %s, %s, %s)")
prediction_data = []

with open('src/meta/state_map.json') as f:
    data = json.load(f)

for i in range(len(input_data)):

    state = data[str(input_data['Dist'][i])]
    d = (int(input_data['Dist'][i]), state, input_data.index[i].date(), pred[i])
    prediction_data.append(d)

db = Db()
cursor = Db.connect()
cursor.executemany(add_prediction, prediction_data)
db.disconnect()