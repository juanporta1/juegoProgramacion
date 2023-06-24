from pynput import keyboard
import os
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
g = 0
def printt(key):
        print("Tecla presionada: {0}".format(key))
    
listener = keyboard.Listener(on_press=printt)
listener.start()
while True:
    if g == 1:
        break
    else:
        continue
listener.stop()