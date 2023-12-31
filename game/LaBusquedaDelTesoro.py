import os
os.system('for /F %i in (requerimientos.txt) do pip install %i')
import os,time,pygame,shutil,copy
from pynput import keyboard
from colorama import Fore,Back,Style,init
from niveles import labs
import math,random
import re

init()
pygame.mixer.init()

anchoConsola, altoConsola = shutil.get_terminal_size()
select = 0  
dificultad = 0
nivel = 0
c = 0
teclaPresionada = True
ultimoRenderizado = time.time()
display = ""
teclaPresionada1 = True
teclaPresionada2 = True
volverAlMenu = False
pausa = 2

#? SFX

escribir1 = pygame.mixer.Sound("sonidos/maquinas/escribir1.wav")
escribir2 = pygame.mixer.Sound("sonidos/maquinas/escribir2.wav")
escribir3 = pygame.mixer.Sound("sonidos/maquinas/escribir3.wav")
finalescribir = pygame.mixer.Sound("sonidos/maquinas/finalescribir.wav")

escribirSFX = [escribir1, escribir2, escribir3]

#Funciones para centrar en la consola
def centrar(mensaje, bajadas = 1):
    c = 0
    for i in mensaje:
        if i == "\n":
            c += 1
    expresionesRegulares = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    aux = expresionesRegulares.sub('', mensaje)
        
       
    if c != 0 and bajadas == 1:
        espacios = (anchoConsola - len(aux)) // 2
        bajadas = (altoConsola - c) // 2
        mensaje = "\n" * bajadas + " " * espacios + mensaje 
        
    elif bajadas == 2:
        espacios = (anchoConsola - len(aux)) // 2
        bajadas = (altoConsola - 1) // 2
        mensaje = "\n" * bajadas + " " * espacios + mensaje 
        
    else:
        espacios = (anchoConsola - len(aux)) // 2
        mensaje = " " * espacios + mensaje 
    if mensaje != None:
        return mensaje
  



def presion(key):
    if key == keyboard.Key.delete or key == keyboard.Key.ctrl_l or key == keyboard.Key.alt_l or key == keyboard.Key.shift or key == keyboard.Key.alt_r or key == keyboard.Key.alt_gr or key == keyboard.Key.ctrl_r or key == keyboard.Key.shift_l or key == keyboard.Key.shift_r:
        return True
    else:
        return False
      
def creadorDeMenues(ops):
    
    selector = 0
    def seleccion(key = None):
        nonlocal selector
        c = 0
        clon = []
        for op in ops:
            clon.append(op)
        
        mayop = len(max(ops, key=len))    
        for i,op in enumerate(clon):
            espacios = mayop - len(op)
            clon[i] = op + " " * espacios
            
        
        if key == keyboard.Key.up or verificarAtributo(key) == "w":
            if selector == 0:
                selector = len(clon) - 1
            else:
                selector -= 1
            escribir3.play()
        if key == keyboard.Key.down or verificarAtributo(key) == "s":
            if selector == len(clon) - 1:
                selector = 0
            else:
                selector += 1
            escribir2.play()
        if key == keyboard.Key.enter:
            escribir1.play()  
            listener.stop()
            input()
            
            
        os.system("cls")
        display = centrar(Fore.CYAN + "SELECCIONE UNA OPCION",3)
        display += "\n\n"
        for op in clon:
            if op != clon[selector]:
                display += centrar(Fore.CYAN + "   " + op,0) + "\n"
            else:
                display += centrar(Fore.CYAN + "-> " + clon[selector],0) + "\n"
        
        
        display += "\n\n" + centrar("PRESIONE ENTER PARA SELECCIONAR",3)
        print(centrar(display))
    
    
    seleccion()
    listener = keyboard.Listener(on_press=seleccion)
    listener.start()
    listener.join()
    
    
    os.system("cls")
    return selector
def dibujarLinea(array):
    linea = ""
    for y in array:
            if y == 1:
                linea += Fore.MAGENTA + "# "
            elif y == 2:
                linea += Fore.GREEN + "X "
            elif y == 5:
                linea += Fore.RED + "@ "
            elif y == 0 or y == 3:
                linea += "  "
            elif y == 4:
                linea += Fore.BLUE + "O "
    return linea


def dibujarLaberinto(maps):
    #? 0 = Espacio Vacio
    #? 1 = Pared
    #? 2 = Meta
    #? 3 = Pozo Que No Se Ve
    #? 4 = Pozo Que Se Ve
    #? 5 = Jugador
    global ancho
    ancho,_ = shutil.get_terminal_size()
    display = ""
    for x in maps:
        linea = centrar(dibujarLinea(x),0)
        display += linea + "\n"
    os.system("cls")
    display += "\n\n" + centrar(Fore.LIGHTCYAN_EX + "W/↑:ARRIBA  S/↓:ABAJO  A/←:IZQUIERDA  D/→:DERECHA",3)
    print(centrar(display))
    
    
    
