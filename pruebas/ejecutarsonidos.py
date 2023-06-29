import time,random,math

def efectoMaquina(texto):
    for caracter in texto:
        print(caracter, end='', flush=True) 
        ran = 1
        while ran >= 0.3:
            ran = random.random()
        time.sleep(math.fabs(ran))
    print() 
    
    
efectoMaquina("Holaaaa")