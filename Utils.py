#!usr/bin
from bitstring import BitArray

def int_from_bytes(xbytes: bytes) -> int:
    return int.from_bytes(xbytes, 'big')

def bytes_from_int(x: int) -> bytes:
    return x.to_bytes((x.bit_length() + 7) // 8, 'big')

def bits_from_bytes(b):
    return bits_from_hexadecimal("0x" + b.hex())

def bytes_from_bits(bitArray):
    value = 0
    for bit in bitArray:
        value = (value << 1) | bit

    return bytes_from_int(value)

def bits_from_string(s):
    result = []
    for c in s:
        bits = bin(ord(c))[2:]
        bits = '00000000'[len(bits):] + bits
        result.extend([int(b) for b in bits])
    return result

def string_from_bits(bits):
    chars = []
    for b in range(int(len(bits) / 8)):
        byte = bits[b*8:(b+1)*8]
        chars.append(chr(int(''.join([str(bit) for bit in byte]), 2)))
    return ''.join(chars)

def bits_from_hexadecimal(word): 
    bit_string = BitArray(hex=word).bin
    return [int(char) for char in bit_string]