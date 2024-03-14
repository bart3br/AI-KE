import pandas as pd
import csv
import datetime

col_types = {
    'id':int,
    'company': str,
    'line': str,
    'departure_time': str,
    'arrival_time': str,
    'start_stop': str,
    'end_stop': str,
    'start_stop_lat': float,
    'start_stop_lon': float,
    'end_stop_lat': float,
    'end_stop_lon': float
    }

data = pd.read_csv("connection_graph.csv", dtype=col_types)
#data1 = csv.reader('connection_graph.csv')
data.rename(columns={data.columns[0]: "id"}, inplace=True)
#print(data.columns)
#print(data.head(10))

for type in data.dtypes:
    print(type)
    
# data = data.astype(col_types, errors='ignore')
# for type in data.dtypes:
#     print(type)
    
print(data.head(10))




#df = pd.DataFrame(data)
#df.head(10)
#df.dtypes
