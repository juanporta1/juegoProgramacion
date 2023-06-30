import os,time,pygame,shutil,copy
from pynput import keyboard
from colorama import Fore,Back,Style
from niveles import labs
import math,random
pygame.mixer.init()

maquinaDeEscribir1 = pygame.mixer.Sound("maquina1.mp3")
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
    mensaje = Fore.CYAN + "PRESIONE C PARA COMENZAR"
    espacios = (anchoConsola - len(mensaje)) // 2
    mensaje = " " * espacios + mensaje
    
    print(centrarV(mensaje))
    if verificarAtributo(key) == "c":
            listener.stop()  
            os.system("cls")
            
            
def menu(key = None):
    global select
    os.system("cls")
    
    op1 = "JUGAR HISTORIA"
    op2 = "MULTIJUGADOR  "
    op3 = "SALIR         "
    
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
    print(centrarH("PRESIONE C PARA SLECCIONAR", 2))
    if verificarAtributo(key) == "c":
        listenerMenu.stop()
        
def hacedorDeMenues(**ops):
    
    select = 0
    listener = keyboard.Listener(on_press=seleccion)
    listener.start()
    listener.join()
    
    def seleccion(key):
        clon = ops
        c = 0
        mayop = 0
        for op in clon:
            if c == 0 or len(op) > mayop:
                mayop = op
            
        for op in clon:
            espacios = mayop - len(op)
            op = op + espacios * " "
        
        if key == keyboard.Key.up:
            if select == 0:
                select = len(clon) - 1
            else:
                select -= 1
        if key == keyboard.Key.down:
            if select == len(clon) - 1:
                select = 0
            else:
                select += 1
                        
        
        clon[select] = "-> " + clon[select]
        
        for op in clon:
            print(centrarH(op))
        

        
def seleccionarDificultad(key = None):
    global dificultad
    os.system("cls")
    print(centrarH(Fore.LIGHTBLUE_EX + "  SELECCIONE LA DIFICULTAD", 12) + "\n\n\n\n")
    op1 =  "PRINCIPIANTE"
    op2 =  "INTERMEDIO  "
    op3 =  "EXPERTO     "
    
    if hasattr(key, "char") == False:
        g = 1
    elif key.char == keyboard.Key.up: 
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
    
        
    print(centrarH(op1))
    print(centrarH(op2))
    print(centrarH(op3))
    print(centrarH("PRESIONE C PARA SLECCIONAR", 2))
    
    if verificarAtributo(key) == "c":
        listener.stop()

