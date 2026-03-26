# import pandas as pd

# track_df = pd.read_csv('grp3-Container-Tracking/data/luzern-horw.csv', header=None, names=["timestamp", "latitude", "longitude", "temperature", "humidity"], index_col="timestamp")

# print(track_df['temperature'].median())

import requests

container_id = "gpr3"

route_id = "luzern-horw"

url = 'https://fl-17-240.zhdk.cloud.switch.ch/'

response_container = requests.get(f"{url}containers")

if response_container.status_code == 200:
    data_container = response_container.json()
    # print(data)
    listed_containers = data_container["containers"]

    print("\nAuswahl Container-Tracking:\n------------------")
    for container in listed_containers:
        print(container)

    chosen_container = input("Wähle einen Container aus: ")

    if chosen_container in listed_containers:
        print("True")
    else:
        print("Bitte wähle einen Container aus dem Menü aus.")

else:
    print("Fehler: ", response_container.status_code)

response_route = requests.get(f"{url}containers/{chosen_container}/routes")

if response_route.status_code == 200:
    data_route = response_route.json()
    print(data_route)
    listed_routes = data_route["routes"]

    print("\nAuswahl Route des Containers:\n------------------")
    for route in listed_routes:
        print(route)

    chosen_route = input("Wähle eine Route aus: ")

    if chosen_route in listed_routes:
        print("True")
    else:
        print("Bitte wähle eine Route aus dem Menü aus.")

else:
    print("Fehler: ", response_route.status_code)