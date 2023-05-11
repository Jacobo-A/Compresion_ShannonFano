
# Autor: Alejandro Flores Jacobo 
# Fecha: 11-05-2023
# Descripcion: 
# Script aplicar el algoritmo de compresion Shannon Fano a un archivo.
import time
inicio = time.time()
# ---------------------------[Función para dividir una lista en dos sublistas con frecuencias casi iguales]---------------------------
def split_list(lst):
    total = sum(freq for _, freq in lst)    # Calcula la frecuencia total de los elementos en la lista
    half = total / 2                        # Calcula la mitad de la frecuencia total
    
    # Inicializa algunas variables para controlar el índice actual, la frecuencia de la lista derecha
    # y los índices de inicio y fin de la lista.
    index = 0
    right = 0 
    inicio = 0
    fin = len(lst)-1
    
    if len(lst) == 2:   # Si la lista tiene solo dos elementos, devuelve el primer elemento en una lista y el segundo en otra.
        index = 1       # Esto es un caso especial, ya que la división de la lista no se puede hacer de otra manera.
        
    else:               # Busca el índice en el cual la lista se puede dividir en dos sublistas con frecuencias casi iguales.
        while True:
            right += lst[inicio][1]  # Agrega la frecuencia del elemento actual a la frecuencia de la lista derecha      
            if (right >= half):      # Si la lista derecha supera la mitad de la frecuencia total
                index = inicio       # guarda el índice actual como el índice de división y rompe el ciclo.
                if inicio == fin:    # Si el índice de inicio es igual al índice de fin, significa que el índice actual es el índice  final de la lista.
                    index = inicio+1 # En ese caso, el índice de división se establece en el índice actual más uno,
                    break            # lo que significa que toda la lista irá a la lista izquierda y la lista derecha estará vacía.
                break
            fin += -1       # Si la frecuencia de la lista derecha todavía no supera la mitad de la frecuencia total, 
            inicio += 1     # aumenta el índice de inicio y disminuye el índice de fin.
            

    # Devuelve las dos sublistas: la primera que va desde el principio hasta el índice de división
    # y la segunda que va desde el índice de división hasta el final.  
    return lst[:index], lst[index:]


# ---------------------------[Función para asignar códigos a cada símbolo usando el algoritmo de Shannon Fano]---------------------------
def shannon_fano(lst, code=""):
    if len(lst) == 1:
        symbol = lst[0][0]
        codes[symbol] = code # Guardar el código asignado al símbolo
        return
    # Dividir la lista en dos sublistas con frecuencias casi iguales
    right, left = split_list(lst)
    # Asignar un bit a cada sublista y recursivamente codificar los símbolos
    shannon_fano(left, code + "0")
    shannon_fano(right, code + "1")
 

# ---------------------------[Lectura del archivo]---------------------------
# Nombre del archivo a leer
archivo = 'h.jpg'
# archivo = 'archivo.py'
# archivo = 'archivo.bin'

with open(archivo, 'rb') as f:  # Leer el contenido del archivo
    cadena = f.read()
    f.close()

if (len(cadena)) % 2 != 0:    # Verificar si hay simbolos suficientes de 2 bytes
    cadena += b'\x00'         # Agregar un byte de padding

# Funcion para determinar el tamano apropiado para los simbolos siendo 16 caracteres o 2 bytes como maximo 
tope = 1     # Se establece una variable tope en 1, que será utilizada para determinar el tamaño apropiado para los símbolos.
while True:
    if len(cadena) == 2:    # Si la longitud es 2 concluye el bucle ya el tamano de los simbolos es el apropiado
        break
    if len(cadena)//tope <= tope:break   # Mientras el cocienente  sea menor al tope y concluye el bucle
    if tope == 16: break                 # El maximo tamano apropiado para un simbolo y concluye el bucle 
    else: tope *= 2                      # Mientras el cocienente  sea mayor al tope, duplicamos el tope.
         