def dibujarMultijugador(clon1,clon2):
    global anchoConsola
    display = ""
    for i,x in enumerate(clon1):
        linea = centrar(dibujarLinea(x) + "            " + dibujarLinea(clon2[i]),0)
        display += linea + "\n"
    
    os.system("cls")
    display += "\n\n\n" +  Fore.LIGHTCYAN_EX + centrar("W/↑:ARRIBA  S/↓:ABAJO  A/←:IZQUIERDA  D/→:DERECHA",3)
    print(centrar(display))
    




def resetMulti(key):
    global teclaPresionada1,teclaPresionada2
    teclaPresionada1 = True
    teclaPresionada2 = True
    
def topJugadores(ranking):
    os.system("cls")
    ranking = ranking.readlines()
    for linea in ranking:
        linea.strip()

    rank = []
    for linea in ranking:
        linea = linea.split(",")
        rank.append(linea.copy())
        for i,linea in enumerate(rank):
            for j,elem in enumerate(linea):
                rank[i][j] = elem.rstrip()
    
    rank.sort(key=lambda x: float(x[2]))
    rank = rank[:10]
    clon = []
    nombreMasLargo = 0
    annoMasLargo = 0
    puntosMasLargo = 0
    c = 0
    for lista in rank:
        clon.append(lista.copy())

    for lista in clon:
        if c == 0 or nombreMasLargo < len(lista[0]):
            nombreMasLargo = len(lista[0])
            c += 1
    nombreMasLargo += 2
    c = 0
    for lista in clon:
        if c == 0 or annoMasLargo < len(lista[1]):
            annoMasLargo = len(lista[1])
            c += 1
    annoMasLargo += 4
    c = 0
    for lista in clon:
        if c == 0 or puntosMasLargo < len(str(lista[2])):
            puntosMasLargo = len(str(lista[2]))
            c += 1
    puntosMasLargo += 4
    for i,lista in enumerate(clon):

        clon[i][0] = clon[i][0] + " " * (nombreMasLargo - len(lista[0]))
        
        clon[i][1] = clon[i][1] + " " * 4

        clon[i][2] = str(clon[i][2]) 
        clon[i][2] = clon[i][2] + " " * (puntosMasLargo - len(clon[i][2]))
        
    display = centrar(Fore.CYAN + f'NOMBRE{" " * (nombreMasLargo - len("nombre"))}AÑO{" " * 3}TIEMPO(SEGUNDOS){" " * (puntosMasLargo - len("TIEMPO(SEGUNDOS)"))}')
    display += "\n\n\n"
    
    for i,lista in enumerate(clon):
        display += centrar(Fore.LIGHTBLACK_EX+ f'{i+1}_   {lista[0]}{lista[1]}{lista[2] + (" " * (len("tiempo(segundos)") - len(lista[2])))}{" " * len(str(i + 1)) + "    "}') 
        display += "\n"
    display += "\n\n" + Fore.CYAN + centrar("PRESIONA ENTER PARA CONTINUAR")
    
    print(centrar(display))
    def continuar(key):
        if key == keyboard.Key.enter:
            listener.stop()
            input()
    listener = keyboard.Listener(on_press=continuar)
    listener.start()
    listener.join()
    
   

    

    
        
