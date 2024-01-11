# Codificador LZ77

import struct
import sys
import math

# Función que busca la mejor coincidencia entre la ventana de búsqueda y el lookahead
def LZ77_search(search, look_ahead):
    ls = len(search)
    llh = len(look_ahead)

    # Caso: Ventana de búsqueda vacía
    if ls == 0:
        return (0, 0, look_ahead[0])

    # Caso: Lookahead vacío
    if llh == 0:
        return (-1, -1, "")

    best_length = 0
    best_offset = 0
    buf = search + look_ahead

    search_pointer = ls

    for i in range(0, ls):
        length = 0
        while buf[i + length] == buf[search_pointer + length]:
            length = length + 1
            if search_pointer + length == len(buf):
                length = length - 1
                break
            if i + length >= search_pointer:
                break
        if length > best_length:
            best_offset = i
            best_length = length

    # Devuelve la mejor coincidencia encontrada/triplete
    if best_length > 0:
        return (best_offset, best_length, buf[search_pointer + best_length])
    else:
        return (0, 0, look_ahead[0])

# Función principal que comprime un archivo utilizando el algoritmo LZ77
def compress(file, max_search):
    MAXSEARCH = max_search
    x = 16
    # Cálculo del tamaño máximo del lookahead
    MAXLH = int(math.pow(2, (x - (math.log(MAXSEARCH, 2)))))

    # Lee el contenido del archivo de entrada
    input_data = parse(file)
    compressed_data = bytearray()
    
    searchiterator = 0
    lhiterator = 0

    # Procesa el archivo en busca de coincidencias y las comprime
    while lhiterator < len(input_data):
        # Define la ventana de búsqueda y la ventana de lookahead
        search = input_data[searchiterator:lhiterator]
        look_ahead = input_data[lhiterator:lhiterator + MAXLH]
        
        # Busca la mejor coincidencia utilizando la función LZ77_search
        (offset, length, char) = LZ77_search(search, look_ahead)

        # Prepara y empaqueta la información de la coincidencia en el formato comprimido
        shifted_offset = offset << 6
        offset_and_length = shifted_offset + length
        ol_bytes = struct.pack(">Hc", offset_and_length, bytes([char]))
        compressed_data += ol_bytes

        # Actualiza los iteradores
        lhiterator = lhiterator + length + 1
        searchiterator = lhiterator - MAXSEARCH

        # Ajusta el iterador de búsqueda si es negativo
        if searchiterator < 0:
            searchiterator = 0

    # Escribe los datos comprimidos en un nuevo archivo binario
    compressed_filename = "compressed.bin"
    with open(compressed_filename, "wb") as compressed_file:
        compressed_file.write(compressed_data)

    return compressed_filename

# Función que lee el contenido de un archivo y lo devuelve como texto
def parse(file):
    text = file.read()
    return text

# Bloque principal que no hace nada en este caso
if __name__ == "__main__":
    pass
