import pickle

# fetch data from sql table-2
input_data = []

loaded_pipe = pickle.load(open('final_model.sav', 'rb'))
pred = loaded_pipe.predict(input_data)