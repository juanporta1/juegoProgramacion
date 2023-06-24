from pynput import keyboard
import os

select = 0
def menu(key = None):
    global select
    os.system("cls")
    op1 = "Iniciar Juego"
    op2 = "Multijugador"
    op3 = "Salir"
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
        
    
    print(op1)
    print(op2)
    print(op3)
    if key == keyboard.Key.enter:
        return select
def loop(key):    
    op = menu(key)
    
    if op == 0:
        print("A entrado al modo historia")
    elif op == 1:
        print("A entrado al modo multijugador")
    elif op == 2:
        print("Gracias por Jugar")

menu()
listener = keyboard.Listener(on_press=loop)
listener.start()
listener.join()