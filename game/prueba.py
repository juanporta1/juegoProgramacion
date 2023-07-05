lineas = open("ranking.txt", "r")
lineas = lineas.readlines()

rank = []
for linea in lineas:
    linea = linea.split(",")
    linea[2].strip()
    rank.append(linea)
rank.sort(key=lambda x: float(x[2]),reverse=True)

print(rank)

lineas.close()

