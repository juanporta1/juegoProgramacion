import os,time,pygame,shutil,copy
from pynput import keyboard
from colorama import Fore,Back,Style
from niveles import labs
import math

anchoConsola, altoConsola = shutil.get_terminal_size()
select = 0  
dificultad = 0
nivel = 0
teclaPresionada = True
ultimoRenderizado = time.time()


#Funciones para centrar en la consola
def centrarH(mensaje, bajadas = 0):
    espacios = (anchoConsola - len(mensaje)) // 2
    mensaje = "\n" * bajadas + " "  * espacios + mensaje
    return mensaje

def centrarV(mensaje):
    bajadas = (altoConsola - 1) // 2
    mensaje = "\n" * bajadas  + mensaje
    return mensaje

#Pantalla al iniciar el juego
def pantallaDeInicio(key = "s"):
    os.system("cls")
    mensaje = Fore.CYAN + "PRESIONE ENTER PARA COMENZAR"
    espacios = (anchoConsola - len(mensaje)) // 2
    mensaje = " " * espacios + mensaje
    
    print(centrarV(mensaje))
    if key == keyboard.Key.space or key == keyboard.Key.enter:
            listener.stop()  
            os.system("cls")
            
            
def menu(key = None):
    global select
    os.system("cls")
    
    op1 = "JUGAR HISTORIA"
    op2 = "MULTIJUGADOR"
    op3 = "SALIR"
    
    if hasattr(key, "char") == False:
        g = 1
    elif key.char == "w":
        if select == 0:
            select = 2
        else:
            select -= 1
    elif key.char == "s":
        if select == 2:
            select = 0
        else:
            select += 1
            
    if select == 0:
        op2 = "   " + op2
        op3 = "   " + op3
        op1 = "-> " + op1
    elif select == 1:
        op3 = "   " + op3
        op1 = "   " + op1
        op2 = "-> " + op2
    elif select == 2:
        op1 = "   " + op1
        op2 = "   " + op2
        op3 = "-> " + op3
        
    print(centrarV(centrarH(op1)))
    print(centrarH(op2))
    print(centrarH(op3))
    if key == keyboard.Key.space or key == keyboard.Key.enter:
        listenerMenu.stop()
        
  
def seleccionarDificultad(key = None):
    global dificultad
    os.system("cls")
    print(centrarH(Fore.LIGHTBLUE_EX + "SELECCIONE LA DIFICULTAD", 20))
    op1 =  "PRINCIPIANTE"
    op2 =  "INTERMEDIO"
    op3 =  "EXPERTO"
    
    if hasattr(key, "char") == False:
        g = 1
    elif key.char == "w": 
        if dificultad == 0:
            dificultad = 2
        else:
            dificultad -= 1
    elif key.char == "s":
        if dificultad == 2:
            dificultad = 0
        else:
            dificultad += 1
            
    if dificultad == 0:
        op3 = Fore.CYAN + "   " + op3
        op2 = Fore.CYAN + "   " + op2
        op1 = Fore.CYAN + "-> " + op1
    elif dificultad == 1:
        op1 = Fore.CYAN + "   " + op1
        op2 = Fore.CYAN + "-> " + op2
        op3 = Fore.CYAN + "   " + op3
    elif dificultad == 2:
        op3 = Fore.CYAN + "-> " + op3
        op2 = Fore.CYAN + "   " + op2
        op1 = Fore.CYAN + "   " + op1
    
        
    print(centrarH(op1,2))
    print(centrarH(op2))
    print(centrarH(op3))
    
    if key == keyboard.Key.space or key == keyboard.Key.enter:
        listener.stop()

def draw(maps):
    #? 0 = Espacio Vacio
    #? 1 = Pared
    #? 2 = Meta
    #? 3 = Pozo
    #?
    #? 
    ancho,_ = shutil.get_terminal_size()
    espacios = (ancho - len(maps[0])) // 2
    display = "\n\n\n\n\n\n\n"
    for x in maps:
        linea = ""
        for y in x:
            if y == 1:
                linea += Fore.MAGENTA + "# "
            elif y == 2:
                linea += Fore.GREEN + "X "
            elif y == 5:
                linea += Fore.RED + "@ "
            elif y == 0:
                linea += "  "
        
        espacios = (ancho - len(x))// 2
        linea = " " * math.trunc((espacios / 1.25)) + linea
        display += linea + "\n"
    os.system("cls")
    print(display)
    