dic_frecuencias = {}     # Diccionario para guardar la frecuencia de cada símbolo
for i in range(0, len(cadena), tope):   # Recorrer el contenido del archivo
    simbolo = cadena[i:i+tope]          # Obtener el símbolo como una cadena de bytes de 2 bytes
    if simbolo in dic_frecuencias:           # Actualizar la frecuencia del símbolo en el diccionario
        dic_frecuencias[simbolo] += 1
    else:
        dic_frecuencias[simbolo] = 1
if len(dic_frecuencias)==1:
    print("Solo hay un simbolo en el archivo, se interrumpe el script.")
    exit()



# Ordenar los símbolos por frecuencia ascendente
sorted_freqs = sorted(dic_frecuencias.items(), key=lambda x: (x[1]))

# ---------------------------[Codificador]---------------------------

# Aplicar el algoritmo de Shannon Fano para codificar los símbolos
codes = {}  # Diccionario para guardar los códigos asignados a cada símbolo
shannon_fano(sorted_freqs)

cadena_binaria = ''
for i in range(0, len(cadena), tope):   # Recorrer el contenido del archivo
    llave = cadena[i:i+tope]          # Se concatenan los simbolos codificados en binario
    cadena_binaria +=  codes[llave] # Busca en el diccionario la llave de acuerdo al simbolo

# Rellenar la cadena de bits con ceros a la derecha hasta que tenga una longitud múltiplo de 8 utilizamos '1' como bandera
resto = len(cadena_binaria)%8
if resto != 0:
    cadena_binaria += '1'+('0'*(7-resto))

# A partir de la cadena binaria forma enteros en bloques de 8 simbolos
lista_de_Bytes = [int(cadena_binaria[i:i+8],2) for i in range(0, len(cadena_binaria),8)] 

# Escribir los bytes en el archivo
with open("codificado.shfa", "wb") as f:    # Crea el archivo .huff  
    for b in lista_de_Bytes:
        f.write(bytes([b]))  # Lo enteros se escriben en el archivo de forma binaria
    f.close()

fin = time.time()
tiempo_total = fin - inicio
print(f"El programa tardó {tiempo_total} segundos en crear el archivo .shfa")

# -----------------------------------------[DECODIFICADOR]-----------------------------------------
# Abrir el archivo en modo lectura de bytes
with open("codificado.shfa", "rb") as f:
    # Leer el contenido del archivo en un objeto bytes
    contenido = f.read()
    f.close()

# Convertir el objeto bytes a una cadena binaria y añadir ceros iniciales
cadena_codificada = ''.join([bin(b)[2:].zfill(8) for b in contenido])

# Quitar el zeroo pading de la cadena
while True:
    if cadena_codificada[-1] == '1': # Se utiliza el primer '1' mas significativo como bandera
        cadena_codificada = cadena_codificada[:-1]
        break
    else:
        cadena_codificada = cadena_codificada[:-1] # Borra todos los '0' de derecha a izquierda 'zero padding'

# Decodificar la cadena de bits utilizando la tabla de códigos Huffman
codigo_temporal = ''
cadena_decodificada = bytes()

# invertir elementos y claves
diccionario_invertido = {valor: clave for clave, valor in codes.items()}

# # Recorre cada bit de la cadena codificada
for bit in cadena_codificada:
    codigo_temporal += bit  # Se crea una cadena temporal para verificar la se enciuentra como llave en el diccionario
    # Si el código temporal está en el diccionario de códigos invertido (es decir, si corresponde a un símbolo decodificado)
    if codigo_temporal in diccionario_invertido.keys():  
        # Obtiene el símbolo correspondiente y lo añade a la cadena decodificada   
        simbolo = diccionario_invertido[codigo_temporal]
        cadena_decodificada += simbolo
        codigo_temporal = ''

# Funcion para verificar si la cadena decodifcada es igual a la cadena antes de codificar para crear el archivo
print(cadena_decodificada == cadena)

# Crea el archivo copia.
with open ("decodificado.bin", 'wb') as f:
    f.write(cadena_decodificada)
    f.close

fin = time.time()
tiempo_total = fin - inicio
print(f"El programa tardó {tiempo_total} segundos.")