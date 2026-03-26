# import pandas as pd

# track_df = pd.read_csv('grp3-Container-Tracking/data/luzern-horw.csv', header=None, names=["timestamp", "latitude", "longitude", "temperature", "humidity"], index_col="timestamp")

# print(track_df['temperature'].median())

import requests

url = 'https://fl-17-240.zhdk.cloud.switch.ch/'

response_container = requests.get(f"{url}containers")

if response_container.status_code == 200:
    data_container = response_container.json()

    print("Verfügbare Container:")
    print("--------------------")
    containers = data_container.get("containers", [])

    for container in containers:
        print(container)

    chosen_container = input("Wähle einen Container aus: ")

    if chosen_container in containers:
        print(f"\nContainer '{chosen_container}' gewählt.")
        response_route = requests.get(f"{url}containers/{chosen_container}/routes")

        if response_route.status_code == 200:
            data_route = response_route.json()
            print(data_route)
            listed_routes = data_route["routes"]

            print("\nVerfügbare Routen:")
            print("--------------------")
            for route in listed_routes:
                print(route)

            chosen_route = input("Wähle eine Route aus: ")
            
            routes = data_route.get("routes", [])

            for route in routes:
                print(route)

            if chosen_route in listed_routes:
                print("True")
            else:
                print("Bitte wähle eine Route aus dem Menü aus.")
        else:
            print("Fehler beim Abrufen der Routen:", response_route.status_code)

    else:
        print("Bitte wähle einen Container aus dem Menü aus.")

else:
    print("Fehler beim Abrufen der Container: ", response_container.status_code)
