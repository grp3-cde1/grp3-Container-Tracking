# import pandas as pd

# track_df = pd.read_csv('grp3-Container-Tracking/data/luzern-horw.csv', header=None, names=["timestamp", "latitude", "longitude", "temperature", "humidity"], index_col="timestamp")

# print(track_df['temperature'].median())

import requests

container_id = "gpr3"

route_id = "luzern-horw"

url = 'https://fl-17-240.zhdk.cloud.switch.ch/'

response = requests.get(f"{url}containers")

if response.status_code == 200:
    data = response.json()
    print(data)
    print(data["containers"])

else:
    print("Fehler: ", response.status_code)