def draw(maps):
    #? 0 = Espacio Vacio
    #? 1 = Pared
    #? 2 = Meta
    #? 3 = Pozo Que No Se Ve
    #? 4 = Pozo Que Se Ve
    #? 5 = Jugador
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
            elif y == 0 or y == 3:
                linea += "  "
            elif y == 4:
                linea += Fore.BLUE + "O "
        
        espacios = (ancho - len(x))// 2
        linea = " " * math.trunc((espacios / 1.25)) + linea
        display += linea + "\n"
    os.system("cls")
    print(display)
    print(centrarH(Fore.LIGHTCYAN_EX + "W/↑:ARRIBA  S/↓:ABAJO  A/←:IZQUIERDA  D/→:DERECHA",4))
    
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

    #* Movimiento Arriba 
    
    if (key == keyboard.Key.up or verificarAtributo(key) == "w") and laberinto[inLab - 1][inList] == 0 and  teclaPresionada == True:
        laberinto[inLab][inList] = 0
        laberinto[inLab - 1][inList] = 5
        teclaPresionada = False
        
    elif (key == keyboard.Key.up or verificarAtributo(key) == "w") and laberinto[inLab - 1][inList] == 2 and  teclaPresionada == True:
        laberinto[inLab][inList] = 0
        laberinto[inLab - 1][inList] = 5
        teclaPresionada = False
        listenerJuego.stop()
    elif (key == keyboard.Key.up or verificarAtributo(key) == "w") and (laberinto[inLab - 1][inList] == 3 or laberinto[inLab - 1][inList] == 4) and teclaPresionada == True:
        laberinto[inLab][inList] = 0
        laberinto[inLab - 1][inList] = 4
        laberinto[posInicialX][posInicialY] = 5
        teclaPresionada = False
        os.system("cls")
        print(centrarV(centrarH('"AHHHHHHHHHHHHHHHHH!!!"')))
        print(centrarH("OH NO!, TE HAS CAIDO EN UN POZO, TEN CUIDADO LA PROXIMA."))
        time.sleep(3)
        
    #* Movimiento Abajo     
    
    if (key == keyboard.Key.down or verificarAtributo(key) == "s") and laberinto[inLab + 1][inList] == 0 and  teclaPresionada == True :
        laberinto[inLab][inList] = 0
        laberinto[inLab + 1][inList] = 5
        teclaPresionada = False
        
    elif (key == keyboard.Key.down or verificarAtributo(key) == "s") and laberinto[inLab + 1][inList] == 2 and  teclaPresionada == True:
        laberinto[inLab][inList] = 0
        laberinto[inLab + 1][inList] = 5
        teclaPresionada = False
        listenerJuego.stop()
    
    elif (key == keyboard.Key.down or verificarAtributo(key) == "s") and (laberinto[inLab + 1][inList] == 3 or laberinto[inLab + 1][inList] == 4) and teclaPresionada == True:
        laberinto[inLab][inList] = 0
        laberinto[inLab + 1][inList] = 4
        teclaPresionada = False
        laberinto[posInicialX][posInicialY] = 5
        os.system("cls")
        print(centrarV(centrarH('"AHHHHHHHHHHHHHHHHH!!!"')))
        print(centrarH("OH NO!, TE HAS CAIDO EN UN POZO, TEN CUIDADO LA PROXIMA."))
        time.sleep(3)
    
    #* Movimiento Izquierda
        
    if (key == keyboard.Key.left or verificarAtributo(key) == "a") and laberinto[inLab][inList - 1] == 0 and  teclaPresionada == True:
        laberinto[inLab][inList] = 0
        laberinto[inLab][inList - 1] = 5
        teclaPresionada = False
        
        
    elif (key == keyboard.Key.left or verificarAtributo(key) == "a") and laberinto[inLab][inList - 1] == 2 and  teclaPresionada == True:
        laberinto[inLab][inList] = 0
        laberinto[inLab][inList - 1] = 5
        teclaPresionada = False
        listenerJuego.stop()
    
    elif (key == keyboard.Key.left or verificarAtributo(key) == "a") and (laberinto[inLab][inList - 1] == 3 or laberinto[inLab][inList - 1] == 4) and  teclaPresionada == True:
        laberinto[inLab][inList] = 0
        laberinto[inLab][inList - 1] = 4
        teclaPresionada = False
        laberinto[posInicialX][posInicialY] = 5
        os.system("cls")
        print(centrarV(centrarH('"AHHHHHHHHHHHHHHHHH!!!"')))
        print(centrarH("OH NO!, TE HAS CAIDO EN UN POZO, TEN CUIDADO LA PROXIMA."))
        time.sleep(3)
    #* Movimiento Derecha 
    
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
    elif (key == keyboard.Key.right or verificarAtributo(key) == "d") and (laberinto[inLab][inList + 1] == 3 or laberinto[inLab][inList + 1] == 4) and  teclaPresionada == True:
        laberinto[inLab][inList] = 0
        laberinto[inLab][inList + 1] = 4
        teclaPresionada = False
        laberinto[posInicialX][posInicialY] = 5
        os.system("cls")
        print(centrarV(centrarH('"AHHHHHHHHHHHHHHHHH!!!"')))
        print(centrarH("OH NO!, TE HAS CAIDO EN UN POZO,Y HAS VUELTO A LA ENTRADA \n TEN CUIDADO LA PROXIMA."))
        time.sleep(3)
        
    draw(laberinto)

def reset(key = None):
    global teclaPresionada
    teclaPresionada = True

def jugarNivel():
    global nivel,listenerJuego,laberinto,posInicialX,posInicialY
    laberinto = copy.deepcopy(labs[dificultad][nivel])
    posInicialX,posInicialY = getPlayerPosition(laberinto)
    listenerJuego = keyboard.Listener(on_press=movePlayer, on_release=reset)
    listenerJuego.start()
    listenerJuego.join()
    
    nivel += 1
    
def efectoMaquina(texto):
    for caracter in texto:
        if caracter == " " or caracter == "\n":
            print(caracter, end='', flush=True)
            continue
        print(caracter, end='', flush=True) 
        ran = 1
        while ran >= 0.2:
            ran = random.random()
        time.sleep(math.fabs(ran))
        
    print() 

