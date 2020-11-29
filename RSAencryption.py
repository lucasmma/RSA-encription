#!usr/bin
#coding: utf8
import HandlePrimes as primes
import base64
import sympy 
import SHA3
import random
from hashlib import sha512

g = 512
h = 512

def int_to_bytes(x: int) -> bytes:
    return x.to_bytes((x.bit_length() + 7) // 8, 'big')

def bytes_to_bits(b):
    return SHA3.hexStringToBitArray("0x" + b.hex())

nonce = bytes_to_bits(int_to_bytes(random.getrandbits(h)))

def getPairPrimes():
    """
        function that generate a pair of large primes
    """
    p = primes.generate_prime_number(length=1024)
    q = primes.generate_prime_number(length=1024)

    return p,q

def generateKeys(): 

    p, q = getPairPrimes()

    n = multiplyLargeNumber(p, q) #multiplicar os numeros primos

    totiente = multiplyLargeNumber(p-1, q-1)

    e = getFirstCoPrime(totiente)

    d = modinv(e, totiente)

    # print("Primeiro Primo p:\t", p)
    # print("Segundo Primo q:\t", q)
    # print("Valor de n:\t", n)
    # print("Valor do totiente:\t", totiente)
    # print("Valor da chave e:\t", e)
    # print("Valor da chave d:\t", d)

    return e,d,n

def multiplyLargeNumber(n1, n2):
    return n1*n2

def gcd(a,b):
    """
        Find greater common divisor
    """
    while b !=0:
        resto = a % b
        a = b
        b = resto

    return a

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m

def getFirstCoPrime(totiente):
    for i in range(2**1024, totiente + 1):
        mdc = gcd(i, totiente)
        # print("Number: ", i , "\tMDC:  ", mdc)
        if mdc == 1:
            # print("First CoPrime: ", i, "\tTotiente:   ", totiente)
            return i

def encrypt(msg, e, n):
    """
        Encrypt function
    """

    messageInBitArray = bytes_to_bits(msg)

    if 1088 < len(messageInBitArray):
        print("Mensagem muito longa")
        return

    oaep = oaep_pad(messageInBitArray)
    
    b = int_from_bytes(SHA3.getBytesFromBitArray(oaep))

    msgcifrada = pow(b, e, n)

    return msgcifrada

def decrypt(msg, d, n):
    """
        Decrypt function
    """

    msgdecifrada = int_to_bytes(pow(msg, d, n))

    # return msgdecifrada

    preOEAP = bytes_to_bits(msgdecifrada)

    posOEAP = remove_oeappad(preOEAP)

    return SHA3.getBytesFromBitArray(posOEAP[:256])


def int_from_bytes(xbytes: bytes) -> int:
    return int.from_bytes(xbytes, 'big')

def xor(a, b):
    assert len(a) == len(b)
    return [aa^bb for aa, bb in zip(a,b)]

def hash(input_, length):
    h = SHA3.sha3_from_bits(input_,1088,length)
    return bytes_to_bits(h)

def oaep_pad(message):
    mm = message + [0] * (g-len(message))
    G = xor(mm, hash(nonce, g))
    H = xor(nonce, hash(G, h))
    return G+H

def pad_bits(bits, pad):
    assert len(bits) <= pad
    return  [0] * (pad - len(bits)) + bits

def remove_oeappad(message):
    message = pad_bits(message,g+h)
    G = message[:g]
    H = message[g:]
    nonce = xor(H, hash(G,h))
    mm = xor(G,hash(nonce,g))
    return mm[:g]
