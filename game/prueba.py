

with open("game/ranking.txt", "r") as lineas:
    lineas = lineas.readlines()

    rank = []
    for linea in lineas:
        linea = linea.split(",")
        rank.append(linea)
        for i,linea in enumerate(rank):
            for j,elem in enumerate(linea):
                rank[i][j] = elem.rstrip()
    
    rank.sort(key=lambda x: float(x[2]),reverse=True)

    print(rank)
print(len("1234\n"))
print(len("1234\n".rstrip()))