def jugarMultijugador():
    global clon1,clon2,posInicialYMulti,posInicialXMulti
    clon1 = []
    clon2 = []
    mapaSeleccionado = labs[random.randint(0,1)][random.randint(0,2)]
    for x in mapaSeleccionado:
        clon1.append(x.copy())
        clon2.append(x.copy())
        
    posInicialXMulti,posInicialYMulti  = obtenerPosicionDelJugador(clon1)
    dibujarMultijugador(clon1,clon2)
    def moverMultijugador(key):
        global teclaPresionada1,teclaPresionada2,clon1,clon2,volverAlMenu
        inLab1,inList1 = obtenerPosicionDelJugador(clon1)
        inLab2,inList2 = obtenerPosicionDelJugador(clon2)
        if verificarAtributo(key) == "w" or verificarAtributo(key) == "s" or verificarAtributo(key) == "a" or verificarAtributo(key) == "d":
            if verificarAtributo(key) == "w" and clon1[inLab1 - 1][inList1] == 0 and  teclaPresionada1 == True:
                clon1[inLab1][inList1] = 0
                clon1[inLab1 - 1][inList1] = 5
                teclaPresionada1 = False
                dibujarMultijugador(clon1,clon2)
            elif verificarAtributo(key) == "w" and clon1[inLab1 - 1][inList1] == 2 and  teclaPresionada1 == True:
                clon1[inLab1][inList1] = 0
                clon1[inLab1 - 1][inList1] = 5
                teclaPresionada1 = False
                listenerMulti.stop()
                dibujarMultijugador(clon1,clon2)
                time.sleep(1)
                os.system("cls")
                print(centrar("¡Felicidades Jugador 1! Has Ganado",2)) 
                time.sleep(3)
            elif verificarAtributo(key) == "w" and (clon1[inLab1 - 1][inList1] == 3 or clon1[inLab1 - 1][inList1] == 4) and teclaPresionada1 == True:
                clon1[inLab1][inList1] = 0
                clon1[inLab1 - 1][inList1] = 4
                clon1[posInicialXMulti][posInicialYMulti] = 5
                teclaPresionada1 = False
                dibujarMultijugador(clon1,clon2)
                
                
            #* Movimiento Abajo     
            
            if verificarAtributo(key) == "s" and clon1[inLab1 + 1][inList1] == 0 and  teclaPresionada1 == True :
                clon1[inLab1][inList1] = 0
                clon1[inLab1 + 1][inList1] = 5
                teclaPresionada1 = False
                dibujarMultijugador(clon1,clon2)
            elif verificarAtributo(key) == "s" and clon1[inLab1 + 1][inList1] == 2 and  teclaPresionada1 == True:
                clon1[inLab1][inList1] = 0
                clon1[inLab1 + 1][inList1] = 5
                teclaPresionada1 = False
                listenerMulti.stop()
                dibujarMultijugador(clon1,clon2)    
                time.sleep(1)
                os.system("cls")
                print(centrar("¡Felicidades Jugador 1! Has Ganado",2)) 
                time.sleep(3)
            elif verificarAtributo(key) == "s" and (clon1[inLab1 + 1][inList1] == 3 or clon1[inLab1 + 1][inList1] == 4) and teclaPresionada1 == True:
                clon1[inLab1][inList1] = 0
                clon1[inLab1 + 1][inList1] = 4
                teclaPresionada1 = False
                clon1[posInicialXMulti][posInicialYMulti] = 5
                dibujarMultijugador(clon1,clon2)
            
            #* Movimiento Izquierda
                
            if verificarAtributo(key) == "a" and clon1[inLab1][inList1 - 1] == 0 and  teclaPresionada1 == True:
                clon1[inLab1][inList1] = 0
                clon1[inLab1][inList1 - 1] = 5
                teclaPresionada1 = False
                dibujarMultijugador(clon1,clon2)
                
            elif verificarAtributo(key) == "a" and clon1[inLab1][inList1 - 1] == 2 and  teclaPresionada1 == True:
                clon1[inLab1][inList1] = 0
                clon1[inLab1][inList1 - 1] = 5
                teclaPresionada1 = False
                listenerMulti.stop()
                dibujarMultijugador(clon1,clon2)            
                time.sleep(1)
                os.system("cls")
                print(centrar("¡Felicidades Jugador 1! Has Ganado",2)) 
                time.sleep(3)
            elif verificarAtributo(key) == "a" and (clon1[inLab1][inList1 - 1] == 3 or clon1[inLab1][inList1 - 1] == 4) and  teclaPresionada1 == True:
                clon1[inLab1][inList1] = 0
                clon1[inLab1][inList1 - 1] = 4
                teclaPresionada1 = False
                clon1[posInicialXMulti][posInicialYMulti] = 5
                dibujarMultijugador(clon1,clon2)
                
            #* Movimiento Derecha 
            
            if verificarAtributo(key) == "d" and clon1[inLab1][inList1 + 1] == 0 and teclaPresionada1 == True:
                clon1[inLab1][inList1] = 0
                clon1[inLab1][inList1 + 1] = 5
                teclaPresionada1 = False
                dibujarMultijugador(clon1,clon2)
                
                
            elif verificarAtributo(key) == "d" and clon1[inLab1][inList1 + 1] == 2 and  teclaPresionada1 == True:
                clon1[inLab1][inList1] = 0
                clon1[inLab1][inList1 + 1] = 5
                teclaPresionada1 = False
                listenerMulti.stop()    
                dibujarMultijugador(clon1,clon2)
                time.sleep(1)
                os.system("cls")
                print(centrar("¡Felicidades Jugador 1! Has Ganado",2)) 
                time.sleep(3)
            elif verificarAtributo(key) == "d" and (clon1[inLab1][inList1 + 1] == 3 or clon1[inLab1][inList1 + 1] == 4) and  teclaPresionada1 == True:
                clon1[inLab1][inList1] = 0
                clon1[inLab1][inList1 + 1] = 4
                teclaPresionada1 = False
                clon1[posInicialXMulti][posInicialYMulti] = 5
                dibujarMultijugador(clon1,clon2)
                
            #* Movimiento Arriba 
        elif key == keyboard.Key.up or key == keyboard.Key.right or key == keyboard.Key.down or key == keyboard.Key.left:
            if key == keyboard.Key.up and clon2[inLab2 - 1][inList2] == 0 and  teclaPresionada2 == True:
                clon2[inLab2][inList2] = 0
                clon2[inLab2 - 1][inList2] = 5
                teclaPresionada2 = False
                dibujarMultijugador(clon1,clon2)
            elif key == keyboard.Key.up and clon2[inLab2 - 1][inList2] == 2 and  teclaPresionada2 == True:
                clon2[inLab2][inList2] = 0
                clon2[inLab2 - 1][inList2] = 5
                teclaPresionada2 = False
                listenerMulti.stop()
                dibujarMultijugador(clon1,clon2)
                time.sleep(1)
                os.system("cls")
                print(centrar("¡Felicidades Jugador 2! Has Ganado",2)) 
                time.sleep(3)
            elif key == keyboard.Key.up and (clon2[inLab2 - 1][inList2] == 3 or clon2[inLab2 - 1][inList2] == 4) and teclaPresionada2 == True:
                clon2[inLab2][inList2] = 0
                clon2[inLab2 - 1][inList2] = 4
                clon2[posInicialXMulti][posInicialYMulti] = 5
                teclaPresionada2 = False
                dibujarMultijugador(clon1,clon2)
                
            #* Movimiento Abajo     
            
            if key == keyboard.Key.down and clon2[inLab2 + 1][inList2] == 0 and  teclaPresionada2 == True :
                clon2[inLab2][inList2] = 0
                clon2[inLab2 + 1][inList2] = 5
                teclaPresionada2 = False
                dibujarMultijugador(clon1,clon2)
            elif key == keyboard.Key.down and clon2[inLab2 + 1][inList2] == 2 and  teclaPresionada2 == True:
                clon2[inLab2][inList2] = 0
                clon2[inLab2 + 1][inList2] = 5
                teclaPresionada2 = False
                listenerMulti.stop()
                dibujarMultijugador(clon1,clon2)
                time.sleep(1)
                os.system("cls")
                print(centrar("¡Felicidades Jugador 2! Has Ganado",2)) 
                time.sleep(3)
            elif key == keyboard.Key.down and (clon2[inLab2 + 1][inList2] == 3 or clon2[inLab2 + 1][inList2] == 4) and teclaPresionada2 == True:
                clon2[inLab2][inList2] = 0
                clon2[inLab2 + 1][inList2] = 4
                teclaPresionada2 = False
                clon2[posInicialXMulti][posInicialYMulti] = 5
                dibujarMultijugador(clon1,clon2)
            
            #* Movimiento Izquierda
                
            if key == keyboard.Key.left and clon2[inLab2][inList2 - 1] == 0 and  teclaPresionada2 == True:
                clon2[inLab2][inList2] = 0
                clon2[inLab2][inList2 - 1] = 5
                teclaPresionada2 = False
                dibujarMultijugador(clon1,clon2)
                
            elif key == keyboard.Key.left and clon2[inLab2][inList2 - 1] == 2 and  teclaPresionada2 == True:
                clon2[inLab2][inList2] = 0
                clon2[inLab2][inList2 - 1] = 5
                teclaPresionada2 = False
                listenerMulti.stop()
                dibujarMultijugador(clon1,clon2)
                time.sleep(1)
                os.system("cls")
                print(centrar("¡Felicidades Jugador 2! Has Ganado",2)) 
                time.sleep(3)
            elif key == keyboard.Key.left and (clon2[inLab2][inList2 - 1] == 3 or clon2[inLab2][inList2 - 1] == 4) and  teclaPresionada2 == True:
                clon2[inLab2][inList2] = 0
                clon2[inLab2][inList2 - 1] = 4
                teclaPresionada2 = False
                clon2[posInicialXMulti][posInicialYMulti] = 5
                dibujarMultijugador(clon1,clon2)
            #* Movimiento Derecha 
            
            if key == keyboard.Key.right and clon2[inLab2][inList2 + 1] == 0 and teclaPresionada2 == True:
                clon2[inLab2][inList2] = 0
                clon2[inLab2][inList2 + 1] = 5
                teclaPresionada2 = False
                dibujarMultijugador(clon1,clon2)
            elif key == keyboard.Key.right and clon2[inLab2][inList2 + 1] == 2 and  teclaPresionada2 == True:
                clon2[inLab2][inList2] = 0
                clon2[inLab2][inList2 + 1] = 5
                teclaPresionada2 = False
                listenerMulti.stop()    
                dibujarMultijugador(clon1,clon2)
                time.sleep(1)
                os.system("cls")
                print(centrar("¡Felicidades Jugador 2! Has Ganado",2)) 
                time.sleep(3)
            elif key == keyboard.Key.right and (clon2[inLab2][inList2 + 1] == 3 or clon2[inLab2][inList2 + 1] == 4) and  teclaPresionada2 == True:
                clon2[inLab2][inList2] = 0
                clon2[inLab2][inList2 + 1] = 4
                teclaPresionada2 = False
                clon2[posInicialXMulti][posInicialYMulti] = 5
                dibujarMultijugador(clon1,clon2)
 
    
    listenerMulti = keyboard.Listener(on_press=moverMultijugador, on_release=resetMulti)
    listenerMulti.start()
    listenerMulti.join()       
        
