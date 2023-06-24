import keyboard,os
from pynput import keyboard
from colorama import Fore,Style,Back
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
                display += Fore.MAGENTA + "# "
            elif y == 2:
                display += Fore.GREEN + "X "
            elif y == 4:
                display += Fore.RED + "@ "
            elif y == 0:
                display += "  "
        display += "\n"
    print(display)

def getPlayerPosition(maps):
    for x in maps:
        for y in x:
            if y == 4:
                return (lab.index(x), x.index(y))
def movePlayer(key):
    os.system("cls")
    inLab,inList = getPlayerPosition(lab)
    
    if hasattr(key, "char") == False:
        print()
    elif key.char == "w" and lab[inLab - 1][inList] != 1 and lab[inLab - 1][inList] != 2:
        lab[inLab][inList] = 0
        lab[inLab - 1][inList] = 4
    elif key.char == "w" and lab[inLab - 1][inList] == 2:
        lab[inLab][inList] = 0
        lab[inLab - 1][inList] = 4
        listener.stop()
        print("Felicidades, has pasado el nivel, presion c para continuar")
    
    if hasattr(key, "char") == False:
        print()    
    elif key.char == "s" and lab[inLab + 1][inList] != 1 and lab[inLab + 1][inList] != 2:
        lab[inLab][inList] = 0
        lab[inLab + 1][inList] = 4
    elif key.char == "s" and lab[inLab + 1][inList] == 2:
        lab[inLab][inList] = 0
        lab[inLab + 1][inList] = 4
        listener.stop()
        print("Felicidades, has pasado el nivel, presion c para continuar")
        
    if hasattr(key, "char") == False:
        print()    
    elif key.char == "a" and lab[inLab][inList - 1] != 1 and lab[inLab][inList - 1] != 2:
        lab[inLab][inList] = 0
        lab[inLab][inList - 1] = 4
    elif key.char == "a" and lab[inLab][inList - 1] == 2:
        lab[inLab][inList] = 0
        lab[inLab][inList - 1] = 4
        listener.stop()
        print("Felicidades, has pasado el nivel, presion c para continuar")
    
    if hasattr(key, "char") == False:
        print()   
    elif key.char == "d" and lab[inLab][inList + 1] != 1 and lab[inLab][inList + 1] != 2:
        lab[inLab][inList] = 0
        lab[inLab][inList + 1] = 4
    elif key.char == "d" and lab[inLab][inList + 1] == 2:
        lab[inLab][inList] = 0
        lab[inLab][inList + 1] = 4
        listener.stop()
        print("Felicidades, has pasado el nivel, presion c para continuar")

    draw(lab)
    
def juego(key):
    print(key)
    movePlayer(key)
draw(lab)
g = 1

listener = keyboard.Listener(on_press=movePlayer)
listener.start()
listener.join()

