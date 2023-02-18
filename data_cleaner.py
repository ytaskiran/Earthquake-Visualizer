import pandas as pd
import requests
from urllib.parse import urlparse
from urllib.parse import parse_qs

TWEETS = "data/kandilli_tweets2.csv"

def getLatLon(url):
    print(url)
    org_url = requests.head(url).headers['location']
    parsed_url = urlparse(org_url)
    captured_value = parse_qs(parsed_url.query)['q'][0].split(",")
    lat = captured_value[0]
    lon = captured_value[1]

    return lat, lon

def cleanData(raw_df):
    earthquakes_text = list(raw_df["text"])
    earthquakes_text = earthquakes_text[:787]
    
    return earthquakes_text

def preprocess(earthquakes_text):
    location = []
    latitude = []
    longitude = []
    magnitude = []
    depth = []
    day = []
    hour = []
    minute = []
    sec = []

    for e in earthquakes_text:
        lines = e.split("\n")
        print(lines)
        try:
            loc = lines[1].split(" ")
        except Exception as e:
            print(lines)
            continue
        if len(loc) == 3:
            url = loc[2]
            loc = " ".join(loc[:2])
        elif len(loc) == 2:
            url = loc[1]
            loc = loc[0]
        else:
            print(loc)
            continue
        lat, lon = getLatLon(url)
        if "," in lines[3]:
            mag = lines[3][-4:-1]
            print(mag)
        else:
            mag = lines[3][-3:]
        dep = lines[4][-7:]
        d = lines[2][:2]
        h = lines[2][-12:-10]
        m = lines[2][-9:-7]
        s = lines[2][-6:-4]

        location.append(loc)
        latitude.append(lat)
        longitude.append(lon)
        magnitude.append(mag)
        depth.append(dep)
        day.append(d)
        hour.append(h)
        minute.append(m)
        sec.append(s)
    
    df = pd.DataFrame(
    {'location': location,
     'latitude': latitude,
     'longitude': longitude,
     'magnitude': magnitude,
     'depth': depth,
     'day': day,
     'hour': hour,
     'minute': minute,
     'sec': sec,
    })

    return df

def main():
    raw_df = pd.read_csv(TWEETS)
    earthquakes_text = cleanData(raw_df)
    earthquakes_df = preprocess(earthquakes_text)

    earthquakes_df.to_csv("data/earthquakes2.csv", index=False)


if __name__ == "__main__":
    main()