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

print(*get_data(), sep="\n")
