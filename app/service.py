def prw(u, p):
    if p[u]!=u:
        return [u+1]+ prw(p[u], p)


def dis(mat, start, end):
    d = {}
    k = 1
    l = [[1 for _ in range(1200)] for i in range(1200)]
    for i in range(30):
        for j in range(40):
            d[k] = (i, j)
            if (i, j) == start:
                start = k-1
            if (i, j ) == end:
                end = k-1
            k+=1
    for i in range(1200):
        for j in range(1200):
            x, y  = d[i]
            x1, y1 = d[j]
            if mat[x][y]==0 or mat[x1][y1]==0:
                l[i][j] = 0
            elif (abs(x-x1)== 1 and abs(y-y1)==0) or (abs(x-x1)== 0 and abs(y-y1)==1):
                l[i][j] = 1
            else:
                l[i][j] = 0
    p = [0]*1200
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