def getPlayerPosition(maps):
    for x in maps:
        for y in x:
            if y == 5:
                return (maps.index(x), x.index(y))

def verificarAtributo(key):
    if hasattr(key, "char"):
        return key.char
    else:
        return False

    

def movePlayer(key):
    global teclaPresionada,nivel,dificultad,laberinto
    inLab,inList = getPlayerPosition(laberinto)

    if (key == keyboard.Key.up or verificarAtributo(key) == "w") and laberinto[inLab - 1][inList] == 0 and  teclaPresionada == True:
        laberinto[inLab][inList] = 0
        laberinto[inLab - 1][inList] = 5
        teclaPresionada = False
        
    elif (key == keyboard.Key.up or verificarAtributo(key) == "w") and laberinto[inLab - 1][inList] == 2 and  teclaPresionada == True:
        laberinto[inLab][inList] = 0
        laberinto[inLab - 1][inList] = 5
        teclaPresionada = False
        listenerJuego.stop()
        
    
    if (key == keyboard.Key.down or verificarAtributo(key) == "s") and laberinto[inLab + 1][inList] == 0 and  teclaPresionada == True :
        laberinto[inLab][inList] = 0
        laberinto[inLab + 1][inList] = 5
        teclaPresionada = False
        
    elif (key == keyboard.Key.down or verificarAtributo(key) == "s") and laberinto[inLab + 1][inList] == 2 and  teclaPresionada == True:
        laberinto[inLab][inList] = 0
        laberinto[inLab + 1][inList] = 5
        teclaPresionada = False
        listenerJuego.stop()
        
    if (key == keyboard.Key.left or verificarAtributo(key) == "a") and laberinto[inLab][inList - 1] == 0 and  teclaPresionada == True:
        laberinto[inLab][inList] = 0
        laberinto[inLab][inList - 1] = 5
        teclaPresionada = False
        
        
    elif (key == keyboard.Key.left or verificarAtributo(key) == "a") and laberinto[inLab][inList - 1] == 2 and  teclaPresionada == True:
        laberinto[inLab][inList] = 0
        laberinto[inLab][inList - 1] = 5
        teclaPresionada = False
        listenerJuego.stop()
        
        
    
    if (key == keyboard.Key.right or verificarAtributo(key) == "d") and laberinto[inLab][inList + 1] == 0 and teclaPresionada == True:
        laberinto[inLab][inList] = 0
        laberinto[inLab][inList + 1] = 5
        teclaPresionada = False
        
        teclaPresionada = 2
    elif (key == keyboard.Key.right or verificarAtributo(key) == "d") and laberinto[inLab][inList + 1] == 2 and  teclaPresionada == True:
        laberinto[inLab][inList] = 0
        laberinto[inLab][inList + 1] = 5
        teclaPresionada = False
        listenerJuego.stop()    
    
    draw(laberinto)

def reset(key = None):
    global teclaPresionada
    teclaPresionada = True

def jugarNivel():
    global nivel,listenerJuego,laberinto
    laberinto = copy.deepcopy(labs[dificultad][nivel])
    listenerJuego = keyboard.Listener(on_press=movePlayer, on_release=reset)
    listenerJuego.start()
    listenerJuego.join()
    
    nivel += 1
    
    

    

while True: 
    nivel = 0
    dificultad = 0
    select = 0
    pantallaDeInicio()
    listener = keyboard.Listener(on_press=pantallaDeInicio)
    listener.start()
    listener.join()
    
    menu()
    listenerMenu = keyboard.Listener(on_press=menu)
    listenerMenu.start()
    listenerMenu.join()
    
    if select == 0:
        seleccionarDificultad()
        listener = keyboard.Listener(on_press=seleccionarDificultad) 
        listener.start()
        listener.join()
        
        draw(labs[dificultad][nivel])
        jugarNivel()
        draw(labs[dificultad][nivel])
        jugarNivel()
        draw(labs[dificultad][nivel])
        jugarNivel()  
        
    elif select == 1:
        os.system("cls")
        print(centrarH("Holaaa",6))
        time.sleep(5)
    elif select == 2: 
        os.system("cls")
        print(centrarH("Muchas Gracias Por Jugar",6))
        break