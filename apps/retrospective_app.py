import pandas as pd

track_df = pd.read_csv('grp3-Container-Tracking/data/luzern-horw.csv', header=None, names=["timestamp", "latitude", "longitude", "temperature", "humidity"], index_col="timestamp")

print(track_df['temperature'].median())