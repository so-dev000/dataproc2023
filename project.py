import json
import os
from typing import Final

import plotly.graph_objects as go
import requests
from dotenv import load_dotenv
from requests import Response

load_dotenv()
MAP_BOX_ACCESS_TOKEN: Final = os.getenv("MAP_BOX_ACCESS_TOKEN")
HOT_PEPPER_API_KEY: Final = os.getenv("HOT_PEPPER_API_KEY")
API_URL: Final = "http://webservice.recruit.co.jp/hotpepper/gourmet/v1/"


def fetch_data(keyword: str) -> dict:
    params: dict = {
        "key": HOT_PEPPER_API_KEY,
        "keyword": keyword,
        "format": "json",
        "count": 100,
    }
    request: Response = requests.get(API_URL, params=params)
    result: dict = json.loads(request.content)["results"]
    results_available: int = result["results_available"]
    results_start: int = result["results_start"]
    shop: dict = result["shop"]

    start: int = results_start
    while start <= results_available:
        print(str(results_start) + "/" + str(results_available))
        start += 100
        params["start"] = start
        request: Response = requests.get(API_URL, params=params)
        result: dict = json.loads(request.content)["results"]
        results_start: int = result["results_start"]
        shop += result["shop"]
    print("done")
    return shop


data: dict = fetch_data("お好み焼き")
lat: list[int] = []
lng = []
for i in data:
    lat.append(i["lat"])
    lng.append(i["lng"])


figure = go.Figure(
    go.Scattermapbox(
        lat=lat,
        lon=lng,
        mode="markers",
        marker=go.scattermapbox.Marker(size=9),
    )
)

figure.update_layout(
    autosize=True,
    hovermode="closest",
    mapbox=dict(
        accesstoken=MAP_BOX_ACCESS_TOKEN,
        center=dict(lat=38.5, lon=137.5),
        zoom=3,
        pitch=0,
        bearing=0,
    ),
)
figure.show()
