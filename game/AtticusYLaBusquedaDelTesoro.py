import os,time,pygame,shutil
from pynput import keyboard
from colorama import Fore,Back,Style

anchoConsola,_ = shutil.get_terminal_size()
select = 0

def centrar(mensaje):
    espacios = (anchoConsola - len(mensaje)) // 2
    mensaje = " " * espacios + mensaje
    return mensaje
#Pantalla al iniciar el juego
def pantallaDeInicio(key = "s"):
    os.system("cls")
    mensaje = Fore.CYAN + "PRESIONE ESPACIO PARA COMENZAR"
    espacios = (anchoConsola - len(mensaje)) // 2
    mensaje = "\n" + "\n" + "\n" + "\n" + "\n" "\n" + "\n" + "\n" + "\n" + "\n" + " " * espacios + mensaje
    
    print(mensaje)
    if key == keyboard.Key.space:
            listener.stop()  
            os.system("cls")
            
            
def menu(key = None):
    global select
    os.system("cls")
    
    op1 = "JUGAR HISTORIA"
    op2 = "MULTIJUGADOR"
    op3 = "SALIR"
    
    if hasattr(key, "char") == False:
        print()
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
        op2 = centrar("   " + op2)
        op3 = centrar("   " + op3)
        op1 = centrar("-> " + op1)
    elif select == 1:
        op3 = centrar("   " + op3)
        op1 = centrar("   " + op1)
        op2 = centrar("-> " + op2)
    elif select == 2:
        op1 = centrar("   " + op1)
        op2 = centrar("   " + op2)
        op3 = centrar("-> " + op3)
    print(op1)
    print(op2)
    print(op3)
    if key == keyboard.Key.space or key == keyboard.Key.enter:
        
        return select

 
        
pantallaDeInicio()
listener = keyboard.Listener(on_press=pantallaDeInicio)
listener.start()
listener.join()



    
    
def menuPrincipal(key = "a sss"):    
    op = menu(key)
    
    if op == 0:
        print("A entrado al modo historia")
        listenerMenu.stop()
    elif op == 1:
        print("A entrado al modo multijugador")
        listenerMenu.stop()
    elif op == 2:
        print("Gracias por Jugar")
        listenerMenu.stop()

menuPrincipal()
listenerMenu = keyboard.Listener(on_press=menuPrincipal)
listenerMenu.start()
listenerMenu.join()