def pedirInfo(texto,centrarVer = False):
    if centrarVer == False:
        texto = centrarH(texto)
        var = input(texto)
    else:
        texto = centrarV(centrarH(texto))
        var = input(texto)
    return var

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
        
        os.system("cls")
        
        nombreJugador = pedirInfo(Fore.LIGHTWHITE_EX + "Ingresa tu nombre, explorador: ",True)
        anno = pedirInfo("Ingresa tu curso(numero y letra): ")
        
        os.system("cls")
        espacios = (anchoConsola - len("informacion"))// 2
        saltos = (altoConsola - 11) // 2
        print("\n" * saltos + " " * espacios + Fore.LIGHTMAGENTA_EX + "INFORMACION")
        print()
        print(espacios * " " + Fore.LIGHTWHITE_EX + "W/↑: ARRIBA" + "\n" + espacios * " "  + "S/↓: ABAJO" + "\n" + espacios * " " + "D/→: DERECHA" + "\n" + espacios * " " + "A/←: IZQUIERDA")
        print()
        print(espacios * " " + Fore.GREEN + "X" + Fore.LIGHTWHITE_EX + ":SALIDA" + "\n" + espacios * " " + Fore.RED + "@" + Fore.LIGHTWHITE_EX + "JUGADOR" + "\n" + espacios * " " + Fore.BLUE + "O" + Fore.LIGHTWHITE_EX + "POZO")
    
        time.sleep(8)
        
        
        os.system("cls")
        efectoMaquina(centrarV(centrarH(f"{nombreJugador}, estás adentrándote en una selva en busca de un tesoro muy especial.")))
        time.sleep(2)
        os.system("cls")
        efectoMaquina(centrarV(centrarH("Cuenta la leyenda que hace mucho tiempo un antiguo explorador, llamado Atticus,")) + "\n" +  centrarH("escondió su tesoro mágico en las profundidades de la selva.") + "\n"+ centrarH("Este, decidió proteger el tesoro para que solo los aventureros más valientes y dignos pudieran encontrarlo."))
        time.sleep(2)
        os.system("cls")
        efectoMaquina(centrarV(centrarH("Atticus dejó obstáculos peligrosos en su camino para desviar a aquellos que buscaran el tesoro y poner a prueba su coraje y astucia.")))
        time.sleep(2)
        os.system("cls")
        efectoMaquina(centrarV(centrarH("La historia de tu búsqueda del tesoro en la selva está por comenzar. ")) + "\n" + centrarH("Tú eliges el camino que tomarás y las cosas emocionantes que descubrirás. ") + "\n" + centrarH(f"Y apresúrate en hacerlo en el menor tiempo posible los otros exploradores estan en busca del mismo. ¡Buena suerte, {nombreJugador}!"))
        time.sleep(2)
        
        if dificultad == 0:
            
            draw(labs[dificultad][nivel])
            jugarNivel()
            
            os.system("cls")
            efectoMaquina(centrarV(centrarH(Fore.LIGHTWHITE_EX + "¡Bien hecho! Haz logrado pasar el primer laberinto, pero cuidado,")) + "\n" +  centrarH("los próximos serán más difíciles, y te encontraras con trampas que te harán volver a la entrada"))
            time.sleep(2)
            os.system("cls")
            print(centrarV(centrarH(Fore.LIGHTRED_EX + "IMPORTANTE: AL PRINCIPIO NO VERAS LOS POZOS, PERO SI TE CAES EN UNO, SABRAS DONDE ESTA, AUNQUE COMENZARAS DESDE EL PRINCIPIO.")))
            time.sleep(4)
            os.system("cls")
            efectoMaquina(centrarV(centrarH(Fore.LIGHTWHITE_EX + "HAS PASADO EL PRIMER LABERINTO, PREPARATE PARA EL PROXIMO DESAFIO")))  
            
            
                  
            draw(labs[dificultad][nivel])
            jugarNivel()
            os.system("cls")
            efectoMaquina(centrarV(centrarH("¡Bien hecho! Ahora estas a un solo paso de llegar al tesoro, ¿podras cruzar el siguiente laberinto."))) 
            time.sleep(2)
            os.system("cls")
            efectoMaquina(centrarV(centrarH("HAS PASADO EL SEGUNDO LABERINTO, PREPARATE PARA EL PROXIMO DESAFIO")))  
            
            
            
            draw(labs[dificultad][nivel])
            jugarNivel()  
            os.system("cls")
            efectoMaquina(centrarV(centrarH(Fore.LIGHTWHITE_EX + f"¡Felicitaciones! {nombreJugador} haz logrado cruzar todos los laberintos y encontrar el tesoro.")))
            time.sleep(2)
            os.system("cls")
            
        elif dificultad == 1:
            
            draw(labs[dificultad][nivel])
            jugarNivel()
            
            
            os.system("cls")
            efectoMaquina(centrarV(centrarH(Fore.LIGHTWHITE_EX + "¡Bien hecho! Haz logrado pasar el primer laberinto, pero ten cuidado,  el próximo te puede sorprender con trampas que te harán iniciar de nuevo.")))
            time.sleep(2)
            os.system("cls")
            print(centrarV(centrarH(Fore.LIGHTRED_EX + "IMPORTANTE: AL PRINCIPIO NO VERAS LAS TRAMPAS, PERO SI TE CAES EN UNA, DESCUBRIRAS DONDE SE ENCONTRABA, AUNQUE COMENZARAS DESDE EL PRINCIPIO.")))
            time.sleep(4)
            os.system("cls")
            efectoMaquina(centrarV(centrarH(Fore.LIGHTWHITE_EX + "HAS PASADO EL PRIMER LABERINTO, PREPARATE PARA EL PROXIMO DESAFIO")))  
            time.sleep(2)
            
                  
            draw(labs[dificultad][nivel])
            jugarNivel()
            os.system("cls")
            efectoMaquina(centrarV(centrarH(Fore.LIGHTWHITE_EX + "¡Bien hecho! Ahora estas a un solo paso de llegar al tesoro, ¿podras cruzar el siguiente laberinto? Este será aun mas difícil."))) 
            time.sleep(2)
            os.system("cls")
            efectoMaquina(centrarV(centrarH(Fore.LIGHTWHITE_EX + "HAS PASADO EL SEGUNDO LABERINTO, PREPARATE PARA EL PROXIMO DESAFIO")))  
            time.sleep(2)
            
            
            draw(labs[dificultad][nivel])
            jugarNivel()  
            os.system("cls")
            efectoMaquina(centrarV(centrarH(Fore.LIGHTWHITE_EX + f"¡Felicitaciones! {nombreJugador} haz logrado cruzar todos los laberintos y encontrar el tesoro")))
            time.sleep(2)
            os.system("cls")
        
        elif dificultad == 2:
            
            draw(labs[dificultad][nivel])
            jugarNivel()
            os.system("cls")
            efectoMaquina(centrarV(centrarH(Fore.LIGHTWHITE_EX + "¡Bien hecho! Haz logrado pasar el primer laberinto, pero cuidado,")) + "\n" +  centrarH("los próximos serán más difíciles, y te encontraras con trampas que te harán volver a la entrada"))
            time.sleep(2)
            os.system("cls")
            print(centrarV(centrarH(Fore.LIGHTRED_EX + "IMPORTANTE: AL PRINCIPIO NO VERAS LOS POZOS, PERO SI TE CAES EN UNO, SABRAS DONDE ESTA, AUNQUE COMENZARAS DESDE EL PRINCIPIO.")))
            time.sleep(4)
            os.system("cls")
            efectoMaquina(centrarV(centrarH(Fore.LIGHTWHITE_EX + "HAS PASADO EL PRIMER LABERINTO, PREPARATE PARA EL PROXIMO DESAFIO")))  
            time.sleep(2)
            
            draw(labs[dificultad][nivel])
            jugarNivel()
            efectoMaquina(centrarV(centrarH(Fore.LIGHTWHITE_EX + "¡Bien hecho! Ahora estas a un solo paso de llegar al tesoro, pero ahora será más difícil tendrás que lidiar con trampas y puertas mágicas."))) 
            
            print(centrarV(centrarH(Fore.LIGHTRED_EX + "IMPORTANTE: AL PRINCIPIO NO VERAS LOS POZOS, PERO SI TE CAES EN UNO, SABRAS DONDE ESTA, AUNQUE COMENZARAS DESDE EL PRINCIPIO.")))
            time.sleep(4)
            os.system("cls")
            efectoMaquina(centrarV(centrarH(Fore.LIGHTWHITE_EX + "HAS PASADO EL SEGUNDO LABERINTO, PREPARATE PARA EL PROXIMO DESAFIO")))  
            time.sleep(2)
            
            os.system("cls")
            print(centrarV(centrarH(Fore.LIGHTRED_EX + "IMPORTANTE: ANTES DE PODER ACCEDER A CIERTOS LUGARES DEBERAS ABRIR UNA PUERTA QUE ESTA Y PARA ESO DEBERAS BUSCAR SU LLAVE, LA CUAL TIENE EL MISMO COLOR.")))
            time.sleep(4)
            os.system("cls")
            
            draw(labs[dificultad][nivel])
            jugarNivel()  
            efectoMaquina(centrarV(centrarH(Fore.LIGHTWHITE_EX + f"¡Felicitaciones! {nombreJugador} haz logrado cruzar todos los laberintos y encontrar el tesoro.")))
            os.system("cls")
            time.sleep(2)
            
            
    elif select == 1:
        os.system("cls")
        print(centrarH("Holaaa",6))
        time.sleep(5)
    elif select == 2: 
        os.system("cls")
        print(centrarH("Muchas Gracias Por Jugar",6))
        break
    
pygame.mixer.quit()