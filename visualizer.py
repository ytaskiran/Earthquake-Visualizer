import folium
import webbrowser
import pandas as pd
import numpy as np
from collections import deque

colors = {"7" : "#c42301",
          "6" : "#d93b2b",
          "5" : "#e85647",
          "4" : "#f37264",
          "3" : "#ff9c91"}

def preprocess(earthquakes_df):
    earthquakes_df = earthquakes_df.iloc[::-1]
    earthquakes_df["depth"] = earthquakes_df["depth"].map(lambda x: x.strip("km") if "km" in x else x)
    earthquakes_df = earthquakes_df.astype({"depth" : np.float64})

    earthquakes = earthquakes_df.to_dict("records")
    earthquakes_q = deque(earthquakes)

    return earthquakes_q

def plotEarthquakes(earthquakes):

    earthquake_map = folium.Map(location=[37.7123, 37.1195], zoom_start=8, tiles="Stamen Terrain")

    for e in earthquakes:
        if e["magnitude"] < 8 and e["magnitude"] >= 7:
            color = colors["7"]
        elif e["magnitude"] < 7 and e["magnitude"] >= 6:
            color = colors["6"]
        elif e["magnitude"] < 6 and e["magnitude"] >= 5:
            color = colors["5"]
        elif e["magnitude"] < 5 and e["magnitude"] >= 4:
            color = colors["4"]
        elif e["magnitude"] < 4 and e["magnitude"] >= 3:
            color = colors["3"]

        weight = (e["magnitude"] / 8)
        info = f'Konum: {e["location"]}<br> Büyüklük: {e["magnitude"]}<br> \
                 Derinlik: {e["depth"]}<br> Tarih: {e["day"]} Şubat 2023 - {e["hour"]}.{e["minute"]}.{e["sec"]}'

        folium.CircleMarker(location=[e["latitude"], e["longitude"]], 
                            color=color, 
                            radius=15*weight, 
                            stroke=False,
                            fill_opacity=weight,
                            popup=info,
                            fill=True).add_to(earthquake_map)

    earthquake_map.save("earthquake_map.html")
    webbrowser.open("earthquake_map.html")
    earthquake_map.render()


def main():
    earthquakes_df = pd.read_csv("data/earthquakes2.csv")
    earthquakes = preprocess(earthquakes_df)
    plotEarthquakes(earthquakes)


if __name__ == "__main__":
    main()