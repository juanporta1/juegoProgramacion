import keyboard,os
import time
lab = [
    
        [1,1,1,1,1,1,1,1,1,1],
        [1,2,0,0,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,0,0,1],
        [1,0,0,0,0,1,0,0,0,1],
        [1,0,0,0,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,0,4,1],
        [1,1,1,1,1,1,1,1,1,1]    
]   
    

def draw(maps):
    display = ""
    for x in maps:
        
        for y in x:
            if y == 1:
                display += "# "
            elif y == 2:
                display += "X "
            elif y == 4:
                display += "@ "
            elif y == 0:
                display += "  "
        display += "\n"
    print(display)

def getPlayerPosition(maps):
    for x in maps:
        for y in x:
            if y == 4:
                return (lab.index(x), x.index(y))
def movePlayer():
    os.system("cls")
    inLab,inList = getPlayerPosition(lab)
    
    if keyboard.is_pressed("w") and lab[inLab - 1][inList] != 1 and lab[inLab - 1][inList] != 2:
        lab[inLab][inList] = 0
        lab[inLab - 1][inList] = 4
    elif keyboard.is_pressed("w") and lab[inLab - 1][inList] == 2:
        lab[inLab][inList] = 0
        lab[inLab - 1][inList] = 4
        print("Felicidades, has pasado el nivel, presion c para continuar")
        
    if keyboard.is_pressed("s") and lab[inLab + 1][inList] != 1 and lab[inLab + 1][inList] != 2:
        lab[inLab][inList] = 0
        lab[inLab + 1][inList] = 4
    elif keyboard.is_pressed("s") and lab[inLab + 1][inList] == 2:
        lab[inLab][inList] = 0
        lab[inLab + 1][inList] = 4
        print("Felicidades, has pasado el nivel, presion c para continuar")
        
    if keyboard.is_pressed("a") and lab[inLab][inList - 1] != 1 and lab[inLab][inList - 1] != 2:
        lab[inLab][inList] = 0
        lab[inLab][inList - 1] = 4
    elif keyboard.is_pressed("a") and lab[inLab][inList - 1] == 2:
        lab[inLab][inList] = 0
        lab[inLab][inList - 1] = 4
        print("Felicidades, has pasado el nivel, presion c para continuar")
        
    if keyboard.is_pressed("d") and lab[inLab][inList + 1] != 1 and lab[inLab][inList + 1] != 2:
        lab[inLab][inList] = 0
        lab[inLab][inList + 1] = 4
    elif keyboard.is_pressed("d") and lab[inLab][inList + 1] == 2:
        lab[inLab][inList] = 0
        lab[inLab][inList + 1] = 4
        print("Felicidades, has pasado el nivel, presion c para continuar")

    draw(lab)
    
def juego():
    movePlayer()
    
while True:
    juego()