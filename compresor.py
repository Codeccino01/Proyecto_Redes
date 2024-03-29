#Codificador LZ77

import struct
import sys
import math

def LZ77_search(search, look_ahead):
    ls = len(search)
    llh = len(look_ahead)

    if ls == 0:
        return (0, 0, look_ahead[0])

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

    if best_length > 0:
        return (best_offset, best_length, buf[search_pointer + best_length])
    else:
        return (0, 0, look_ahead[0])


def compress(file, max_search):
    MAXSEARCH = max_search
    x = 16
    MAXLH = int(math.pow(2, (x - (math.log(MAXSEARCH, 2)))))

    input_data = parse(file)
    compressed_data = bytearray()
    
    searchiterator = 0
    lhiterator = 0

    while lhiterator < len(input_data):
        search = input_data[searchiterator:lhiterator]
        look_ahead = input_data[lhiterator:lhiterator + MAXLH]
        (offset, length, char) = LZ77_search(search, look_ahead)

        shifted_offset = offset << 6
        offset_and_length = shifted_offset + length
        ol_bytes = struct.pack(">Hc", offset_and_length, bytes([char]))
        compressed_data += ol_bytes

        lhiterator = lhiterator + length + 1
        searchiterator = lhiterator - MAXSEARCH

        if searchiterator < 0:
            searchiterator = 0

    compressed_filename = "compressed.bin"
    with open(compressed_filename, "wb") as compressed_file:
        compressed_file.write(compressed_data)

    return compressed_filename
		 

def parse(file):
    r = []
    text = file.read()
    return text


if __name__ == "__main__":
    pass