def obtenerPosicionDelJugador(maps):
    for x in maps:
        for y in x:
            if y == 5:
                return (maps.index(x), x.index(y))

def verificarAtributo(key):
    if hasattr(key, "char"):
        return key.char
    else:
        return False

    

def moverJugador(key):
    global teclaPresionada,nivel,dificultad,laberinto,volverAlMenu,pausa
    inLab,inList = obtenerPosicionDelJugador(laberinto)

    #* Movimiento Arriba 
    
    if (key == keyboard.Key.up or verificarAtributo(key) == "w") and laberinto[inLab - 1][inList] == 0 and  teclaPresionada == True and pausa == 2:
        laberinto[inLab][inList] = 0
        laberinto[inLab - 1][inList] = 5
        teclaPresionada = False
        dibujarLaberinto(laberinto)
    elif (key == keyboard.Key.up or verificarAtributo(key) == "w") and laberinto[inLab - 1][inList] == 2 and  teclaPresionada == True and pausa == 2:
        laberinto[inLab][inList] = 0
        laberinto[inLab - 1][inList] = 5
        teclaPresionada = False
        listenerJuego.stop()
        dibujarLaberinto(laberinto)
    elif (key == keyboard.Key.up or verificarAtributo(key) == "w") and (laberinto[inLab - 1][inList] == 3 or laberinto[inLab - 1][inList] == 4) and teclaPresionada == True and pausa == 2:
        laberinto[inLab][inList] = 0
        laberinto[inLab - 1][inList] = 4
        laberinto[posInicialX][posInicialY] = 5
        teclaPresionada = False
        os.system("cls")
        print(centrar(centrar('"AHHHHHHHHHHHHHHHHH!!!"') + "\n" + centrar("OH NO!, TE HAS CAIDO EN UN POZO, TEN CUIDADO LA PROXIMA."))) 
        time.sleep(3)
        dibujarLaberinto(laberinto)
    #* Movimiento Abajo     
    
    if (key == keyboard.Key.down or verificarAtributo(key) == "s") and laberinto[inLab + 1][inList] == 0 and  teclaPresionada == True  and pausa == 2:
        laberinto[inLab][inList] = 0
        laberinto[inLab + 1][inList] = 5
        teclaPresionada = False
        dibujarLaberinto(laberinto)
    elif (key == keyboard.Key.down or verificarAtributo(key) == "s") and laberinto[inLab + 1][inList] == 2 and  teclaPresionada == True and pausa == 2:
        laberinto[inLab][inList] = 0
        laberinto[inLab + 1][inList] = 5
        teclaPresionada = False
        listenerJuego.stop()
        dibujarLaberinto(laberinto)
    elif (key == keyboard.Key.down or verificarAtributo(key) == "s") and (laberinto[inLab + 1][inList] == 3 or laberinto[inLab + 1][inList] == 4) and teclaPresionada == True and pausa == 2:
        laberinto[inLab][inList] = 0
        laberinto[inLab + 1][inList] = 4
        teclaPresionada = False
        laberinto[posInicialX][posInicialY] = 5
        os.system("cls")
        print(centrar(centrar('"AHHHHHHHHHHHHHHHHH!!!"') + "\n" + centrar("OH NO!, TE HAS CAIDO EN UN POZO, TEN CUIDADO LA PROXIMA.")))
        time.sleep(3)
        dibujarLaberinto(laberinto)
    #* Movimiento Izquierda
        
    if (key == keyboard.Key.left or verificarAtributo(key) == "a") and laberinto[inLab][inList - 1] == 0 and  teclaPresionada == True and pausa == 2:
        laberinto[inLab][inList] = 0
        laberinto[inLab][inList - 1] = 5
        teclaPresionada = False
        dibujarLaberinto(laberinto)
        
    elif (key == keyboard.Key.left or verificarAtributo(key) == "a") and laberinto[inLab][inList - 1] == 2 and  teclaPresionada == True and pausa == 2:
        laberinto[inLab][inList] = 0
        laberinto[inLab][inList - 1] = 5
        teclaPresionada = False
        listenerJuego.stop()
        dibujarLaberinto(laberinto)
    elif (key == keyboard.Key.left or verificarAtributo(key) == "a") and (laberinto[inLab][inList - 1] == 3 or laberinto[inLab][inList - 1] == 4) and  teclaPresionada == True and pausa == 2:
        laberinto[inLab][inList] = 0
        laberinto[inLab][inList - 1] = 4
        teclaPresionada = False
        laberinto[posInicialX][posInicialY] = 5
        os.system("cls")
        print(centrar(centrar('"AHHHHHHHHHHHHHHHHH!!!"') + "\n" + centrar("OH NO!, TE HAS CAIDO EN UN POZO, TEN CUIDADO LA PROXIMA.")))
        time.sleep(3)
        dibujarLaberinto(laberinto)
    #* Movimiento Derecha 
    
    if (key == keyboard.Key.right or verificarAtributo(key) == "d") and laberinto[inLab][inList + 1] == 0 and teclaPresionada == True and pausa == 2:
        laberinto[inLab][inList] = 0
        laberinto[inLab][inList + 1] = 5
        teclaPresionada = False
        dibujarLaberinto(laberinto)
    elif (key == keyboard.Key.right or verificarAtributo(key) == "d") and laberinto[inLab][inList + 1] == 2 and  teclaPresionada == True and pausa == 2:
        laberinto[inLab][inList] = 0
        laberinto[inLab][inList + 1] = 5
        teclaPresionada = False
        listenerJuego.stop()    
        dibujarLaberinto(laberinto)
    elif (key == keyboard.Key.right or verificarAtributo(key) == "d") and (laberinto[inLab][inList + 1] == 3 or laberinto[inLab][inList + 1] == 4) and  teclaPresionada == True and pausa == 2:
        laberinto[inLab][inList] = 0
        laberinto[inLab][inList + 1] = 4
        teclaPresionada = False
        laberinto[posInicialX][posInicialY] = 5
        os.system("cls")
        print(centrar(centrar('"AHHHHHHHHHHHHHHHHH!!!"') + "\n" + centrar("OH NO!, TE HAS CAIDO EN UN POZO, TEN CUIDADO LA PROXIMA.")))
        time.sleep(3)
        dibujarLaberinto(laberinto) 

