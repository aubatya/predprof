import requests
import json


def get_data():
    url = "https://dt.miet.ru/ppo_it_final"
    headers = {"X-Auth-Token": "bjbpldgt"}

    response = requests.request("GET", url, headers=headers)
    text = response.text
    data = json.loads(text)["message"]

    ans = []

    for item in data:
        anoms = [item["id"]]
        anoms += list(map(int, item["coords"]))
        for anom in item["swans"]:
            anoms.append([anom["id"], float(anom["rate"])])
        ans.append(anoms)

    return ans


def get_center(h1, h2, h3):
    x1, y1 = h1
    x2, y2 = h2
    x3, y3 = h3

    a = x1 ** 2 - x2 ** 2
    b = y2 ** 2 - y1 ** 2
    e = y2 - y1
    g = x1 - x2
    c = x1 ** 2 - x3 ** 2
    d = y3 ** 2 - y1 ** 2
    f = y3 - y1
    h = x1 - x3

    y0 = (2 * g * (c - d) - 2 * h * (a - b)) / (4 * (h * e - g * f))
    x0 = (a - b + 2 * y0 * e) / (2 * g)

    return x0, y0
