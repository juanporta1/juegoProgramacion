import pygame as py
py.init()

window = py.display.set_mode((1280,720))
tamCuadrado = 80

colorPared = (128,0,0)
colorJuagdor = (50,150,175)
colorSalida = (0,128,0)

def obtenerMapa(laberinto):
    muros = []
    mapa = []
    x = 0
    y = 0
    for fila in laberinto:
        for valor in fila:
            if valor == 1:
                pared = py.draw.rect(window,colorPared,(x,y,tamCuadrado,tamCuadrado))
                mapa.append(pared)
                muros.append(pared)
            elif valor == 2:
                salida = py.draw.rect(window,colorSalida,(x,y,tamCuadrado,tamCuadrado))
                mapa.append(salida)
            elif valor == 4:
                jugador = py.draw.rect(window,colorJuagdor,(x,y,tamCuadrado,tamCuadrado))
                playerX = x
                playerY = y
                valor = 0
                
            x += tamCuadrado
            y += tamCuadrado
                
    return mapa, muros, jugador, playerX, playerY


    
               


lab = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,2,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,4,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
]






while True:
    window.fill((0,0,0))
    for event in py.event.get():
        if event.type == py.QUIT:
            py.quit()
    obtenerMapa(lab)
    
           
            
    py.display.update()
    py.time.Clock()
    