def reset(key = None):
    global teclaPresionada,c
    teclaPresionada = True
    c += 1

def jugarNivel():
    global nivel,listenerJuego,laberinto,posInicialX,posInicialY
    laberinto = copy.deepcopy(labs[dificultad][nivel])
    posInicialX,posInicialY = obtenerPosicionDelJugador(laberinto)
    listenerJuego = keyboard.Listener(on_press=moverJugador, on_release=reset)
    listenerJuego.start()
    listenerJuego.join()
    c = 0
    nivel += 1
    
def efectoMaquina(texto):
    for caracter in texto:
        if caracter == " " or caracter == "\n":
            print(caracter, end='', flush=True)
            continue
        elif caracter == None:
            continue
        print(caracter, end='', flush=True) 
        escribirSFX[random.randint(0,2)].play()
        ran = 1
        while ran >= 0.15:
            ran = random.random()
        time.sleep(math.fabs(ran))
    
    if random.randint(1,4) % 2 == 0:
        finalescribir.play()    
    print() 

def pedirInfo(texto,centrarVer = False):
    if centrarVer == True:
        texto = centrar("\n" + centrar(texto,0),2)
        var = input(texto)
    else:
        texto = centrar(texto,0)
        var = input(texto)
    return var

def pantallaIncio(texto = "PRESIONE ENTER PARA COMENZAR\n"):
    os.system("cls")
    print(centrar(Fore.CYAN + texto))
    def click(key):
        
        if key == keyboard.Key.enter:
            listener.stop()
            input()
    listener = keyboard.Listener(on_press=click)
    listener.start()
    listener.join()
    
    
