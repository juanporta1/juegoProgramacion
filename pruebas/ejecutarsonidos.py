import shutil

texto = "Hola, mundo!"

# Obtener el ancho de la consola
ancho_consola, alto = shutil.get_terminal_size()

# Calcular la cantidad de espacios necesarios para centrar el texto
espacios = (ancho_consola - len(texto)) // 2

# Generar la cadena con los espacios a la izquierda y el texto centrado
texto_centralizado = " " * espacios + texto

# Imprimir el texto centrado en la consola
print(texto_centralizado, alto)