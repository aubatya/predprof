import requests
import json
from app.backend.models import *


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


def get_3_dets():
    data = get_data()
    anoms = {}
    for det in data:
        for anom in det[3:]:
            if anom[0] in anoms:
                if len(anoms[anom[0]]) < 6:
                    anoms[anom[0]].append(anom[1])
                    anoms[anom[0]].append((det[1], det[2]))
            else:
                anoms[anom[0]] = [anom[1], (det[1], det[2])]
    # print(anoms)
    return [[i[1], i[3], i[5], i[0], i[2], i[4]] for i in list(anoms.values())]


def get_center():
    data = get_3_dets()
    ans = []
    for dat in data:
        h1, h2, h3, i1, i2, i3 = dat
        x1, y1 = h1
        x2, y2 = h2
        x3, y3 = h3

        a = i1 * x1 ** 2 - i2 * x2 ** 2
        b = i2 * y2 ** 2 - i1 * y1 ** 2
        e = i1 * x1 ** 2 - i3 * x3 ** 2
        g = i3 * x3 - i1 * x1
        c = i2 * x2 - i1 * x1
        d = i1 * y1 - i2 * y2
        f = i3 * y3 ** 2 - i1 * y1 ** 2
        h = i1 * y1 - i3 * y3

        y0 = (g * (b - a) + c * (e - f)) / (2 * (c * h - g * d))
        x0 = (b + 2 * y0 * d - a) / (2 * c)

        i0 = i1 * (((x1 - x0) ** 2) + ((y1 - y0) ** 2))
        ans.append([x0, y0, i0])

    return ans


def calc_ints():  # [[x, y, i], ...]
    data = get_center()
    matrix = [[1 for _ in range(40)] for _ in range(30)]
    for row in range(30):
        for col in range(40):
            max_int = 0
            for anom in data:
                x = anom[0]
                y = anom[1]
                i = anom[2]
                r = (row ** 2 - y ** 2) + (col ** 2 - x ** 2)
                if r == 0:
                    intr = r
                else:
                    intr = i / r
                max_int = max(max_int, intr)
            matrix[row][col] = int(max_int <= 2)
    return matrix


def prw(u, p):
    if p[u] != u:
        return [u + 1] + prw(p[u], p)


def dis(mat, start, end):
    d = {}
    k = 1
    l = [[1 for _ in range(1200)] for i in range(1200)]
    for i in range(30):
        for j in range(40):
            d[k] = (i, j)
            if (i, j) == start:
                start = k - 1
            if (i, j) == end:
                end = k - 1
            k += 1
    for i in range(1200):
        for j in range(1200):
            x, y = d[i]
            x1, y1 = d[j]
            if mat[x][y] == 0 or mat[x1][y1] == 0:
                l[i][j] = 0
            elif (abs(x - x1) == 1 and abs(y - y1) == 0) or (abs(x - x1) == 0 and abs(y - y1) == 1):
                l[i][j] = 1
            else:
                l[i][j] = 0
    p = [0] * 1200
    D = [None] * 1200
    p[start] = start
    D[start] = 0
    Q = []
    Q.append(start)
    while Q:
        start = Q.pop(0)
        for v in range(1200):
            if l[start][v]:
                if D[v] is None:
                    D[v] = D[start] + 1
                    Q.append(v)
                    p[v] = start
    path = prw(p[end], p)
    path1 = []
    for i in path:
        path1.append(d[i])
    return path1