def escribirHistoria(texto, vertical = False, color = Fore.LIGHTWHITE_EX):
    if vertical:
        efectoMaquina(centrar(color + texto,2))
    else:
        efectoMaquina(centrar(color + texto))
    time.sleep(1)
    
pantallaIncio()
while True: 
    nivel = 0
    totalTiempo = 0
    
    
    select = creadorDeMenues(["JUGAR HISTORIA","MULTIJUGADOR","TOP JUGADORES\n","SALIR"])
    if select == 0:
        print()
        dificultad = creadorDeMenues(["PRINCIPIANTE","INTERMEDIO","EXPERTO\n","VOLVER AL MENU"])
        
        if dificultad == 3:
            continue 
        
        
        os.system("cls")
        time.sleep(.1)
        while True:
            nombreJugador = pedirInfo(Fore.LIGHTWHITE_EX + "Ingresa tu nombre, explorador(No mas de 15 caracteres): ",True)
            nombreJugador = nombreJugador[:15]
            anno = pedirInfo("Ingresa tu curso(numero y letra): ",0)
            anno = anno[:2]
            
            info = creadorDeMenues(["LA INFORMACION ES CORRECTA","LA INFORMACION ES INCORRECTA"])
            
            if info == 0:
                break
            
        
        os.system("cls")
        
        escribirHistoria("¡INTENTA PASAR LA HISTORIA EN EL MENOR TIEMPO POSIBLE Y LLEGAR AL TESORO ANTES QUE NADIE!",True,Fore.GREEN)
        
        os.system("cls")
        espacios = (anchoConsola - len("informacion"))// 2
        saltos = (altoConsola - 11) // 2
        print("\n" * saltos + " " * espacios + Fore.LIGHTMAGENTA_EX + "INFORMACION")
        print()
        print(espacios * " " + Fore.LIGHTWHITE_EX + "W/↑: ARRIBA" + "\n" + espacios * " "  + "S/↓: ABAJO" + "\n" + espacios * " " + "D/→: DERECHA" + "\n" + espacios * " " + "A/←: IZQUIERDA" + "\n")
        print()
        print(espacios * " " + Fore.GREEN + "X" + Fore.LIGHTWHITE_EX + ":SALIDA" + "\n" + espacios * " " + Fore.RED + "@" + Fore.LIGHTWHITE_EX + ":JUGADOR" + "\n" + espacios * " " + Fore.BLUE + "O" + Fore.LIGHTWHITE_EX + ":POZO")
    
        time.sleep(8)
        
        
        os.system("cls")
        escribirHistoria(f"{nombreJugador}, Estás adentrándote en una selva, un tesoro muy especial te espera al final!.",True)
        
        os.system("cls")
        escribirHistoria("Hace mucho tiempo, un antiguo explorador llamado Atticus",True)
        escribirHistoria("escondió su tesoro mágico en las profundidades de la selva.")
        escribirHistoria("Decidió protegerlo con pozos ocultos para que solo los aventureros más valientes y astutos pudieran encontrarlo.")
        os.system("cls")
        escribirHistoria("Atticus dejó obstáculos peligrosos en su camino para desviar a aquellos que buscaran el tesoro y ponerlos a prueba",True)
        os.system("cls")
        escribirHistoria("La historia de tu búsqueda del tesoro acaba de comenzar.",True)
        escribirHistoria("Tú eliges el camino que tomarás y que cosas emocionantes descubrirás.")
        escribirHistoria(f"Es una carrera contra reloj, muchos exploradores estan en busca del mismo tesoro. ¡Buena suerte, {nombreJugador}!")
        os.system("cls")
        
        inicio = time.time()
        
        if dificultad == 0:
            
            inicio = time.time()
            dibujarLaberinto(labs[dificultad][nivel])
            jugarNivel()
            totalTiempo += time.time() - inicio
            if volverAlMenu:
                volverAlMenu = False
                continue
            
            os.system("cls")
            escribirHistoria("¡Bien hecho! Haz logrado pasar el primer laberinto, pero cuidado, ",True)
            escribirHistoria("los próximos serán más difíciles. No te des por vencido")
            os.system("cls")
            escribirHistoria("¿Eso es un papel? A ver que dice...",True)
            os.system("cls")
            escribirHistoria("¡Alerta, valiente aventurero! Sumérgete en lo desconocido: un agujero sin visión. ¡Desafía tus sentidos y conquista lo invisible!",True,Fore.LIGHTRED_EX)
            os.system("cls")
            escribirHistoria("PREPARATE PARA EL PROXIMO DESAFIO",True)
            
            inicio = time.time()
            dibujarLaberinto(labs[dificultad][nivel])
            jugarNivel()
            totalTiempo += time.time() - inicio
            if volverAlMenu:
                volverAlMenu = False
                continue
            os.system("cls")
            escribirHistoria("¡Bien hecho! Ahora estas a un solo paso de llegar al tesoro, ¿podras cruzar el siguiente laberinto.",True)
            os.system("cls")
            escribirHistoria("PREPARATE PARA EL PROXIMO DESAFIO",True)
            
            inicio = time.time()
            dibujarLaberinto(labs[dificultad][nivel])
            jugarNivel()  
            totalTiempo += time.time() - inicio
            if volverAlMenu:
                volverAlMenu = False
                continue
            os.system("cls")
            escribirHistoria(f"¡Felicitaciones! {nombreJugador} haz logrado cruzar todos los laberintos y encontrar el tesoro.",True)
            os.system("cls")
            
            
            with open("rankingPrincipiante.txt", "a") as archivo:
                archivo.write(f"\n{nombreJugador},{anno},{round(totalTiempo,2)}")
            
        elif dificultad == 1:
            inicio = time.time()
            dibujarLaberinto(labs[dificultad][nivel])
            jugarNivel()
            totalTiempo += time.time() - inicio
            if volverAlMenu:
                volverAlMenu = False
                continue
            
            os.system("cls")
            escribirHistoria("¡Bien hecho! Haz logrado pasar el primer laberinto, pero ten cuidado,  el próximo te puede sorprender con más trampas que te harán iniciar de nuevo.",True)
            os.system("cls")
            escribirHistoria("Mira!! Alli!! Una pista de Atticus.",True)
            os.system("cls")
            escribirHistoria("¡Alerta, audaz explorador! Sumérgete en lo desconocido: un agujero sin visión. ¡Desafía tus sentidos y conquista lo invisible!",True,Fore.LIGHTRED_EX)
            os.system("cls")
            escribirHistoria("PREPARATE PARA EL PROXIMO DESAFIO",True)
            
            inicio = time.time()
            dibujarLaberinto(labs[dificultad][nivel])
            jugarNivel()
            totalTiempo += time.time() - inicio
            if volverAlMenu:
                volverAlMenu = False
                continue
            os.system("cls")
            escribirHistoria("¿Eso es... una advertencia?",True)
            os.system("cls")
            escribirHistoria("¡Bien hecho! Ahora estas a un solo paso de llegar al tesoro, ¿podras cruzar el siguiente laberinto?",True,Fore.LIGHTRED_EX)
            os.system("cls")
            escribirHistoria("PREPARATE PARA EL PROXIMO DESAFIO",True)
            
            inicio = time.time()
            dibujarLaberinto(labs[dificultad][nivel])
            jugarNivel()  
            totalTiempo += time.time() - inicio
            if volverAlMenu:
                volverAlMenu = False
                continue
            os.system("cls")
            escribirHistoria(f"¡Felicitaciones! {nombreJugador} haz logrado cruzar todos los laberintos y encontrar el tesoro",True)
            os.system("cls")
            
            
            with open("rankingIntermedio.txt", "a") as archivo:
                archivo.write(f"\n{nombreJugador},{anno},{round(totalTiempo,2)}")
        elif dificultad == 2:
            inicio = time.time()
            dibujarLaberinto(labs[dificultad][nivel])
            jugarNivel()
            totalTiempo += time.time() - inicio
            if volverAlMenu:
                volverAlMenu = False
                continue
            os.system("cls")
            escribirHistoria("Mira!! Has encontrado un mensaje de Atticus",True)
            os.system("cls")
            escribirHistoria("¡Bien hecho! Haz logrado pasar el primer laberinto, pero cuidado,",True)
            escribirHistoria("los próximos serán más difíciles, y te encontraras con múltiples trampas que te harán volver a la entrada")
            os.system("cls")
            escribirHistoria("Aquello es.. ¡Una Pista!",True)
            os.system("cls")
            escribirHistoria("¡Atención, valiente explorador! Pozos ocultos: una prueba a ciegas. ¡No te caigas en ellos!",True,Fore.LIGHTRED_EX)
            os.system("cls")
            escribirHistoria("PREPARATE PARA EL PROXIMO DESAFIO",True)
            
            inicio = time.time()
            dibujarLaberinto(labs[dificultad][nivel])
            jugarNivel()
            totalTiempo += time.time() - inicio
            if volverAlMenu:
                volverAlMenu = False
                continue
            os.system("cls")
            escribirHistoria("Aqui!! Otra pista:",True)
            os.system("cls")
            escribirHistoria("¡Bien hecho! Ahora estas a un solo paso de llegar al tesoro, pero ahora será más difícil. ¡Ten cuidado!.",True)
            os.system("cls")
            escribirHistoria("¿Eso es un poema?",True)
            os.system("cls")       
            escribirHistoria("Un ultimo laberinto has de cruzar, si lo haces, al tesoro llegaras.",True,Fore.LIGHTRED_EX)
            os.system("cls")
            escribirHistoria("PREPARATE PARA EL PROXIMO DESAFIO",True)
            os.system("cls")
            
            inicio = time.time()
            dibujarLaberinto(labs[dificultad][nivel])
            jugarNivel()  
            totalTiempo += time.time() - inicio
            if volverAlMenu:
                volverAlMenu = False
                continue
            os.system("cls")
            escribirHistoria(f"¡Felicitaciones! {nombreJugador} haz logrado cruzar todos los laberintos y encontrar el tesoro.",True)
            os.system("cls")
            
            
            with open("rankingAvanzado.txt", "a") as archivo:
                archivo.write(f"\n{nombreJugador},{anno},{round(totalTiempo,2)}")
        elif dificultad == 3:
            continue
        
        
        pantallaIncio("PRESIONE ENTER PARA VOLVER AL MENU\n")   
    elif select == 1:
        os.system("cls")
        jugarMultijugador()
        
    elif select == 2:
        
        while True:
            seleccion = creadorDeMenues(["PRINCIPIANTE","INTERMEDIO","AVANZADO\n","VOLVER"])
            
            if seleccion == 0:
                with open("rankingPrincipiante.txt", "r") as ranking:
                    topJugadores(ranking)
            elif seleccion == 1:
                with open("rankingIntermedio.txt", "r") as ranking:
                    topJugadores(ranking)
            elif seleccion == 2:
                with open("rankingAvanzado.txt", "r") as ranking:
                    topJugadores(ranking)
            elif seleccion == 3:
                break
    elif select == 3: 
        os.system("cls")
        print(centrar("Muchas Gracias Por Jugar",6))
        break
pygame.mixer.quit()