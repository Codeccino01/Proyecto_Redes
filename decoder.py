#Decodificador LZ77

import struct
import os
import sys

def decoder(file_storage, out_filename, search):
    MAX_SEARCH = search

    # Leer los contenidos del objeto FileStorage
    input_data = file_storage.read()

    chararray = ""
    i = 0

    while i < len(input_data):
        # Desempaquetar, cada 3 bytes (x, y, z)
        (offset_and_length, char) = struct.unpack(">Hc", input_data[i:i + 3])

        # Desplazar a la derecha, obtener offset (desaparece longitud)
        offset = offset_and_length >> 6

        # substraer por offset000000, da el valor de la longitud
        length = offset_and_length - (offset << 6)

        i = i + 3

        # case es (0, 0, c)
        if offset == 0 and length == 0:
            chararray += char.decode('utf-8')

        # case es (x, y, c)
        else:
            iterator = len(chararray) - MAX_SEARCH
            if iterator < 0:
                iterator = offset
            else:
                iterator += offset
            for pointer in range(length):
                chararray += chararray[iterator + pointer]
            chararray += char.decode('utf-8')

    # Ecribir los datos decodificados al archivo de output
    with open(out_filename, "w", encoding="utf-8") as output_file:
        output_file.write(chararray)


if __name__ == "__main__":
    pass
